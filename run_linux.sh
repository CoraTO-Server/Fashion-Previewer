#!/bin/bash
echo "Fashion Previewer Launcher"
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

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check and install required Python packages
echo "Checking Python dependencies..."

# Try to import PIL to check if Pillow is installed
if ! $PYTHON_CMD -c "import PIL" >/dev/null 2>&1; then
    echo "Installing Pillow package..."
    
    # First try pip/pip3
    if command_exists pip3; then
        pip3 install --user Pillow
    elif command_exists pip; then
        pip install --user Pillow
    # If pip fails or isn't found, try system package manager
    elif command_exists apt-get; then
        echo "Using apt to install Pillow..."
        sudo apt-get update && sudo apt-get install -y python3-pil
    elif command_exists dnf; then
        echo "Using dnf to install Pillow..."
        sudo dnf install -y python3-pillow
    elif command_exists yum; then
        echo "Using yum to install Pillow..."
        sudo yum install -y python3-pillow
    elif command_exists pacman; then
        echo "Using pacman to install Pillow..."
        sudo pacman -S --noconfirm python-pillow
    else
        echo "ERROR: Could not install Pillow!"
        echo "Please install Pillow manually using one of these commands:"
        echo "  pip3 install --user Pillow"
        echo "  sudo apt-get install python3-pil"
        echo "  sudo dnf install python3-pillow"
        echo "  sudo pacman -S python-pillow"
        read -p "Press Enter to exit..."
        exit 1
    fi
    
    # Check if installation was successful
    if ! $PYTHON_CMD -c "import PIL" >/dev/null 2>&1; then
        echo "ERROR: Failed to install Pillow package!"
        echo "Please try installing it manually using your system's package manager"
        echo "or pip: pip3 install --user Pillow"
        read -p "Press Enter to exit..."
        exit 1
    fi
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

if [ ! -d "src/nonremovable_assets/icons" ]; then
    echo "WARNING: src/nonremovable_assets/icons folder not found! Icons may not export."
    echo
fi

# Creating Export folders
for dir in "exports/custom_pals/fashion" "exports/custom_pals/hair" "exports/images" "exports/icons" "exports/colors/json" "exports/colors/icon"; do
    if [ ! -d "$dir" ]; then
        echo "Creating $dir folder for appropriate exporting..."
        mkdir -p "$dir"
        echo
    fi
done

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