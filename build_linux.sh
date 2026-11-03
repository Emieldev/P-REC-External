#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================"
echo "Building P-REC 64 Standalone Binary (Linux)"
echo "========================================================"

if ! command -v pyinstaller &> /dev/null && ! python3 -m PyInstaller --version &> /dev/null; then
    echo "PyInstaller not found. Installing PyInstaller via pip..."
    python3 -m pip install --user pyinstaller
fi

echo "Compiling prec64.py into single-file binary with bundled league profiles..."
if command -v pyinstaller &> /dev/null; then
    pyinstaller --onefile --name prec64 --add-data "leagues:leagues" --clean --noconfirm prec64.py
else
    python3 -m PyInstaller --onefile --name prec64 --add-data "leagues:leagues" --clean --noconfirm prec64.py
fi

if [ -f "$SCRIPT_DIR/dist/prec64" ]; then
    cp "$SCRIPT_DIR/dist/prec64" "$SCRIPT_DIR/prec64"
    chmod +x "$SCRIPT_DIR/prec64"
    echo "========================================================"
    echo "Build Successful!"
    echo "Binary located at: $SCRIPT_DIR/prec64"
    echo "========================================================"
fi

