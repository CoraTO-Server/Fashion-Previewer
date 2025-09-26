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
    root_dir = os.path.dirname(script_dir)
    main_script = os.path.join(script_dir, "fashionpreviewer.py")
    
    # Set root_dir as a global variable
    os.environ["FASHION_PREVIEWER_ROOT"] = root_dir

    # Change to the script directory
    os.chdir(script_dir)

    print(f"Working directory set to: {os.getcwd()}")
    print("Launching Fashion Previewer...")

    # Check required launcher files
    required_files = [
        os.path.join(root_dir, "run_linux.sh"),
        os.path.join(root_dir, "run_windows.bat"),
        os.path.join(script_dir, "fashionpreviewer.py"),
        os.path.join(script_dir, "icon_handler.py"),
        os.path.join(script_dir, "palette_ranges.py")
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            filename = os.path.basename(file_path)
            print(f"ERROR: Required file {filename} is missing!")
            print("Please redownload the repository and try again.")
            input("Press Enter to exit...")
            return

    # Check if required folders exist
    required_folders = ["rawbmps", "nonremovable_assets/vanilla_pals", "nonremovable_assets/icons"]
    missing_folders = []

    for folder in required_folders:
        if not os.path.exists(os.path.join(script_dir, folder)):
            missing_folders.append(folder)

    if missing_folders:
        print(f"WARNING: Missing required folders: {missing_folders}")
        print("The application may not work correctly without these folders.")
        print("Make sure you have the complete FashionPreviewer folder structure.")
        input("Press Enter to continue anyway...")

    # Create export directories if they don't exist
    # root_dir was already defined at the start of main()
    export_folders = ["exports/images", "exports/custom_pals/fashion", "exports/custom_pals/hair", "exports/icons", "exports/colors/json", "exports/colors/icon"]
    for folder in export_folders:
        folder_path = os.path.join(root_dir, folder)
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"Created export directory: {folder}")
            except Exception as e:
                print(f"WARNING: Could not create {folder}: {e}")

    # Create statistics.json if it doesn't exist
    stats_path = os.path.join(script_dir, "statistics.json")
    if not os.path.exists(stats_path):
        import json, time
        print(f"Statistics file missing! Making stats file...")
        default_stats = {
            'live_palette_files_edited': [],
            'live_palette_files_saved': [],
            'icons_edited': [],
            'icons_saved': [],
            'frames_previewed': 0,
            'frames_skipped': 0,
            'start_time': time.time(),
            'character_edits': {},
            'exported_frames': 0,
            'exported_backgrounds': 0,
            'exported_palettes': {},
            'colors_saved': 0,
            'indexes_changed': 0,
            'indexes_selected': 0,
            'indexes_saved_in_pals': 0,
            'colors_saved_in_json': 0,
            'preview_indexes_selected': {'live_pal': 0, 'live_icon': 0},
            'palettes_previewed': 0
        }
        try:
            with open(stats_path, 'w') as f:
                json.dump(default_stats, f, indent=4)
            print("Created statistics.json file")
        except Exception as e:
            print(f"WARNING: Could not create statistics.json: {e}")

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
