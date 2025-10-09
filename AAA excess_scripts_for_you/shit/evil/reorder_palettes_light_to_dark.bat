@echo off
REM Sort RIFF palette colors from brightest to darkest
REM This batch file runs the Python script

echo.
echo ===============================================
echo  Palette Color Sorter (Light to Dark)
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

REM Run the Python script (no external dependencies needed)
python reorder_palettes_light_to_dark.py %*

REM Keep window open
echo.
pause
