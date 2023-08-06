#!/bin/bash

# Aynı dizindeki tüm mol2 dosyaları için döngü başlangıcı
for mol2_file in *.mol2; do
	    # Çıktı dosyasının ismini belirleme (örneğin, input.mol2 için output: input.pdbqt)
	        output_file="${mol2_file%.mol2}.pdbqt"
		    
		    # Komutun çalıştırılması
		        /mnt/d/mglinux/bin/pythonsh /mnt/d/mglinux/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l "$mol2_file" -o "$output_file"
		done

