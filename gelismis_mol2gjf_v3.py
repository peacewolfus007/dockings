import re
import argparse
import os

def parse_mol2(file_path):
    """
    .mol2 dosyasındaki ATOM ve BOND satırlarını okuyup
    atom ve bond listelerini döndürür.
    Atomlar: (atom_id, atom_name, atom_type, x, y, z)
    Bağlar:  (atom1_id, atom2_id, bond_type)
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    atoms = []
    bonds = []
    atom_section = False
    bond_section = False

    for line in lines:
        line = line.strip()
        if line.startswith("@<TRIPOS>ATOM"):
            atom_section = True
            bond_section = False
            continue
        elif line.startswith("@<TRIPOS>BOND"):
            atom_section = False
            bond_section = True
            continue
        elif line.startswith("@<TRIPOS>"):
            atom_section = False
            bond_section = False
            continue

        if atom_section and line:
            parts = line.split()
            if len(parts) >= 6:
                atom_id = int(parts[0])
                atom_name = parts[1]       # Örn: 'Pd1', 'Zn01', 'Fe2' vb.
                x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                atom_type = parts[5]      # Örn: 'Pd', 'O.3' vb.
                atoms.append((atom_id, atom_name, atom_type, x, y, z))

        if bond_section and line:
            parts = line.split()
            if len(parts) >= 4:
                # bond_id = int(parts[0])  # Gerekmedikçe kullanmıyoruz
                atom1 = int(parts[1])
                atom2 = int(parts[2])
                bond_type = parts[3]
                bonds.append((atom1, atom2, bond_type))

    return atoms, bonds

def extract_metal_symbol(atom_name):
    """
    Örneğin 'Pd1', 'Zn002', 'Fe12' gibi isimlerden element sembolünü ('Pd', 'Zn', 'Fe') ayıklamak için basit regex.
    Hiç bulamazsa olduğu gibi döndürür.
    """
    match = re.match(r'([A-Za-z]+)', atom_name)
    if match:
        return match.group(1)
    return atom_name  # fallback

def get_first_atom_as_metal(atoms):
    """
    İlk atomu metal kabul eder.
    Geriye (metal_id, metal_symbol) döndürür.
    """
    if not atoms:
        return None, None
    # İlk atom
    first_atom = atoms[0]
    metal_id = first_atom[0]           # sayısal ID
    # Sembolü 'Pd1' -> 'Pd', 'Zn001' -> 'Zn' vb. bul
    metal_symbol = extract_metal_symbol(first_atom[1])
    return metal_id, metal_symbol

def get_metal_neighbors(metal_id, bonds):
    """
    metal_id atomuna doğrudan bağlı atomların ID'lerini döndürür.
    """
    neighbors = []
    for (a1, a2, _) in bonds:
        if a1 == metal_id:
            neighbors.append(a2)
        elif a2 == metal_id:
            neighbors.append(a1)
    return neighbors

def count_bonds(atom_id, bonds):
    """
    Belirli bir atomun toplam kaç bağ yaptığını döndürür.
    (Basitçe bond listesi üzerinden sayım)
    """
    count = 0
    for (a1, a2, _) in bonds:
        if atom_id in (a1, a2):
            count += 1
    return count

def get_formal_charge(atom_type, total_bonds):
    """
    Komşu atom tipine ve bağ sayısına göre (oksijen, azot vb.)
    basit bir formel yük tablosu.
    """
    charge_table = {
        "O": {1: -1, 2: 0, 3: +1},
        "N": {2: -1, 3: 0, 4: +1},
        "C": {3: -1, 4: 0},
        "S": {2: 0, 3: +1, 4: +2, 6: +4},
        "P": {3: 0, 4: +1, 5: +3},
        "B": {3: 0, 4: -1},
        # AROMATIK (ar, AR vb.)
        "AR": {3: 1.5},
        "ar": {3: 1.5},
        "Ar": {3: 1.5}
    }

    # atom_type mesela 'O.3', 'C.2' vb.
    element = atom_type.split(".")[0]  # 'O.3' -> 'O'
    return charge_table.get(element, {}).get(total_bonds, 0)

def calculate_net_charge(atoms, bonds, metal_id, metal_symbol, metal_charge):
    """
    metal_id: ilk atomun ID'si,
    metal_symbol: 'Pd', 'Zn' vs
    metal_charge: kullanıcıdan gelen metal yükü (varsayılan 2)

    Komşu atomların formel yüklerini toplayarak net yük.
    """
    net_charge = metal_charge
    neighbors = get_metal_neighbors(metal_id, bonds)

    for neighbor_id in neighbors:
        # Komşu atomun tipini bul
        # (atom_id, atom_name, atom_type, x, y, z)
        neighbor_atom_type = None
        for (aid, aname, atype, _, _, _) in atoms:
            if aid == neighbor_id:
                neighbor_atom_type = atype
                break

        if neighbor_atom_type:
            # Bağ sayısı
            total_b = count_bonds(neighbor_id, bonds)
            form_charge = get_formal_charge(neighbor_atom_type, total_b)
            net_charge += form_charge

    return net_charge

def calculate_multiplicity(net_charge, metal_symbol):
    """
    Basit e- sayımı üzerinden (toplam_e - net_charge) mod 2'ye göre 1 eşleşmemiş elektron
    varsa doublet, yoksa singlet vb.

    Gelişmiş spin durumları için ligand alan kuramı vs. gerekli.
    Burada basit yaklaşımla:
      unpaired_electrons = (toplam_e - net_charge) % 2
    """
    # Bazı metallerin nötr hal elektron sayısı
    # (Kullanıcı bu listeyi genişletebilir)
    electron_dict = {
        "Pd": 46,
        "Zn": 30,
        "Fe": 26,
        "B": 5,
        # İstersen başka elementler ekle:
        # "Ni": 28, ...
    }
    total_electrons = electron_dict.get(metal_symbol, 46)  # Varsayılan 46

    # Yük çıkart
    # Ör. +2 yük -> 2 elektron eksik
    effective_electrons = total_electrons - net_charge

    # Tek/çift kontrolü
    unpaired_electrons = effective_electrons % 2
    S = unpaired_electrons / 2
    multiplicity = int(2 * S + 1)
    return multiplicity

def mol2_to_gjf(mol2_file, gjf_file, method="# freq b3lyp/lanl2dz geom=connectivity", metal_charge=2):
    """
    Tek bir .mol2 dosyasını okuyup .gjf dosyası oluşturur.
    (İlk atom metal kabul edilir, net yük & multiplicity hesaplanır.)
    """
    atoms, bonds = parse_mol2(mol2_file)

    if not atoms:
        print(f"[Uyarı] {mol2_file} içinde atom yok. Atlanıyor.")
        return

    metal_id, metal_symbol = get_first_atom_as_metal(atoms)
    if metal_id is None:
        print(f"[Uyarı] İlk atom bulunamadı. {mol2_file} atlanıyor.")
        return

    net_charge = calculate_net_charge(
        atoms, bonds, metal_id, metal_symbol, metal_charge
    )
    multiplicity = calculate_multiplicity(net_charge, metal_symbol)

    # GJF'ye yazmak için atom koordinatları
    atom_lines = []
    for (atom_id, atom_name, atom_type, x, y, z) in atoms:
        atom_lines.append(f"{atom_name:<4} {x:>15.4f} {y:>15.4f} {z:>15.4f}")

    # Dosyayı oluştur
    with open(gjf_file, "w") as f:
        f.write("%nprocshared=20\n")
        f.write(f"{method}\n\n")
        f.write("MOL\n\n")
        f.write(f"{net_charge} {multiplicity}\n")
        for line in atom_lines:
            f.write(line + "\n")

    print(
        f"[OK] {gjf_file} oluşturuldu. "
        f"(Metal: {metal_symbol}, Yük: {net_charge}, Spin: {multiplicity})"
    )

def process_all_mol2(directory, metal_charge):
    """
    Verilen klasördeki tüm .mol2 dosyalarını GJF'ye çevirir.
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith(".mol2"):
            mol2_file = os.path.join(directory, filename)
            gjf_file = os.path.join(directory, filename.replace(".mol2", ".gjf"))
            print(f"İşleniyor: {mol2_file} → {gjf_file}")
            mol2_to_gjf(mol2_file, gjf_file, metal_charge=metal_charge)

def main():
    parser = argparse.ArgumentParser(
        description="Convert MOL2 files to Gaussian input files with auto metal detection."
    )
    parser.add_argument("--file", required=True,
                        help="Directory containing MOL2 files")
    parser.add_argument("--charge", type=int, default=2,
                        help="Charge of metal (default: +2)")

    args = parser.parse_args()
    process_all_mol2(args.file, args.charge)

if __name__ == "__main__":
    main()


#########################
##Kod artık ilk atomu otomatik olarak metal atomu kabul edecek ve varsayılan olarak yükü +2 alacak, ancak kullanıcı --charge argümanıyla değiştirebilecek. Ayrıca --file argümanıyla hangi dizindeki .mol2 dosyalarının işleneceğini belirleyebilirsin.
##
##Kullanım:
##
##python3 gelismis_mol2gjf_v3.py --file /home/barbar/mol2s --charge 3
##veya
##
##python3 gelismis_mol2gjf_v3.py --file /home/barbar/mol2s
##Bu, hem net yükü hem de spin durumunu Gaussian .gjf dosyasında "0 1" yerine doğru değerlerle yazacaktır.
#####################