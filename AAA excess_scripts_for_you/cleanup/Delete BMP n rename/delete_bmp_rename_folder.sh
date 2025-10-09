#!/bin/bash
# One-click BMP folder renamer and cleanup
# This shell script runs the Python script

echo
echo "==============================================="
echo " BMP Folder Renamer and Cleanup"
echo "==============================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python and try again."
    exit 1
fi

# Use python3 if available, otherwise fall back to python
if command -v python3 &> /dev/null; then
    python3 delete_bmp_rename_folder.py
else
    python cleanup_bmp_files.py
fi

echo
echo "Press Enter to exit..."
read
