#!/usr/bin/env python3
"""
Fashion Previewer Launcher
This script ensures the working directory is set correctly before launching the main application.
"""

import os
import sys
import subprocess

def main():
    # Get the directory where this launcher script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    print(f"Working directory set to: {os.getcwd()}")
    print("Launching Fashion Previewer...")
    
    # Check if the main script exists
    main_script = "fashionpreviewer_v2.2.py"
    if not os.path.exists(main_script):
        print(f"ERROR: {main_script} not found!")
        print(f"Make sure this launcher is in the same folder as {main_script}")
        input("Press Enter to exit...")
        return
    
    # Check if required folders exist
    required_folders = ["rawbmps", "pals"]
    missing_folders = []
    
    for folder in required_folders:
        if not os.path.exists(folder):
            missing_folders.append(folder)
    
    if missing_folders:
        print(f"WARNING: Missing required folders: {missing_folders}")
        print("The application may not work correctly without these folders.")
        print("Make sure you have the complete FashionPreviewer folder structure.")
        input("Press Enter to continue anyway...")
    
    try:
        # Run the main application
        print("Starting Fashion Previewer...")
        subprocess.run([sys.executable, main_script], check=True)
        print("Application closed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Application failed to start: {e}")
        print("This might be due to missing Python dependencies.")
        print("Try running: pip install Pillow")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
