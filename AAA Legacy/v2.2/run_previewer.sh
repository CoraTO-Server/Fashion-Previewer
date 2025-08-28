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

# Check if the launcher script exists
if [ ! -f "launch_previewer.py" ]; then
    echo "ERROR: launch_previewer.py not found!"
    echo "Make sure this script is in the same folder as launch_previewer.py"
    exit 1
fi

# Check if the main script exists
if [ ! -f "fashionpreviewer_v2.2.py" ]; then
    echo "ERROR: fashionpreviewer_v2.2.py not found!"
    echo "Make sure this script is in the same folder as fashionpreviewer_v2.2.py"
    exit 1
fi

# Check if required folders exist
if [ ! -d "rawbmps" ]; then
    echo "WARNING: rawbmps folder not found! Character images may not load."
    echo
fi

if [ ! -d "pals" ]; then
    echo "WARNING: pals folder not found! Fashion palettes may not load."
    echo
fi

echo "Starting Fashion Previewer..."
echo
python launch_previewer.py
status=$?

if [ $status -ne 0 ]; then
    echo
    echo "ERROR: The application crashed or failed to start!"
    echo "This might be due to missing dependencies."
    echo "Try running: pip install Pillow"
    exit $status
fi
