#!/bin/bash
echo "+------------------------------------------------+"
echo "[               Fashion                          ]"
echo "[                   Previewer                    ]"
echo "[                       Launcher                 ]"
echo "+------------------------------------------------+"
echo 
echo "Lovingly made by:"
echo "KusangiKyo, Dino, Yuki, and Mewsie."
echo
echo "From CoraTO, on behalf of the Trickster community."
echo "Thank you for everything :3"
echo 
echo "+------------------------------------------------+"
echo

# Change to the directory where this script is located
cd "$(dirname "$0")"

echo "Working directory: $(pwd)"
echo

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Check if python is version 3.x
    ver=$(python -c 'import sys; print(sys.version_info[0])')
    if [ "$ver" -eq "3" ]; then
        PYTHON_CMD="python"
    else
        echo "ERROR: Python 3.x is required but Python 2.x was found!"
        echo "The Fashion Previewer uses modern Python features that require version 3.x"
        echo "Please install Python3 using your package manager (e.g. apt install python3)"
        echo "After installing Python3, try running this script again."
        read -p "Press Enter to exit..."
        exit 1
    fi
else
    echo "ERROR: Python3 is not installed or not in PATH!"
    echo "Please install Python3 using your package manager (e.g. apt install python3)"
    echo "After installing Python3, try running this script again."
    read -p "Press Enter to exit..."
    exit 1
fi

# Install/Update pip if needed
echo "Setting up pip..."

# Try to detect pip3 availability
if ! command -v pip3 >/dev/null 2>&1; then
    echo "pip3 not found, attempting to install it..."

    # Detect distribution and install pip accordingly
    if [ -f /etc/arch-release ]; then
        echo "Detected Arch Linux. Installing pip via pacman..."
        sudo pacman -S --noconfirm python-pip || {
            echo "ERROR: pip install failed via pacman!"
            exit 1
        }
    elif [ -f /etc/debian_version ]; then
        echo "Detected Debian-based distro. Installing pip via apt..."
        sudo apt update && sudo apt install -y python3-pip || {
            echo "ERROR: pip install failed via apt!"
            exit 1
        }
    elif [ -f /etc/fedora-release ]; then
        echo "Detected Fedora. Installing pip via dnf..."
        sudo dnf install -y python3-pip || {
            echo "ERROR: pip install failed via dnf!"
            exit 1
        }
    else
        echo "ERROR: Unsupported distribution or pip not available!"
        echo "Please manually install pip using your system's package manager."
        read -p "Press Enter to exit..."
        exit 1
    fi
else
    echo "pip3 is already installed."
fi

$PYTHON_CMD -m pip install --upgrade pip >/dev/null 2>&1
# Verify pip works by trying to use it
$PYTHON_CMD -m pip --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Pip is not working properly. Please try:"
    echo "1. Run this script with sudo: sudo ./$(basename $0)"
    echo "2. After pip installs, you can run normally without sudo"
    echo
    echo "Alternative methods:"
    echo "Use your system's package manager:"
    echo "   sudo apt install python3-pip    # For Debian/Ubuntu"
    echo "   sudo dnf install python3-pip    # For Fedora"
    echo "   sudo pacman -S python-pip       # For Arch"
    read -p "Press Enter to exit..."
    exit 1
fi
echo "Pip setup complete."

# Check if Pillow is installed
echo "Checking for required dependencies..."
$PYTHON_CMD -c "import PIL" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing Pillow..."
    $PYTHON_CMD -m pip install Pillow >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Pillow! Please try:"
        echo "1. Run this script with sudo: sudo ./$(basename $0)"
        echo "2. After Pillow installs, you can run normally without sudo"
        echo
        echo "Alternative methods:"
        echo "Use your system's package manager:"
        echo "   sudo apt install python3-pil    # For Debian/Ubuntu"
        echo "   sudo dnf install python3-pillow # For Fedora"
        echo "   sudo pacman -S python-pillow    # For Arch"
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "Pillow installed successfully."
else
    echo "Pillow is installed."
fi

# Check if required Python files exist
cd src
for file in launch_previewer.py fashionpreviewer.py icon_handler.py palette_ranges.py; do
    if [ ! -f "$file" ]; then
        echo "Error: $file not found!"
        echo "Please redownload the repository and try again."
        cd ..
        read -p "Press Enter to exit..."
        exit 1
    fi
done
cd ..

# Check if required folders exist
if [ ! -d "src/rawbmps" ]; then
    echo "WARNING: src/rawbmps folder not found! Character images may not load."
    echo
fi

if [ ! -d "src/nonremovable_assets/vanilla_pals" ]; then
    echo "WARNING: src/nonremovable_assets/vanilla_pals folder not found! Fashion palettes may not load."
    echo
fi

if [ ! -d "src/nonremovable_assets/vanilla_pals/3rd_default_fashion" ]; then
    echo "WARNING: src/nonremovable_assets/vanilla_pals/3rd_default_fashion folder not found!"
    echo "Third Job fashion palettes may not load."
    echo
fi

if [ ! -d "src/nonremovable_assets/vanilla_pals/fashion" ]; then
    echo "WARNING: src/nonremovable_assets/vanilla_pals/fashion folder not found!"
    echo "Default fashion palettes may not load."
    echo
fi

if [ ! -d "src/nonremovable_assets/vanilla_pals/hair" ]; then
    echo "WARNING: src/nonremovable_assets/vanilla_pals/hair folder not found!"
    echo "Default hair palettes may not load."
    echo
fi

if [ ! -d "src/nonremovable_assets/icons" ]; then
    echo "WARNING: src/nonremovable_assets/icons folder not found! Icons may not export."
    echo
else
    # Check for BMP and PAL folders in character folders
    if [ ! -d "src/nonremovable_assets/icons/chr001/BMP" ]; then echo "WARNING: BMP folder missing in First Job Bunny! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr001/PAL" ]; then echo "WARNING: PAL folder missing in First Job Bunny! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr002/BMP" ]; then echo "WARNING: BMP folder missing in First Job Buffalo! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr002/PAL" ]; then echo "WARNING: PAL folder missing in First Job Buffalo! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr003/BMP" ]; then echo "WARNING: BMP folder missing in First Job Sheep! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr003/PAL" ]; then echo "WARNING: PAL folder missing in First Job Sheep! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr004/BMP" ]; then echo "WARNING: BMP folder missing in First Job Dragon! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr004/PAL" ]; then echo "WARNING: PAL folder missing in First Job Dragon! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr005/BMP" ]; then echo "WARNING: BMP folder missing in First Job Fox! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr005/PAL" ]; then echo "WARNING: PAL folder missing in First Job Fox! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr006/BMP" ]; then echo "WARNING: BMP folder missing in First Job Lion! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr006/PAL" ]; then echo "WARNING: PAL folder missing in First Job Lion! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr007/BMP" ]; then echo "WARNING: BMP folder missing in First Job Cat! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr007/PAL" ]; then echo "WARNING: PAL folder missing in First Job Cat! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr008/BMP" ]; then echo "WARNING: BMP folder missing in First Job Raccoon! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr008/PAL" ]; then echo "WARNING: PAL folder missing in First Job Raccoon! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr009/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Bunny! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr009/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Bunny! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr010/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Buffalo! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr010/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Buffalo! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr011/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Sheep! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr011/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Sheep! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr012/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Dragon! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr012/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Dragon! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr013/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Fox! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr013/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Fox! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr014/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Lion! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr014/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Lion! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr015/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Cat! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr015/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Cat! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr016/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Raccoon! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr016/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Raccoon! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr017/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Bunny! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr017/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Bunny! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr018/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Buffalo! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr018/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Buffalo! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr019/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Sheep! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr019/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Sheep! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr020/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Dragon! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr020/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Dragon! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr021/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Fox! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr021/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Fox! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr022/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Lion! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr022/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Lion! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr023/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Cat! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr023/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Cat! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr024/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Raccoon! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr024/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Raccoon! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr025/BMP" ]; then echo "WARNING: BMP folder missing in First Job Paula! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr025/PAL" ]; then echo "WARNING: PAL folder missing in First Job Paula! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr026/BMP" ]; then echo "WARNING: BMP folder missing in Second Job Paula! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr026/PAL" ]; then echo "WARNING: PAL folder missing in Second Job Paula! Icon palette loading may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr027/BMP" ]; then echo "WARNING: BMP folder missing in Third Job Paula! Icon exports may fail."; fi
    if [ ! -d "src/nonremovable_assets/icons/chr027/PAL" ]; then echo "WARNING: PAL folder missing in Third Job Paula! Icon palette loading may fail."; fi
    echo
fi

# Creating Export folders
for dir in "exports/custom_pals/fashion" "exports/custom_pals/hair" "exports/images" "exports/icons" "exports/colors/json" "exports/colors/icon" "exports/full_pals"; do
    if [ ! -d "$dir" ]; then
        echo "Creating $dir folder for appropriate exporting..."
        mkdir -p "$dir"
        echo
    fi
done

# Create settings.json if it doesn't exist
if [ ! -f "src/settings.json" ]; then
    echo "Creating settings.json file..."
    cat > "src/settings.json" << 'EOF'
{
    "global": {
        "use_bmp_export": true,
        "use_portrait_export": true,
        "cute_bg_option": "both",
        "palette_format": "png",
        "show_frame_labels": true,
        "use_right_click": true,
        "live_pal_ui_mode": "Simple",
        "show_export_palette_button": false,
        "show_dev_buttons": false,
        "use_quick_export": false,
        "zoom_level": "100%",
        "background_color": [255, 255, 255],
        "dont_show_excess_colors_prompt": false,
        "dont_show_all_mode_warning": false,
        "dont_show_50_frames_warning": false,
        "last_character": null,
        "last_job": null,
        "last_frame": 0,
        "last_preview_mode": "single"
    },
    "per_character": {}
}
EOF
    echo "Settings file created."
    echo
fi

echo "Starting Fashion Previewer..."
echo
cd src
$PYTHON_CMD launch_previewer.py
cd ..

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: The application crashed or failed to start!"
    echo "This might be due to missing dependencies."
    echo "Try running: pip3 install Pillow"
    read -p "Press Enter to exit..."
    exit 1
fi
