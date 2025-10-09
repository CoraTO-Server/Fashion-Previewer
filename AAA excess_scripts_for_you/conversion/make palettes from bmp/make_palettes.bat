@echo off
REM Generate palettes with advanced options
REM This batch file runs the Python script with dependency checks

echo.
echo ===============================================
echo  Advanced Palette Generator
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

REM Check for Pillow
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing required package: Pillow...
    python -m pip install --quiet Pillow >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to install Pillow. Try running as administrator.
        pause
        exit /b 1
    )
)

REM Check for numpy
python -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo Installing required package: numpy...
    python -m pip install --quiet numpy >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to install numpy. Try running as administrator.
        pause
        exit /b 1
    )
)

REM Run the Python script
echo Running palette generator...
python make_palettes_v2.py %*

REM Keep window open
echo.
echo Palette generation complete!
pause
