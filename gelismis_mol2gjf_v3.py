import os
# netcharge_and_spin.py'deki gerekli fonksiyonları içeri aktar
from netcharge_and_spin import calculate_net_charge, calculate_multiplicity

def mol2_to_gjf(mol2_file, gjf_file, method="# freq b3lyp/lanl2dz geom=connectivity", metal_symbol="Pd", metal_charge=2):
    # MOL2 dosyasından verileri oku
    with open(mol2_file, "r") as f:
        lines = f.readlines()

    atom_data = []
    bond_data = []
    read_atoms = False
    read_bonds = False

    for line in lines:
        stripped_line = line.strip()

        # ATOM bölümünü başlat
        if stripped_line.startswith("@<TRIPOS>ATOM"):
            read_atoms = True
            continue
        elif stripped_line.startswith("@<TRIPOS>BOND"):
            read_atoms = False
            read_bonds = True
            continue

        # ATOM Koordinatlarını Al
        if read_atoms and stripped_line:
            parts = stripped_line.split()
            if len(parts) >= 6:
                atom_symbol_line = parts[5]  # Element sembolü (Pd, O, H vs.)
                x, y, z = parts[2:5]         # Koordinatlar
                atom_data.append(f"{atom_symbol_line:<3} {x:>15} {y:>15} {z:>15}")

        # BOND Bilgilerini Gaussian formatına çevir
        if read_bonds and stripped_line:
            parts = stripped_line.split()
            if len(parts) == 4:
                bond_id, atom1, atom2, bond_type = parts
                atom1, atom2 = int(atom1), int(atom2)

                # Aromatik bağları 1.5 olarak ayarla
                if bond_type == "1":
                    bond_type = "1.0"
                elif bond_type == "2":
                    bond_type = "2.0"
                elif bond_type.lower() == "ar":  # Aromatik bağlar
                    bond_type = "1.5"

                bond_data.append((atom1, atom2, bond_type))

    # Gaussian giriş dosyasını oluştururken, net yük ve spin hesaplamasını yap
    # (netcharge_and_spin.py dosyası dosyayı kendi okuyor; burada doğrudan mol2_file yolunu veriyoruz)
    net_charge = calculate_net_charge(mol2_file, metal_symbol, metal_charge)
    # Metal atomuna göre toplam elektron sayısı: Pd için 46, Zn için 30 gibi. Burada varsayılan Pd kabul edildi.
    total_electrons = 46 if metal_symbol == "Pd" else 30
    multiplicity = calculate_multiplicity(net_charge, total_electrons)

    # Bağ bilgilerini Gaussian formatında sıkıştır
    bond_dict = {}
    for atom1, atom2, bond_type in bond_data:
        if atom1 not in bond_dict:
            bond_dict[atom1] = []
        bond_dict[atom1].append(f"{atom2} {bond_type}")

        if atom2 not in bond_dict:
            bond_dict[atom2] = []
        bond_dict[atom2].append(f"{atom1} {bond_type}")

    # Gaussian giriş dosyasına yaz
    with open(gjf_file, "w") as f:
        # Başlıklar
        f.write("%nprocshared=20\n")
        f.write(f"{method}\n\n")
        f.write("MOL\n\n")
        # Hesaplanan net_charge ve multiplicity değerlerini yaz (örneğin: -1 2)
        f.write(f"{net_charge} {multiplicity}\n")

        # Atom koordinatları
        for atom_line in atom_data:
            f.write(atom_line + "\n")

        # Boş satır
        f.write("\n")

        # Bağ bilgileri
        for atom in sorted(bond_dict.keys()):
            line = f"{atom} " + " ".join(bond_dict[atom])
            f.write(line + "\n")

    print(f"{gjf_file} dosyası başarıyla oluşturuldu. (Net Yük: {net_charge}, Spin: {multiplicity})")

def process_all_mol2(directory, metal_symbol="Pd", metal_charge=2):
    # Dizindeki tüm .mol2 dosyalarını işle
    for filename in os.listdir(directory):
        if filename.endswith(".mol2"):
            mol2_file = os.path.join(directory, filename)
            gjf_file = os.path.join(directory, filename.replace(".mol2", ".gjf"))
            print(f"İşleniyor: {mol2_file} → {gjf_file}")
            mol2_to_gjf(mol2_file, gjf_file, metal_symbol=metal_symbol, metal_charge=metal_charge)

# Kullanım: Belirli bir klasördeki tüm .mol2 dosyalarını işle
directory_path = "/home/barbar/mol2s"  # **Buraya kendi klasörünüzü yazınız**
process_all_mol2(directory_path)
