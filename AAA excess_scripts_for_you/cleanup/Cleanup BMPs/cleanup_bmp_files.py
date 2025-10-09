#!/usr/bin/env python3
"""
One-click recursive BMP cleanup script for Fashion-Previewer project.

This script will:
- Rename all folders named "BMP" to "PNG" (case-insensitive)
- Delete all .bmp files throughout the project
- Work recursively from the project root directory

Usage: Double-click this file or run: python cleanup_bmp_files.py
"""

import os
import sys
from pathlib import Path

def rename_bmp_folders(base: Path):
    """Rename folders named BMP -> PNG recursively."""
    print("🔍 Searching for BMP folders...")
    folders_renamed = 0
    
    # Get all directories, sorted by depth (deepest first) to avoid path conflicts
    all_dirs = [p for p in base.rglob("*") if p.is_dir()]
    all_dirs.sort(key=lambda p: -len(str(p)))
    
    for folder in all_dirs:
        if folder.name.lower() == "bmp":
            new_path = folder.with_name("PNG")
            try:
                folder.rename(new_path)
                print(f"📂 Renamed folder: {folder.relative_to(base)} -> PNG")
                folders_renamed += 1
            except Exception as e:
                print(f"⚠️  Could not rename {folder.relative_to(base)}: {e}")
    
    if folders_renamed == 0:
        print("✅ No BMP folders found to rename.")
    else:
        print(f"✅ Renamed {folders_renamed} BMP folder(s) to PNG.")

def delete_bmp_files(base: Path):
    """Delete all .bmp files recursively."""
    print("\n🔍 Searching for BMP files...")
    files_deleted = 0
    
    for bmp_file in base.rglob("*.bmp"):
        try:
            bmp_file.unlink()
            print(f"🗑️  Deleted: {bmp_file.relative_to(base)}")
            files_deleted += 1
        except Exception as e:
            print(f"⚠️  Could not delete {bmp_file.relative_to(base)}: {e}")
    
    if files_deleted == 0:
        print("✅ No BMP files found to delete.")
    else:
        print(f"✅ Deleted {files_deleted} BMP file(s).")

def main():
    # Get the project root directory (where this script is located)
    script_dir = Path(__file__).parent.absolute()
    
    print("=" * 60)
    print("🧹 BMP Cleanup Script for Fashion-Previewer")
    print("=" * 60)
    print(f"📍 Working directory: {script_dir}")
    print()
    
    # Confirm with user before proceeding
    try:
        response = input("⚠️  This will rename BMP folders to PNG and DELETE all .bmp files.\nContinue? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("❌ Operation cancelled.")
            return
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")
        return
    
    print("\n🚀 Starting cleanup...")
    
    # Step 1: Rename BMP folders to PNG
    rename_bmp_folders(script_dir)
    
    # Step 2: Delete all BMP files
    delete_bmp_files(script_dir)
    
    print("\n" + "=" * 60)
    print("✅ Cleanup completed successfully!")
    print("=" * 60)
    
    # Keep window open on Windows if double-clicked
    if sys.platform.startswith('win') and not sys.stdin.isatty():
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
