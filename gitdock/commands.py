# Dosyayı okuma modunda aç
with open("commands.txt", "r") as infile:
    lines = infile.readlines()

# Yeni komutları saklamak için bir liste oluştur
corrected_lines = []

for line in lines:
    # Komutları düzelt
    corrected_line = line.replace(".\\vina.exe", "./vina.exe") \
                          .replace("\\mnt\\c\\", "C:\\\\") \
                          .replace("A_results\\", "A_results\\\\")
    corrected_lines.append(corrected_line)

# Dosyayı yazma modunda aç ve düzeltilmiş komutları yaz
with open("corrected_commands.txt", "w") as outfile:
    outfile.writelines(corrected_lines)
