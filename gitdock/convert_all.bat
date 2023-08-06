@echo off
SETLOCAL EnableDelayedExpansion

REM Eğer results klasörü yoksa oluştur
if not exist results mkdir results

for %%f in (*.pdb) do (
    set base_name=%%~nf

    echo Starting %%f at %date% %time%
    "D:\mgl157\python.exe" "D:\mgl157\Lib\site-packages\AutoDockTools\Utilities24\prepare_ligand4.py" -l "%%f" -v -A hydrogens -U nphs -o "results\!base_name!1.pdbqt"
    echo Finished %%f at %date% %time%

    timeout /t 3 /nobreak
)

endlocal
