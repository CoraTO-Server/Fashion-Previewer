@echo off
echo Fashion Previewer Launcher
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Working directory: %CD%
echo.

REM Check if Python is installed and is version 3.x
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org and make sure to check "Add to PATH" during installation.
    echo After installing Python, restart your computer and try again.
    echo There's also a tutorial in the "AAA Tutorials" folder to help you add to Paths if you don't know how!
    pause
    exit /b 1
)

REM Verify Python version is 3.x
python -c "import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.x is required but another version was found!
    echo The Fashion Previewer uses modern Python features that require version 3.x
    echo Please install Python 3.x from https://python.org
    echo Make sure to check "Add to PATH" during installation.
    echo There's also a tutorial in the "AAA Tutorials" folder to help you add to Paths if you don't know how!
    pause
    exit /b 1
)

REM Check and install required Python packages
echo Checking Python dependencies...
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing Pillow package...
    python -m pip install --upgrade pip
    python -m pip install Pillow
    if errorlevel 1 (
        echo ERROR: Failed to install required package Pillow!
        echo Please try running: pip install Pillow
        echo If that doesn't work, check the troubleshooting guide.
        pause
        exit /b 1
    )
)

REM Check if required Python files exist
cd src
if not exist launch_previewer.py (
    echo Error: launch_previewer.py not found!
    echo Please redownload the repository and try again.
    cd ..
    pause
    exit /b 1
)
if not exist fashionpreviewer.py (
    echo Error: fashionpreviewer.py not found!
    echo Please redownload the repository and try again.
    cd ..
    pause
    exit /b 1
)
if not exist icon_handler.py (
    echo Error: icon_handler.py not found!
    echo Please redownload the repository and try again.
    cd ..
    pause
    exit /b 1
)
if not exist palette_ranges.py (
    echo Error: palette_ranges.py not found!
    echo Please redownload the repository and try again.
    cd ..
    pause
    exit /b 1
)
cd ..

REM Check if required folders exist
if not exist "src\rawbmps" (
    echo WARNING: src\rawbmps folder not found! Character images may not load.
    echo.
)

if not exist "src\nonremovable_assets\vanilla_pals" (
    echo WARNING: src\nonremovable_assets\vanilla_pals folder not found! Fashion palettes may not load.
    echo.
)

if not exist "src\nonremovable_assets\icons" (
    echo WARNING: src\nonremovable_assets\icons folder not found! Icons may not export.
    echo.
)

REM Creating Export folders
if not exist "exports\custom_pals\fashion" (
    echo Creating exports\custom_pals\fashion folder for custom fashion palettes...
    mkdir "exports\custom_pals\fashion" 2>nul
    echo.
)

if not exist "exports\custom_pals\hair" (
    echo Creating exports\custom_pals\hair folder for custom hair palettes...
    mkdir "exports\custom_pals\hair" 2>nul
    echo.
)

if not exist "exports\images" (
    echo Creating exports\images folder for custom images...
    mkdir "exports\images" 2>nul
    echo.
)

if not exist "exports\icons" (
    echo Creating exports\icons folder for custom icons...
    mkdir "exports\icons" 2>nul
    echo.
)

if not exist "exports\colors" (
    echo Creating exports\colors folder for saved colors...
    mkdir "exports\colors" 2>nul
    echo.
)

if not exist "exports\colors\json" (
    echo Creating exports\colors\json folder for JSON color files...
    mkdir "exports\colors\json" 2>nul
    echo.
)

if not exist "exports\colors\icon" (
    echo Creating exports\colors\icon folder for icon color files...
    mkdir "exports\colors\icon" 2>nul
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
    exit /b 1
)