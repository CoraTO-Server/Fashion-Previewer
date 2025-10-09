# Utility Scripts

This folder contains various utility scripts organized by function. Each subfolder has its own readme
    and Windows+Linux click-to-run scripts, in case you need those, too. **Most** of these are:
        - Recursive (check the folders inside the folder you're in and the ones below it)
        - Click-to-run (don't require you to input text to complete)

## Folder Contents

### 1. Cleanup Scripts (`cleanup/`)
Scripts for cleaning up and managing BMP/PNG files
- See `cleanup/readme.md` for details

### 2. Conversion Scripts (`conversion/`)
Scripts for converting between different image formats and creating palettes
- See `conversion/readme.md` for details

### 3. Palette Management (`shit/`)
Scripts for managing and reordering palettes. This is an evil system that caused many bugs for us.
    Now it's yours.
- See `shit/readme.md` for details

## Quick Start
1. Choose the folder with the scripts you need
2. Run the appropriate start-up script for your OS
3. Follow the folder's readme for usage instructions

## Global Dependencies Overview

### Cleanup Scripts
- No external dependencies (uses built-in Python modules only)
- Safe to run without installation

### Conversion Scripts
- Requires Pillow (PIL) for image processing
- Requires numpy for palette generation (make_palettes_v2.py only)
- Dependency installers provided

### Palette Management
- No external dependencies (uses built-in Python modules only)
- Safe to run without installation