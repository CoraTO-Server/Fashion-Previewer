#!/bin/bash
# Convert BMPs to PNGs with black transparency
# This shell script runs the Python script

echo
echo "==============================================="
echo " BMP to PNG Converter (Black Transparency)"
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
    echo "Installing required package: Pillow"
    $PYTHON_CMD -m pip install --user Pillow
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Pillow. Please run install_dependencies.sh first."
        exit 1
    fi
fi

# Run the Python script
$PYTHON_CMD convert_bmp_png_blk.py "$@"

echo
echo "Press Enter to exit..."
read
