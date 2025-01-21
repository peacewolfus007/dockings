@echo off
SETLOCAL EnableDelayedExpansion

REM Eğer results klasörü yoksa oluştur
if not exist results mkdir results

for %%f in (*.pdb) do (
    set base_name=%%~nf

    echo Starting receptor preparation for %%f at %date% %time%
    "D:\mgl157\python.exe" "D:\mgl157\Lib\site-packages\AutoDockTools\Utilities24\prepare_receptor4.py" -r "%%f" -v -A hydrogens -U nphs -o "results\!base_name!.pdbqt"
    echo Finished receptor preparation for %%f at %date% %time%

    timeout /t 3 /nobreak
)

endlocal