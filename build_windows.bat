@echo off
setlocal
cd /d "%~dp0"
echo ========================================================
echo Building P-REC External Standalone Executable (Windows)
echo ========================================================

python -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing PyInstaller via pip...
    python -m pip install pyinstaller
)

echo.
echo Compiling prec64.py into single-file binary with bundled assets and league profiles...
python -m PyInstaller --onefile --windowed --noupx --version-file="version_info.txt" --manifest="prec64.manifest" --name prec64 --icon="assets/supreme_soviet.ico" --add-data "leagues;leagues" --add-data "assets;assets" --clean --noconfirm prec64.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo Build Successful!
    echo Executable located at: %~dp0dist\prec64.exe
    echo ========================================================
    copy /y "%~dp0dist\prec64.exe" "%~dp0prec64.exe" >nul 2>&1
    echo Copied prec64.exe to root folder for easy access.
) else (
    echo.
    echo [ERROR] Build failed.
)

endlocal
