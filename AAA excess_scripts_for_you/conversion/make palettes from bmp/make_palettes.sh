#!/bin/bash
# Generate palettes with advanced options
# This shell script runs the Python script with dependency checks

echo
echo "==============================================="
echo " Advanced Palette Generator"
echo "==============================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python and try again."
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Check for Pillow
if ! $PYTHON_CMD -c "import PIL" &> /dev/null; then
    echo "Installing required package: Pillow..."
    $PYTHON_CMD -m pip install --quiet Pillow >/dev/null 2>&1
    if [ $? -ne 0 ]; then
            echo "ERROR: Failed to install Pillow. Try running with sudo."
            exit 1
    fi
fi

# Check for numpy
if ! $PYTHON_CMD -c "import numpy" &> /dev/null; then
    echo "Installing required package: numpy..."
    $PYTHON_CMD -m pip install --quiet numpy >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install numpy. Try running with sudo."
        exit 1
    fi
fi

# Run the Python script
echo "Running palette generator..."
$PYTHON_CMD make_palettes_v2.py "$@"

echo
echo "Palette generation complete!"
echo "Press Enter to exit..."
read
