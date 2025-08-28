@echo off
echo Fashion Previewer Launcher
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Working directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org and make sure to check "Add to PATH" during installation.
    echo After installing Python, restart your computer and try again.
    pause
    exit /b 1
)

REM Check if the launcher script exists
if not exist "launch_previewer.py" (
    echo ERROR: launch_previewer.py not found!
    echo Make sure this batch file is in the same folder as launch_previewer.py
    pause
    exit /b 1
)

REM Check if the main script exists
if not exist "fashionpreviewer_v2.2.py" (
    echo ERROR: fashionpreviewer_v2.2.py not found!
    echo Make sure this batch file is in the same folder as fashionpreviewer_v2.1.py
    pause
    exit /b 1
)

REM Check if required folders exist
if not exist "rawbmps" (
    echo WARNING: rawbmps folder not found! Character images may not load.
    echo.
)

if not exist "pals" (
    echo WARNING: pals folder not found! Fashion palettes may not load.
    echo.
)

echo Starting Fashion Previewer...
echo.
python launch_previewer.py

if errorlevel 1 (
    echo.
    echo ERROR: The application crashed or failed to start!
    echo This might be due to missing dependencies.
    echo Try running: pip install Pillow
    pause
)
