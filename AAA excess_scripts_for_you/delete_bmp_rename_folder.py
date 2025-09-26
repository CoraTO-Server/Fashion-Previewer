#!/usr/bin/env python3
"""
Recursive folder and file cleanup:
- Renames all folders named "BMP" -> "PNG"
- Deletes all .bmp files in the tree
"""

import os
from pathlib import Path

def rename_bmp_folders(base: Path):
    """Rename folders named BMP -> PNG recursively."""
    for folder in sorted(base.rglob("*"), key=lambda p: -len(str(p))):  
        # sort deepest first, so renames don’t interfere with traversal
        if folder.is_dir() and folder.name.lower() == "bmp":
            new_path = folder.with_name("PNG")
            try:
                folder.rename(new_path)
                print(f"📂 Renamed folder: {folder} -> {new_path}")
            except Exception as e:
                print(f"⚠ Could not rename {folder}: {e}")

def delete_bmp_files(base: Path):
    """Delete all .bmp files recursively."""
    for bmp_file in base.rglob("*.bmp"):
        try:
            bmp_file.unlink()
            print(f"🗑️ Deleted file: {bmp_file}")
        except Exception as e:
            print(f"⚠ Could not delete {bmp_file}: {e}")

def main():
    base = Path(__file__).parent
    print(f"🔍 Scanning in: {base}")

    rename_bmp_folders(base)
    delete_bmp_files(base)

    print("✅ Done!")

if __name__ == "__main__":
    main()
