#!/usr/bin/env python3
"""
Recursive BMP -> PNG converter with black (#000000) keyed out.
- Scans the folder it's placed in (recursively).
- Converts all BMPs to PNG with transparency.
- Saves PNGs alongside the originals.
"""

import sys
from pathlib import Path
from PIL import Image

def convert_bmp_to_png(bmp_path: Path):
    """Convert a BMP to a PNG with black transparency."""
    img = Image.open(bmp_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        # Check if pixel is pure black (0,0,0)
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((0, 0, 0, 0))  # fully transparent
        else:
            new_data.append(item)
    img.putdata(new_data)

    out_path = bmp_path.with_suffix(".png")
    img.save(out_path, "PNG")
    print(f"✔ Converted: {bmp_path.name} -> {out_path.name}")

def main():
    # Base folder = script location
    base = Path(__file__).parent
    print(f"🔍 Searching for BMP files in: {base}")

    bmp_files = list(base.rglob("*.bmp"))
    if not bmp_files:
        print("No BMP files found.")
        return

    for bmp in bmp_files:
        try:
            convert_bmp_to_png(bmp)
        except Exception as e:
            print(f"⚠ Failed on {bmp}: {e}")

    print("✅ Done converting all BMPs!")

if __name__ == "__main__":
    main()
