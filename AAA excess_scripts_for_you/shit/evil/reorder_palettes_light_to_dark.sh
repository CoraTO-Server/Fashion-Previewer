#!/bin/bash
# Sort RIFF palette colors from brightest to darkest
# This shell script runs the Python script

echo
echo "==============================================="
echo " Palette Color Sorter (Light to Dark)"
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

# Run the Python script (no external dependencies needed)
$PYTHON_CMD reorder_palettes_light_to_dark.py "$@"

echo
echo "Press Enter to exit..."
read
