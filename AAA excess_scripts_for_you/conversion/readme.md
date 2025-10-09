# Conversion Scripts

Scripts for converting between image formats and managing palettes.

## Scripts

### 8bitbmp-to-palette.py
- **Purpose**: Convert 8-bit BMPs to RIFF palette files
- **Dependencies**: Pillow (PIL)
- **Usage**: `python 8bitbmp-to-palette.py [input.bmp]`

### convert_bmp_png_blk.py
- **Purpose**: Convert BMPs to PNGs with black (#000000) transparency
- **Dependencies**: Pillow (PIL)
- **Usage**: `python convert_bmp_png_blk.py [input.bmp]`

### convert_bmp_png_mag.py
- **Purpose**: Convert BMPs to PNGs with magenta (#FF00FF) transparency
- **Dependencies**: Pillow (PIL)
- **Usage**: `python convert_bmp_png_mag.py [input.bmp]`

### make_palettes_v2.py
- **Purpose**: Generate palettes with advanced options
- **Dependencies**: Pillow (PIL), numpy
- **Usage**: Run through make_palettes.bat

### Png32ToBmp8.py
- **Purpose**: Convert 32-bit PNGs to 8-bit BMPs
- **Dependencies**: Pillow (PIL)
- **Usage**: `python Png32ToBmp8.py [input.png]`

## Dependencies
Required Python packages:
```bash
pip install Pillow    # For all image processing
pip install numpy     # For make_palettes_v2.py only
```

Or run the provided installer:
- Windows: `install_dependencies.bat`
- Linux: `install_dependencies.sh`
