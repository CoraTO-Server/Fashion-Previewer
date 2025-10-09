@echo off
REM One-click BMP cleanup for Fashion-Previewer project
REM This batch file runs the Python cleanup script

echo.
echo ===============================================
echo  BMP Cleanup Script for Fashion-Previewer
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Run the Python script
python cleanup_bmp_files.py

REM Keep window open
echo.
pause
