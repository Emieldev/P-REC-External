@echo off
title P-REC External
cd /d "%~dp0"
echo Starting P-REC External for Team Fortress 2...
python -u prec64.py PREC_Settings.cfg
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] P-REC External exited with an error.
    echo Make sure Python 3 is installed and added to your system PATH.
    pause
)
