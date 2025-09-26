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

REM Check if src folder exists
if not exist "src" (
    echo ERROR: src folder not found!
    echo Make sure this batch file is in the same folder as the src folder
    pause
    exit /b 1
)

REM Check if the launcher script exists
if not exist "src\launch_previewer.py" (
    echo ERROR: src\launch_previewer.py not found!
    echo Make sure launch_previewer.py is in the src folder
    pause
    exit /b 1
)

REM Check if the main script exists
if not exist "src\fashionpreviewer.py" (
    echo ERROR: src\fashionpreviewer.py not found!
    echo Make sure fashionpreviewer.py is in the src folder
    exit /b 1
)

REM Check if required folders exist
if not exist "src\rawbmps" (
    echo WARNING: src\rawbmps folder not found! Character images may not load.
    echo.
)

if not exist "src\vanilla_pals" (
    echo WARNING: src\vanilla_pals folder not found! Fashion palettes may not load.
    echo.
)

REM Creating Export folders
if not exist "exports\custom_pals" (
    echo Creating exports\custom_pals folder for custom palettes...
    mkdir "exports\custom_pals" 2>nul
    echo.
)

if not exist "exports\images" (
    echo Creating exports\images folder for custom images...
    mkdir "exports\images" 2>nul
    echo.
)

echo Starting Fashion Previewer...
echo.
cd src
python launch_previewer.py
cd ..

if errorlevel 1 (
    echo.
    echo ERROR: The application crashed or failed to start!
    echo This might be due to missing dependencies.
    echo Try running: pip install Pillow
    pause
)