import os
def log_to_xyz(log_filename, xyz_filename, code):
    with open(log_filename, 'r') as f:
        lines = f.readlines()

    rotation_line_index = next(i for i, line in enumerate(lines) if 'Rotational constants (GHZ)' in line)
    start_line_index = rotation_line_index - 1
    while not "----" in lines[start_line_index]:
        start_line_index -= 1
    end_line_index = start_line_index - 1
    while not "----" in lines[end_line_index]:
        end_line_index -= 1
    section = lines[end_line_index + 1 : start_line_index]

    atoms = []
    for line in section:
        parts = line.split()
        atom_num = parts[1]
        x, y, z = map(float, parts[3:6])
        atom_name = code.get(atom_num, "X")
        atoms.append((atom_name, x, y, z))

    with open(xyz_filename, "w") as xyz_file:
        xyz_file.write(f"{len(atoms)}\n")
        xyz_file.write("Converted from Gaussian log\n")
        for atom in atoms:
            xyz_file.write(f"{atom[0]}  {atom[1]:.6f}  {atom[2]:.6f}  {atom[3]:.6f}\n")

    print(f"Conversion from {log_filename} to {xyz_filename} completed!")

# Kullanıcıdan hangi dosya uzantılarını çevireceğini sormak için
file_extension = input("Lütfen dönüştürmek istediğiniz dosya uzantısını girin (örn: log, LOG, OUT, out): ")

# Atom kodları için sözlük
code = {"1" : "H", "2" : "He", "3" : "Li", "4" : "Be", "5" : "B", 
"6"  : "C", "7"  : "N", "8"  : "O", "9" : "F", "10" : "Ne",
"11" : "Na" , "12" : "Mg" , "13" : "Al" , "14" : "Si" , "15" : "P", 
"16" : "S"  , "17" : "Cl" , "18" : "Ar" , "19" : "K"  , "20" : "Ca",
"21" : "Sc" , "22" : "Ti" , "23" : "V"  , "24" : "Cr" , "25" : "Mn",
"26" : "Fe" , "27" : "Co" , "28" : "Ni" , "29" : "Cu" , "30" : "Zn",
"31" : "Ga" , "32" : "Ge" , "33" : "As" , "34" : "Se" , "35" : "Br",
"36" : "Kr" , "37" : "Rb" , "38" : "Sr" , "39" : "Y"  , "40" : "Zr",
"41" : "Nb" , "42" : "Mo" , "43" : "Tc" , "44" : "Ru" , "45" : "Rh",
"46" : "Pd" , "47" : "Ag" , "48" : "Cd" , "49" : "In" , "50" : "Sn",
"51" : "Sb" , "52" : "Te" , "53" : "I"  , "54" : "Xe" , "55" : "Cs",
"56" : "Ba" , "57" : "La" , "58" : "Ce" , "59" : "Pr" , "60" : "Nd",
"61" : "Pm" , "62" : "Sm" , "63" : "Eu" , "64" : "Gd" , "65" : "Tb",
"66" : "Dy" , "67" : "Ho" , "68" : "Er" , "69" : "Tm" , "70" : "Yb",
"71" : "Lu" , "72" : "Hf" , "73" : "Ta" , "74" : "W"  , "75" : "Re",
"76" : "Os" , "77" : "Ir" , "78" : "Pt" , "79" : "Au" , "80" : "Hg",
"81" : "Tl" , "82" : "Pb" , "83" : "Bi" , "84" : "Po" , "85" : "At",
"86" : "Rn" , "87" : "Fr" , "88" : "Ra" , "89" : "Ac" , "90" : "Th",
"91" : "Pa" , "92" : "U"  , "93" : "Np" , "94" : "Pu" , "95" : "Am",
"96" : "Cm" , "97" : "Bk" , "98" : "Cf" , "99" : "Es" ,"100" : "Fm",
"101": "Md" ,"102" : "No" ,"103" : "Lr" ,"104" : "Rf" ,"105" : "Db",
"106": "Sg" ,"107" : "Bh" ,"108" : "Hs" ,"109" : "Mt" ,"110" : "Ds",
"111": "Rg" ,"112" : "Uub","113" : "Uut","114" : "Uuq","115" : "Uup",
"116": "Uuh","117" : "Uus","118" : "Uuo"} 

directory_path = "."  

for filename in os.listdir(directory_path):
    if filename.endswith(f".{file_extension}"):
        log_to_xyz(filename, filename.replace(f".{file_extension}", ".xyz"), code)
