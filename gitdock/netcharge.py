import re
import argparse

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
            atoms.append((atom_id, atom_name, atom_type))
        elif bond_section:
            parts = line.split()
            bond_id, atom1, atom2, bond_type = int(parts[0]), int(parts[1]), int(parts[2]), parts[3]
            bonds.append((atom1, atom2))
    
    return atoms, bonds

def get_pd_neighbors(pd_id, bonds):
    pd_neighbors = []
    for bond in bonds:
        if bond[0] == pd_id:
            pd_neighbors.append(bond[1])
        elif bond[1] == pd_id:
            pd_neighbors.append(bond[0])
    return pd_neighbors

def count_bonds(atom_id, bonds):
    count = 0
    for bond in bonds:
        if atom_id in bond:
            count += 1
    return count

def get_formal_charge(atom_type, total_bonds):
    charge_table = {
        "O": {1: -1, 2: 0, 3: +1},
        "N": {2: -1, 3: 0, 4: +1},
        "C": {3: -1, 4: 0},
        "S": {2: 0, 3: +1, 4: +2, 6: +4},
        "P": {3: 0, 4: +1, 5: +3},
        "B": {3: 0, 4: -1},
        "AR": {3: 1.5},
        "ar": {3: 1.5},
        "Ar": {3: 1.5}
    }
    element = atom_type.split(".")[0]  # Remove hybridization info (e.g., C.3 -> C)
    return charge_table.get(element, {}).get(total_bonds, 0)  # Default to 0 if not in table

def calculate_net_charge(file_path, pd_symbol="Pd", pd_charge=2):
    atoms, bonds = parse_mol2(file_path)
    pd_id = None
    
    for atom in atoms:
        if atom[1].startswith(pd_symbol):
            pd_id = atom[0]
            break
    
    if pd_id is None:
        raise ValueError("Pd atom not found in the file")
    
    pd_neighbors = get_pd_neighbors(pd_id, bonds)
    net_charge = pd_charge
    
    for neighbor_id in pd_neighbors:
        atom_type = None
        for atom in atoms:
            if atom[0] == neighbor_id:
                atom_type = atom[2]
                break
        
        total_bonds = count_bonds(neighbor_id, bonds)
        formal_charge = get_formal_charge(atom_type, total_bonds)
        net_charge += formal_charge
    
    return net_charge

def main():
    parser = argparse.ArgumentParser(description="Calculate net charge of Pd complex from MOL2 file.")
    parser.add_argument("--file", required=True, help="MOL2 file path")
    parser.add_argument("--charge", type=int, default=2, help="Charge of Pd (default: +2)")
    parser.add_argument("--atom", type=str, default="Pd", help="Pd atom label (default: Pd)")
    
    args = parser.parse_args()
    
    net_charge = calculate_net_charge(args.file, args.atom, args.charge)
    print("Net Yük:", net_charge)

if __name__ == "__main__":
    main()



##########################

###python3 netcharge.py --file ABEVEL.mol2 --charge 2 --atom Pd
###veya sadece (default değerler Pd ve +2 olduğundan) :
###python3 netcharge.py --file ABEVEL.mol2
###yazarak çalıştır...
############################