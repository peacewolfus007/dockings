import re
import argparse
import os

def parse_mol2(file_path):
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
        
        if atom_section:
            parts = line.split()
            atom_id, atom_name, x, y, z, atom_type = int(parts[0]), parts[1], float(parts[2]), float(parts[3]), float(parts[4]), parts[5]
            atoms.append((atom_id, atom_name, atom_type, x, y, z))
    
    return atoms

def determine_metal(atoms):
    if atoms:
        return atoms[0][1]  # İlk atomun adını metal olarak al
    return "Pd"  # Varsayılan olarak Pd kullan

def calculate_net_charge(file_path, metal_charge=2):
    atoms = parse_mol2(file_path)
    metal_symbol = determine_metal(atoms)
    net_charge = metal_charge
    return metal_symbol, net_charge

def calculate_multiplicity(net_charge, metal_symbol):
    total_electrons_dict = {"Pd": 46, "Zn": 30, "B": 5}
    total_electrons = total_electrons_dict.get(metal_symbol, 46)  # Varsayılan olarak Pd için 46 kullan
    total_electrons -= net_charge  # Yükü hesaba katarak elektron sayısını düzelt
    unpaired_electrons = total_electrons % 2  # Çift sayıda değilse 1 eşleşmemiş elektron var
    S = unpaired_electrons / 2
    return int(2 * S + 1)

def mol2_to_gjf(mol2_file, gjf_file, method="# freq b3lyp/lanl2dz geom=connectivity", metal_charge=2):
    atoms = parse_mol2(mol2_file)
    metal_symbol, net_charge = calculate_net_charge(mol2_file, metal_charge)
    multiplicity = calculate_multiplicity(net_charge, metal_symbol)
    
    atom_data = []
    for atom in atoms:
        atom_id, atom_name, atom_type, x, y, z = atom
        atom_data.append(f"{atom_name:<3} {x:>15} {y:>15} {z:>15}")
    
    with open(gjf_file, "w") as f:
        f.write("%nprocshared=20\n")
        f.write(f"{method}\n\n")
        f.write("MOL\n\n")
        f.write(f"{net_charge} {multiplicity}\n")
        
        for atom_line in atom_data:
            f.write(atom_line + "\n")
    
    print(f"{gjf_file} dosyası başarıyla oluşturuldu.")

def process_all_mol2(directory, metal_charge):
    for filename in os.listdir(directory):
        if filename.endswith(".mol2"):
            mol2_file = os.path.join(directory, filename)
            gjf_file = os.path.join(directory, filename.replace(".mol2", ".gjf"))
            print(f"İşleniyor: {mol2_file} → {gjf_file}")
            mol2_to_gjf(mol2_file, gjf_file, metal_charge=metal_charge)

def main():
    parser = argparse.ArgumentParser(description="Convert MOL2 files to Gaussian input files with automatic metal detection.")
    parser.add_argument("--file", required=True, help="Directory containing MOL2 files")
    parser.add_argument("--charge", type=int, default=2, help="Charge of metal (default: +2)")
    
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