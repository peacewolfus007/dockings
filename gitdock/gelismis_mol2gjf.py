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
                bond_type = "1.0" if bond_type == "1" else "2.0"

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

# Kullanım
mol2_to_gjf("input.mol2", "output.gjf")
