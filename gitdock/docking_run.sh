#!/bin/bash

# receptor dosyasının yolu
receptor_path="results/1qsg.pdbqt"

# ligand dosyalarının listesini al ve toplam sayısını hesapla
ligands=( *.pdbqt )
total_ligands=${#ligands[@]}

echo "Toplamda $total_ligands ligand dosyası bulundu."

# Başlangıç zamanını kaydet (saniye cinsinden)
start_secs=$(date +%s)

# her bir ligand dosyası için işlem yap
for index in "${!ligands[@]}"; do
    ligand=${ligands[$index]}
    
    # ligand dosyasının adından uzantıyı çıkar (örn: a.pdbqt --> a)
    base_name=$(basename "$ligand" .pdbqt)
    
    # çıktı dosyalarının isimleri
    out_name="${base_name}_result.pdbqt"
    log_name="${base_name}_result.txt"

    # başlangıç zamanını yaz
    start_time=$(date "+%Y-%m-%d %H:%M:%S")
    echo "Komut Başladı: $start_time - $((index+1)). ligand: $ligand - Kalan: $((total_ligands-index-1))"

    # vina komutu
    ./vina.exe --receptor "$receptor_path" --ligand "$ligand" --center_x 88.472 --center_y 85.056 --center_z -3.472 --size_x 126 --size_y 126 --size_z 125 --out "A_results/$out_name" --log "A_results/$log_name" --exhaustiveness 24

    # bitiş zamanını yaz
    end_time=$(date "+%Y-%m-%d %H:%M:%S")
    echo "Komut Bitti: $end_time - $ligand için işlem tamamlandı."

    # 4 saniye bekle
    sleep 4
done

# Bitiş zamanını kaydet (saniye cinsinden)
end_secs=$(date +%s)

# Toplam süreyi hesapla ve ortalama süreyi bul
total_time=$((end_secs-start_secs))
average_time=$(echo "scale=2; $total_time/$total_ligands" | bc)

echo "Ortalama bir docking işlemi $average_time saniye sürdü."