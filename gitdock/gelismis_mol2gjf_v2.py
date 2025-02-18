import os

def mol2_to_gjf(mol2_file, gjf_file, method="# freq b3lyp/lanl2dz geom=connectivity"):
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
                atom_symbol = parts[5]  # Element sembolü (Pd, O, H vs.)
                x, y, z = parts[2:5]    # Koordinatlar
                atom_data.append(f"{atom_symbol:<3} {x:>15} {y:>15} {z:>15}")

        # BOND Bilgilerini Gaussian formatına çevir
        if read_bonds and stripped_line:
            parts = stripped_line.split()
            if len(parts) == 4:
                bond_id, atom1, atom2, bond_type = parts
                atom1, atom2 = int(atom1), int(atom2)

                # **Aromatik bağları 1.5 olarak ayarla**
                if bond_type == "1":
                    bond_type = "1.0"
                elif bond_type == "2":
                    bond_type = "2.0"
                elif bond_type.lower() == "ar":  # Aromatik bağlar
                    bond_type = "1.5"

                bond_data.append((atom1, atom2, bond_type))

    # Bağları Gaussian formatında sıkıştır
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
        f.write("0 1\n")

        # Atom koordinatları
        for atom_line in atom_data:
            f.write(atom_line + "\n")

        # Boş satır
        f.write("\n")

        # Bağ bilgileri
        for atom in sorted(bond_dict.keys()):
            line = f"{atom} " + " ".join(bond_dict[atom])
            f.write(line + "\n")

    print(f"{gjf_file} dosyası başarıyla oluşturuldu.")

def process_all_mol2(directory):
    # Dizindeki tüm .mol2 dosyalarını işle
    for filename in os.listdir(directory):
        if filename.endswith(".mol2"):
            mol2_file = os.path.join(directory, filename)
            gjf_file = os.path.join(directory, filename.replace(".mol2", ".gjf"))
            print(f"İşleniyor: {mol2_file} → {gjf_file}")
            mol2_to_gjf(mol2_file, gjf_file)

# Kullanım: Belirli bir klasördeki tüm .mol2 dosyalarını işle
directory_path = "C:\\Users\\Kullanıcı\\Desktop\\mol2_dosyalar"  # **Buraya kendi klasörünü yaz**
process_all_mol2(directory_path)
