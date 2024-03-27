import os

# Dizin yolu
pdbqt_folder = "/mnt/c/Users/meow2/Downloads/firat_dock/pdbqt/"

# Çıktı dosyası
output_file = "/mnt/c/Users/meow2/Downloads/firat_dock/commands.txt"

# Ligand dosya yolu (örnek)
ligand = "/mnt/c/Users/meow2/Downloads/firat_dock/ligand/ligand.pdbqt"

with open(output_file, "w") as out_f:
    for filename in os.listdir(pdbqt_folder):
        if filename.endswith('.pdbqt'):
            min_x = min_y = min_z = float('inf')
            max_x = max_y = max_z = float('-inf')

            pdbqt_path = os.path.join(pdbqt_folder, filename)
            with open(pdbqt_path, "r") as f:
                for line in f:
                    if line.startswith("ATOM") or line.startswith("HETATM"):
                        x, y, z = map(float, [line[30:38], line[38:46], line[46:54]])
                        min_x = min(min_x, x)
                        min_y = min(min_y, y)
                        min_z = min(min_z, z)
                        max_x = max(max_x, x)
                        max_y = max(max_y, y)
                        max_z = max(max_z, z)

            center_x = (max_x + min_x) / 2
            center_y = (max_y + min_y) / 2
            center_z = (max_z + min_z) / 2

            size_x = max_x - min_x
            size_y = max_y - min_y
            size_z = max_z - min_z

            out_name = f"{filename}_out.pdbqt"
            log_name = f"{filename}_log.txt"

            vina_command = f'./vina.exe --receptor "{pdbqt_path}" --ligand "{ligand}" ' \
                           f'--center_x {center_x} --center_y {center_y} --center_z {center_z} ' \
                           f'--size_x {size_x} --size_y {size_y} --size_z {size_z} ' \
                           f'--out "A_results/{out_name}" --log "A_results/{log_name}" --exhaustiveness 24'

            out_f.write(vina_command + "\n")
