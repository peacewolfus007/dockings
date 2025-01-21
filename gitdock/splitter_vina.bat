@echo on
setlocal enabledelayedexpansion

:: Tüm PDBQT dosyalarını döngüye al
for %%f in (*.pdbqt) do (
    :: Dosya adını al (uzantısız)
    set "base_name=%%~nf"
    
    echo ======================================
    echo Processing: %%f
    
    :: Bu dosya adıyla klasör oluştur (eğer yoksa)
    if not exist "!base_name!" mkdir "!base_name!"
    
    :: vina_split ile modellere ayır ve klasöre kaydet
    vina_split.exe --input %%f --ligand "!base_name!\ligand_"
    
    echo Completed: %%f
    echo ======================================
    echo.
)

echo Tum dosyalar islendi
pause