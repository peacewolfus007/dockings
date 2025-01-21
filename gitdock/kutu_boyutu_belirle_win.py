import os

# Çalışılan dizin (scriptin bulunduğu dizin)
current_directory = os.getcwd()

# Çıktı dosyası (commands.txt, çalışılan dizinde oluşturulacak)
output_file = os.path.join(current_directory, "commands.txt")

# Ligand dosya yolu (örnek, çalışılan dizinde ligand.pdbqt olarak varsayıldı)
ligand = os.path.join(current_directory, "ligand.pdbqt")

# Çıktı dizini (A_results) oluşturuluyor
output_dir = os.path.join(current_directory, "A_results")
os.makedirs(output_dir, exist_ok=True)

with open(output_file, "w") as out_f:
    for filename in os.listdir(current_directory):
        if filename.endswith('.pdb'):  # Sadece .pdb dosyalarını işle
            min_x = min_y = min_z = float('inf')
            max_x = max_y = max_z = float('-inf')

            pdb_path = os.path.join(current_directory, filename)
            with open(pdb_path, "r") as f:
                for line in f:
                    if line.startswith("ATOM") or line.startswith("HETATM"):
                        try:
                            x, y, z = map(float, [line[30:38], line[38:46], line[46:54]])
                            min_x = min(min_x, x)
                            min_y = min(min_y, y)
                            min_z = min(min_z, z)
                            max_x = max(max_x, x)
                            max_y = max(max_y, y)
                            max_z = max(max_z, z)
                        except ValueError:
                            # Koordinatlar geçersizse bu satırı atla
                            continue

            center_x = (max_x + min_x) / 2
            center_y = (max_y + min_y) / 2
            center_z = (max_z + min_z) / 2

            size_x = max_x - min_x
            size_y = max_y - min_y
            size_z = max_z - min_z

            out_name = f"{filename}_out.pdbqt"
            log_name = f"{filename}_log.txt"

            vina_command = f'vina.exe --receptor "{pdb_path}" --ligand "{ligand}" ' \
                           f'--center_x {center_x} --center_y {center_y} --center_z {center_z} ' \
                           f'--size_x {size_x} --size_y {size_y} --size_z {size_z} ' \
                           f'--out "{os.path.join(output_dir, out_name)}" --log "{os.path.join(output_dir, log_name)}" --exhaustiveness 24'

            out_f.write(vina_command + "\n")