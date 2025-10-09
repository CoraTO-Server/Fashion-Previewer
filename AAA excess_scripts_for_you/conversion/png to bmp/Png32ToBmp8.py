#!/usr/bin/env python3
"""
Convert all 32-bit PNGs (including subfolders) to 8-bit BMP (256 colors) and rename PNG folders to BMP

Usage:
  1. Double-click to run: Processes the current directory
  2. Command line: python png32_to_bmp8_recursive.py [input_dir] [output_dir]

If run without arguments (double-click), processes the current directory.
If run with only input_dir, the .bmp files will be created next to the original files.
Requires Pillow:
  pip install pillow

Notes:
 - Keeps subfolder structure (if output_dir is specified), otherwise saves .bmp in the same folder.
 - Handles alpha channel by compositing onto a magenta background (255, 0, 255) before quantization.
 - Uses PIL's median-cut quantization to produce a 256-color palette.
 - Automatically renames any folder named 'PNG' to 'BMP' (case insensitive).
"""

import os
import sys
from PIL import Image
import argparse


def convert_png_to_bmp8(in_path: str, out_path: str):
    """Convert a single PNG to 8-bit BMP (overwrite or save new file)."""
    try:
        im = Image.open(in_path)
    except Exception as e:
        print(f"Skipped: cannot open {in_path} -> {e}")
        return

    # If image has alpha, composite onto magenta background (255,0,255)
    if im.mode in ("RGBA", "LA") or ("transparency" in im.info):
        rgba = im.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (255, 0, 255, 255))
        bg.paste(rgba, mask=rgba.split()[3])  # use alpha as mask
        rgb = bg.convert("RGB")
    else:
        rgb = im.convert("RGB")

    # Quantize to 256 colors (median-cut method)
    try:
        pal = rgb.quantize(colors=256, method=Image.MEDIANCUT)
    except Exception:
        # Fallback for older Pillow versions
        pal = rgb.quantize(256)

    # Ensure output folder exists
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)

    try:
        pal.save(out_path, format='BMP')
        print(f"Done: {in_path} -> {out_path}")
    except Exception as e:
        print(f"Failed: cannot save {out_path} -> {e}")


def find_and_convert(root_dir: str, output_root: str = None):
    """Traverse root_dir and convert all PNGs to BMP.

    If output_root is provided, files are saved under output_root with the same relative paths.
    Otherwise, .bmp files are created in the same folders as the source PNGs.
    Additionally, any folder named 'PNG' will be renamed to 'BMP'.
    """
    root_dir = os.path.abspath(root_dir)
    if output_root:
        output_root = os.path.abspath(output_root)

    count = 0
    folder_renames = 0
    
    # We need to collect folders first because renaming during walk can affect traversal
    folders_to_rename = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # Collect PNG folders for renaming
        for dirname in dirnames:
            if dirname.upper() == "PNG":
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, "BMP")
                folders_to_rename.append((old_path, new_path))
                
        for fn in filenames:
            if fn.lower().endswith('.png'):
                in_path = os.path.join(dirpath, fn)

                # Determine output path
                rel = os.path.relpath(dirpath, root_dir)
                base_name = os.path.splitext(fn)[0] + '.bmp'
                if output_root:
                    out_dir = os.path.join(output_root, rel)
                    out_path = os.path.join(out_dir, base_name)
                else:
                    out_path = os.path.join(dirpath, base_name)

                convert_png_to_bmp8(in_path, out_path)
                count += 1
    
    # Rename folders after walking (to avoid affecting the walk)
    for old_path, new_path in reversed(folders_to_rename):  # Reverse to handle nested folders
        try:
            if os.path.exists(new_path):
                print(f"Warning: Cannot rename {old_path} to {new_path} - target already exists")
                continue
            os.rename(old_path, new_path)
            folder_renames += 1
            print(f"Renamed folder: {old_path} -> {new_path}")
        except Exception as e:
            print(f"Failed to rename folder {old_path}: {e}")

    print(f"Processed {count} PNG files and renamed {folder_renames} folders in total.")


def main():
    # If no arguments provided, use current directory
    if len(sys.argv) == 1:
        current_dir = os.getcwd()
        print(f"No directory specified, using current directory: {current_dir}")
        find_and_convert(current_dir)
        input("\nPress Enter to exit...")  # Keep window open
        return

    # Otherwise use command line arguments
    p = argparse.ArgumentParser(description='Convert all PNGs (including subfolders) to 8-bit BMP')
    p.add_argument('input_dir', help='Input folder (will be searched recursively)')
    p.add_argument('output_dir', nargs='?', default=None, help='Optional output root folder. If not provided, .bmp files will be created alongside source PNGs.')
    args = p.parse_args()

    if not os.path.isdir(args.input_dir):
        print('Error: input_dir is not a folder or does not exist.')
        sys.exit(1)

    find_and_convert(args.input_dir, args.output_dir)


if __name__ == '__main__':
    main()
