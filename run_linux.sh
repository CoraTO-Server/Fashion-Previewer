#!/bin/bash
echo "Fashion Previewer Launcher"
echo

# Change to the directory where this script is located
cd "$(dirname "$0")" || exit 1

echo "Working directory: $(pwd)"
echo

# Check if Python is installed
if ! command -v python >/dev/null 2>&1; then
    echo "ERROR: Python is not installed or not in PATH!"
    echo "Please install Python (e.g. sudo pacman -S python  OR  sudo apt install python3)"
    echo "After installing Python, restart your terminal and try again."
    exit 1
fi

# Check if src folder exists
if [ ! -d "src" ]; then
    echo "ERROR: src folder not found!"
    echo "Make sure this script is in the same folder as the src folder"
    exit 1
fi

# Check if the launcher script exists
if [ ! -f "src/launch_previewer.py" ]; then
    echo "ERROR: src/launch_previewer.py not found!"
    echo "Make sure launch_previewer.py is in the src folder"
    exit 1
fi

# Check if the main script exists
if [ ! -f "src/fashionpreviewer.py" ]; then
    echo "ERROR: src/fashionpreviewer.py not found!"
    echo "Make sure fashionpreviewer.py is in the src folder"
    exit 1
fi

# Check if required folders exist
if [ ! -d "src/rawbmps" ]; then
    echo "WARNING: src/rawbmps folder not found! Character images may not load."
    echo
fi

if [ ! -d "src/vanilla_pals" ]; then
    echo "WARNING: src/vanilla_pals folder not found! Fashion palettes may not load."
    echo
fi

# Create src/custom_pals if it doesn't exist
if [ ! -d "exports/custom_pals" ]; then
    echo "Creating src/exports/custom_pals folder for custom palettes..."
    mkdir -p "exports/custom_pals"
    echo
fi

if [ ! -d "exports/images" ]; then
    echo "Creating exports/images folder for custom images..."
    mkdir -p "exports/images"
    echo
fi

echo "Starting Fashion Previewer..."
echo
cd src
python launch_previewer.py
cd ..
status=$?

if [ $status -ne 0 ]; then
    echo
    echo "ERROR: The application crashed or failed to start!"
    echo "This might be due to missing dependencies."
    echo "Try running: pip install Pillow"
    exit $status
fi
