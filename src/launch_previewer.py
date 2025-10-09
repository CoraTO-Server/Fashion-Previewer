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
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_script = os.path.join(script_dir, "fashionpreviewer.py")
    
    # Set root_dir as a global variable
    os.environ["FASHION_PREVIEWER_ROOT"] = root_dir

    # Change to the root directory
    os.chdir(root_dir)

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)  # More explicit parent directory handling
    
    # Define base paths
    nonremovable_dir = os.path.join(script_dir, "nonremovable_assets")
    
    # Build required folder paths
    required_folders = [
        os.path.join(script_dir, "rawbmps"),
        os.path.join(nonremovable_dir, "vanilla_pals"),
        os.path.join(nonremovable_dir, "icons")
    ]
    missing_folders = []

    # Check each path
    for folder in required_folders:
        if not os.path.exists(os.path.abspath(folder)):
            missing_folders.append(folder)

    if missing_folders:
        print(f"WARNING: Missing required folders: {missing_folders}")
        print("The application may not work correctly without these folders.")
        print("Make sure you have the complete FashionPreviewer folder structure.")
        input("Press Enter to continue anyway...")
    
    # Check for BMP and PAL folders in icons directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons_dir = os.path.join(script_dir, "nonremovable_assets", "icons")
    if os.path.exists(icons_dir):
        bmp_folders_missing = False
        pal_folders_missing = False
        for chr_folder in os.listdir(icons_dir):
            chr_path = os.path.join(icons_dir, chr_folder)
            if chr_folder.startswith("chr") and os.path.isdir(chr_path):
                bmp_path = os.path.join(chr_path, "BMP")
                pal_path = os.path.join(chr_path, "PAL")
                if not os.path.exists(bmp_path):
                    print(f"WARNING: BMP folder missing in {chr_folder}! Icon exports may fail.")
                    bmp_folders_missing = True
                if not os.path.exists(pal_path):
                    print(f"WARNING: PAL folder missing in {chr_folder}! Icon palette loading may fail.")
                    pal_folders_missing = True
        if bmp_folders_missing:
            print("Some character icon BMP folders are missing. Icons may not export properly.")
            print("Make sure you have the complete icon BMP files for all characters.")
        if pal_folders_missing:
            print("Some character icon PAL folders are missing. Icon palettes may not load properly.")
            print("Make sure you have the complete icon PAL files for all characters.")

    # Create export directories if they don't exist
    # Define base export paths
    exports_dir = os.path.join(root_dir, "exports")
    custom_pals_dir = os.path.join(exports_dir, "custom_pals")
    colors_dir = os.path.join(exports_dir, "colors")
    
    # Build export folder paths
    export_folders = [
        os.path.join(exports_dir, "images"),
        os.path.join(custom_pals_dir, "fashion"),
        os.path.join(custom_pals_dir, "hair"),
        os.path.join(exports_dir, "icons"),
        os.path.join(colors_dir, "json"),
        os.path.join(colors_dir, "icon"),
        os.path.join(exports_dir, "full_pals")
    ]
    
    # Create each directory
    for folder_path in export_folders:
        if not os.path.exists(os.path.abspath(folder_path)):
            try:
                os.makedirs(folder_path, exist_ok=True)
                print(f"Created export directory: {os.path.relpath(folder_path, root_dir)}")
            except Exception as e:
                print(f"WARNING: Could not create {os.path.relpath(folder_path, root_dir)}: {e}")

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
    
    # Create settings.json if it doesn't exist
    settings_path = os.path.join(script_dir, "settings.json")
    if not os.path.exists(settings_path):
        import json
        print(f"Settings file missing! Making settings file...")
        default_settings = {
            'global': {
                'use_bmp_export': True,
                'use_portrait_export': True,
                'cute_bg_option': 'both',
                'palette_format': 'png',
                'show_frame_labels': True,
                'use_right_click': True,
                'live_pal_ui_mode': 'Simple',
                'show_export_palette_button': False,
                'show_dev_buttons': False,
                'use_quick_export': False,
                'zoom_level': '100%',
                'background_color': [255, 255, 255],
                'dont_show_excess_colors_prompt': False,
                'dont_show_all_mode_warning': False,
                'dont_show_50_frames_warning': False,
                'last_character': None,
                'last_job': None,
                'last_frame': 0,
                'last_preview_mode': 'single'
            },
            'per_character': {}
        }
        try:
            with open(settings_path, 'w') as f:
                json.dump(default_settings, f, indent=4)
            print("Created settings.json file")
        except Exception as e:
            print(f"WARNING: Could not create settings.json: {e}")

    try:
        # Run the main application from the src directory
        print("Starting Fashion Previewer...")
        os.chdir(script_dir)  # Change to src directory to run the main script
        subprocess.run([sys.executable, main_script], check=True)
        os.chdir(root_dir)  # Change back to root directory
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
