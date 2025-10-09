@echo off
REM One-click BMP folder renamer and cleanup
REM This batch file runs the Python script

echo.
echo ===============================================
echo  BMP Folder Renamer and Cleanup
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
python delete_bmp_rename_folder.py

REM Keep window open
echo.
pause
