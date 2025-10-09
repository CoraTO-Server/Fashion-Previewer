@echo off
REM Convert 32-bit PNGs to 8-bit BMPs
REM This batch file runs the Python script

echo.
echo ===============================================
echo  32-bit PNG to 8-bit BMP Converter
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
    echo Installing required package: Pillow
    python -m pip install Pillow
    if errorlevel 1 (
        echo ERROR: Failed to install Pillow. Please run install_dependencies.bat first.
        pause
        exit /b 1
    )
)

REM Run the Python script
python Png32ToBmp8.py %*

REM Keep window open
echo.
pause
