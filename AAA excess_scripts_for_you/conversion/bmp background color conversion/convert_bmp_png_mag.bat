@echo off
REM Convert BMPs to PNGs with magenta transparency
REM This batch file runs the Python script

echo.
echo ===============================================
echo  BMP to PNG Converter (Magenta Transparency)
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
python convert_bmp_png_mag.py %*

REM Keep window open
echo.
pause
