@echo off
echo +------------------------------------------------+
echo [               Fashion                          ]
echo [                   Previewer                    ]
echo [                       Launcher                 ]
echo +------------------------------------------------+
echo.
echo Lovingly made by:
echo KusangiKyo, Dino, Yuki, and Mewsie.
echo.
echo From CoraTO, on behalf of the Trickster community.
echo Thank you for everything :3
echo.
echo +------------------------------------------------+
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

REM Check if pip exists and install if needed ===
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Pip not found. Trying to install pip...
    python -m ensurepip --default-pip >nul 2>&1
    if errorlevel 1 (
        echo WARNING: 'ensurepip' failed or pip is externally managed.
        echo Attempting fallback check for pip...
    )

    REM Recheck if pip was installed successfully after ensurepip attempt
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Pip is still not working!
        echo Please try the following:
        echo 1. Right-click this script and choose "Run as administrator"
        echo 2. Or manually install pip from https://pip.pypa.io
        pause
        exit /b 1
    ) else (
        echo Pip installed successfully.
        python -m pip install --upgrade pip --no-warn-script-location >nul 2>&1
    )
) else (
    echo Pip is working.
)

REM Check if Pillow is installed
echo Checking for required dependencies...
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing Pillow...
    python -m pip install Pillow --no-warn-script-location >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to install Pillow! Please try:
        echo 1. Right-click this script
        echo 2. Select "Run as administrator"
        echo 3. After Pillow installs, you can run normally by double-clicking
        pause
        exit /b 1
    )
    echo Pillow installed successfully.
) else (
    echo Pillow is installed.
)

REM Check if src folder exists
if not exist "src" (
    echo ERROR: src folder not found!
    echo Make sure this batch file is in the same folder as the src folder
    pause
    exit /b 1
)

REM Check if required Python files exist
if not exist "src\launch_previewer.py" (
    echo Error: src\launch_previewer.py not found!
    echo Please redownload the repository and try again.
    pause
    exit /b 1
)
if not exist "src\fashionpreviewer.py" (
    echo Error: src\fashionpreviewer.py not found!
    echo Please redownload the repository and try again.
    pause
    exit /b 1
)
if not exist "src\icon_handler.py" (
    echo Error: src\icon_handler.py not found!
    echo Please redownload the repository and try again.
    pause
    exit /b 1
)
if not exist "src\palette_ranges.py" (
    echo Error: src\palette_ranges.py not found!
    echo Please redownload the repository and try again.
    pause
    exit /b 1
)

REM Check if required folders exist
if not exist "src\rawbmps" (
    echo WARNING: src\rawbmps folder not found! Character images may not load.
    echo.
)

if not exist "src\nonremovable_assets\vanilla_pals" (
    echo WARNING: src\nonremovable_assets\vanilla_pals folder not found! Fashion palettes may not load.
    echo.
)

if not exist "src\nonremovable_assets\vanilla_pals\3rd_default_fashion" (
    echo WARNING: src\nonremovable_assets\vanilla_pals\3rd_default_fashion folder not found! 
    echo Third Job fashion palettes may not load.
    echo.
)

if not exist "src\nonremovable_assets\vanilla_pals\fashion" (
    echo WARNING: src\nonremovable_assets\vanilla_pals\fashion folder not found! 
    echo Default fashion palettes may not load.
    echo.
)

if not exist "src\nonremovable_assets\vanilla_pals\hair" (
    echo WARNING: src\nonremovable_assets\vanilla_pals\hair folder not found! 
    echo Default hair palettes may not load.
    echo.
)

if not exist "src\nonremovable_assets\icons" (
    echo WARNING: src\nonremovable_assets\icons folder not found! Icons may not export.
    echo.
)

REM Check for BMP and PAL folders in character folders
if not exist "src\nonremovable_assets\icons\chr001\BMP" ( echo WARNING: BMP folder missing in First Job Bunny! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr001\PAL" ( echo WARNING: PAL folder missing in First Job Bunny! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr002\BMP" ( echo WARNING: BMP folder missing in First Job Buffalo! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr002\PAL" ( echo WARNING: PAL folder missing in First Job Buffalo! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr003\BMP" ( echo WARNING: BMP folder missing in First Job Sheep! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr003\PAL" ( echo WARNING: PAL folder missing in First Job Sheep! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr004\BMP" ( echo WARNING: BMP folder missing in First Job Dragon! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr004\PAL" ( echo WARNING: PAL folder missing in First Job Dragon! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr005\BMP" ( echo WARNING: BMP folder missing in First Job Fox! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr005\PAL" ( echo WARNING: PAL folder missing in First Job Fox! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr006\BMP" ( echo WARNING: BMP folder missing in First Job Lion! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr006\PAL" ( echo WARNING: PAL folder missing in First Job Lion! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr007\BMP" ( echo WARNING: BMP folder missing in First Job Cat! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr007\PAL" ( echo WARNING: PAL folder missing in First Job Cat! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr008\BMP" ( echo WARNING: BMP folder missing in First Job Raccoon! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr008\PAL" ( echo WARNING: PAL folder missing in First Job Raccoon! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr009\BMP" ( echo WARNING: BMP folder missing in Second Job Bunny! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr009\PAL" ( echo WARNING: PAL folder missing in Second Job Bunny! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr010\BMP" ( echo WARNING: BMP folder missing in Second Job Buffalo! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr010\PAL" ( echo WARNING: PAL folder missing in Second Job Buffalo! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr011\BMP" ( echo WARNING: BMP folder missing in Second Job Sheep! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr011\PAL" ( echo WARNING: PAL folder missing in Second Job Sheep! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr012\BMP" ( echo WARNING: BMP folder missing in Second Job Dragon! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr012\PAL" ( echo WARNING: PAL folder missing in Second Job Dragon! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr013\BMP" ( echo WARNING: BMP folder missing in Second Job Fox! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr013\PAL" ( echo WARNING: PAL folder missing in Second Job Fox! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr014\BMP" ( echo WARNING: BMP folder missing in Second Job Lion! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr014\PAL" ( echo WARNING: PAL folder missing in Second Job Lion! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr015\BMP" ( echo WARNING: BMP folder missing in Second Job Cat! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr015\PAL" ( echo WARNING: PAL folder missing in Second Job Cat! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr016\BMP" ( echo WARNING: BMP folder missing in Second Job Raccoon! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr016\PAL" ( echo WARNING: PAL folder missing in Second Job Raccoon! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr017\BMP" ( echo WARNING: BMP folder missing in Third Job Bunny! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr017\PAL" ( echo WARNING: PAL folder missing in Third Job Bunny! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr018\BMP" ( echo WARNING: BMP folder missing in Third Job Buffalo! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr018\PAL" ( echo WARNING: PAL folder missing in Third Job Buffalo! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr019\BMP" ( echo WARNING: BMP folder missing in Third Job Sheep! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr019\PAL" ( echo WARNING: PAL folder missing in Third Job Sheep! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr020\BMP" ( echo WARNING: BMP folder missing in Third Job Dragon! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr020\PAL" ( echo WARNING: PAL folder missing in Third Job Dragon! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr021\BMP" ( echo WARNING: BMP folder missing in Third Job Fox! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr021\PAL" ( echo WARNING: PAL folder missing in Third Job Fox! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr022\BMP" ( echo WARNING: BMP folder missing in Third Job Lion! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr022\PAL" ( echo WARNING: PAL folder missing in Third Job Lion! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr023\BMP" ( echo WARNING: BMP folder missing in Third Job Cat! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr023\PAL" ( echo WARNING: PAL folder missing in Third Job Cat! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr024\BMP" ( echo WARNING: BMP folder missing in Third Job Raccoon! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr024\PAL" ( echo WARNING: PAL folder missing in Third Job Raccoon! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr025\BMP" ( echo WARNING: BMP folder missing in First Job Paula! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr025\PAL" ( echo WARNING: PAL folder missing in First Job Paula! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr026\BMP" ( echo WARNING: BMP folder missing in Second Job Paula! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr026\PAL" ( echo WARNING: PAL folder missing in Second Job Paula! Icon palette loading may fail. )
if not exist "src\nonremovable_assets\icons\chr027\BMP" ( echo WARNING: BMP folder missing in Third Job Paula! Icon exports may fail. )
if not exist "src\nonremovable_assets\icons\chr027\PAL" ( echo WARNING: PAL folder missing in Third Job Paula! Icon palette loading may fail. )
echo.

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

if not exist "exports\full_pals" (
    echo Creating exports\full_pals folder for full palette exports...
    mkdir "exports\full_pals" 2>nul
    echo.
)

REM Create settings.json if it doesn't exist
if not exist "src\settings.json" (
    echo Creating settings.json file...
    echo { > "src\settings.json"
    echo     "global": { >> "src\settings.json"
    echo         "use_bmp_export": true, >> "src\settings.json"
    echo         "use_portrait_export": true, >> "src\settings.json"
    echo         "cute_bg_option": "both", >> "src\settings.json"
    echo         "palette_format": "png", >> "src\settings.json"
    echo         "show_frame_labels": true, >> "src\settings.json"
    echo         "use_right_click": true, >> "src\settings.json"
    echo         "live_pal_ui_mode": "Simple", >> "src\settings.json"
    echo         "show_export_palette_button": false, >> "src\settings.json"
    echo         "show_dev_buttons": false, >> "src\settings.json"
    echo         "use_quick_export": false, >> "src\settings.json"
    echo         "zoom_level": "100%%", >> "src\settings.json"
    echo         "background_color": [255, 255, 255], >> "src\settings.json"
    echo         "dont_show_excess_colors_prompt": false, >> "src\settings.json"
    echo         "dont_show_all_mode_warning": false, >> "src\settings.json"
    echo         "dont_show_50_frames_warning": false, >> "src\settings.json"
    echo         "last_character": null, >> "src\settings.json"
    echo         "last_job": null, >> "src\settings.json"
    echo         "last_frame": 0, >> "src\settings.json"
    echo         "last_preview_mode": "single" >> "src\settings.json"
    echo     }, >> "src\settings.json"
    echo     "per_character": {} >> "src\settings.json"
    echo } >> "src\settings.json"
    echo Settings file created.
    echo.
)

echo Starting Fashion Previewer...
echo.
cd src
python launch_previewer.py 2>nul
set PYTHON_ERROR=%errorlevel%
cd ..

if %PYTHON_ERROR% NEQ 0 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python is not installed or not in PATH!
        echo Please install Python from https://python.org
        echo Make sure to check "Add to PATH" during installation.
        pause
        exit /b 1
    ) else (
    echo.
    echo ERROR: The application crashed or failed to start!
    echo This might be due to missing dependencies.
    echo Try running: pip install Pillow
    pause
    exit /b 1
    )
)
