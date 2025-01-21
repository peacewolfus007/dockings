@echo on
setlocal enabledelayedexpansion

:: Ana dizin ve klasör yolları
set "base_dir=D:\murathocabildiri"
set "results_dir=%base_dir%\results"
:: Receptor dosyasının yolu
set "receptor_path=%results_dir%\1qsg.pdbqt"

:: Results klasöründeki tüm pdbqt dosyalarını say (receptor hariç)
set count=0
for %%f in (%results_dir%\*.pdbqt) do (
    if not "%%f"=="%receptor_path%" (
        set /a count+=1
    )
)
echo Toplamda %count% ligand dosyasi bulundu.

:: A_results klasörü yoksa oluştur
if not exist "%base_dir%\A_results" mkdir "%base_dir%\A_results"

:: Her bir ligand için docking yap (receptor hariç)
set current=0
for %%f in (%results_dir%\*.pdbqt) do (
    if not "%%f"=="%receptor_path%" (
        set /a current+=1
        set "ligand=%%f"
        set "base_name=%%~nf"
        
        :: Çıktı dosyalarının isimleri
        set "out_name=!base_name!_out.pdbqt"
        set "log_name=!base_name!_log.txt"
        
        :: İşlem bilgisini göster
        echo.
        echo ======================================
        echo Islem: !current!/%count%
        echo Ligand: !ligand!
        echo Tarih/Saat: %DATE% %TIME%
        echo ======================================
        
        :: Vina komutu
        vina.exe --receptor "%receptor_path%" --ligand "!ligand!" ^
            --center_x 24.068 --center_y 18.8255 --center_z 19.654 ^
            --size_x 132.61 --size_y 100.679 --size_z 128.386 ^
            --out "%base_dir%\A_results\!out_name!" ^
            --log "%base_dir%\A_results\!log_name!" ^
            --exhaustiveness 24
        
        :: İşlem bitti bilgisi
        echo.
        echo !ligand! icin docking tamamlandi.
        echo ======================================
        
        :: 4 saniye bekle
        timeout /t 4 /nobreak >nul
    )
)

echo.
echo Tum docking islemleri tamamlandi.
pause