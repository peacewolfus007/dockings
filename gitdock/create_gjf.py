import os

def mol2_to_gjf(mol2_filename, gjf_filename):
    atoms = []

    with open(mol2_filename, 'r') as f:
        read_atoms = False
        for line in f:
            if "@<TRIPOS>ATOM" in line:
                read_atoms = True
                continue
            if "@<TRIPOS>BOND" in line:
                break
            if read_atoms:
                parts = line.split()
                atom_type = parts[1]
                x = float(parts[2])
                y = float(parts[3])
                z = float(parts[4])
                atoms.append((atom_type, x, y, z))

    with open(gjf_filename, 'w') as f:
        f.write("%chk=" + os.path.splitext(gjf_filename)[0] + ".chk\n")
        f.write("#P UFF Opt\n")
        f.write("\nMol2 to GJF conversion\n\n")
        f.write("0 1\n")
        for atom in atoms:
            f.write(f"{atom[0]}   {atom[1]:.6f}   {atom[2]:.6f}   {atom[3]:.6f}\n")
        f.write("\n")

if __name__ == "__main__":
    for file in os.listdir("."):
        if file.endswith(".mol2"):
            mol2_filename = file
            gjf_filename = os.path.splitext(file)[0] + ".gjf"
            mol2_to_gjf(mol2_filename, gjf_filename)
            print(f"Converted {mol2_filename} to {gjf_filename}")
