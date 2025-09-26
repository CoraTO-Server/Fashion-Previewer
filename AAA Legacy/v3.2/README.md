# Fashion Previewer v3.2

A Python application for previewing and customizing character fashion using palette files.
Now including Linux Support!

# PLEASE READ THE LICENSE BEFORE USING THIS PROGRAM

## Please Note:

Our license may appear excessive, political, or restrictive at first glance,
	but it serves a clear purpose. It is not about vendettas; it is about
	boundaries. We will not tolerate mistreatment of our staff, our community,
	our leadership, our love, or our effort. What we’ve built is carried by
	care, and it deserves to be protected.

This project is not born from spite, but from redemption. It is for the
	players who were abandoned by greed, corruption, and neglect. It is for
	those who were outcast, forgotten, or left behind. The developers who never
	stood a chance without the resources and manpower we now provide.

	We fully intend to break that cycle. The only question is:
	
	Will you stand with us, or continue the pattern?

## Credits

This was made possible by the following players:
- KusanagiKyo
- Dino
- Yuki
- Mewsie

Thank you for your hard work and contributions to bring this tool to life for the community!!!

## [Join our Trickster Development Discord and get a central repository for live support, tools, information, updates on releases, and more!](https://discord.gg/d6h8brNwYY)

![PalEditor](https://github.com/CoraTO-Server/Fashion-Previewer/blob/main/AAA%20TUTORIALS/paleditor.gif)

## Features

- **Character Selection:** Choose from different characters and jobs
- **Fashion Customization:** Apply different fashion palettes
- **Hair Customization:** Apply different hair palettes
- **3rd Job Base Fashion:** Special handling for 3rd job characters
- **Custom Palettes:** Add your own custom palettes in `exports/custom_pals/`
- **Export Options:** Export as transparent PNG, backgrounded BMP, or combined palette
- **Multiple Preview Modes:** Single frame, all frames, or a custom range
- **Live Pal Editing**: Single or multiple indexes with sliders and saved colors
- **Key Commands**: Commands to make your life simple and efficient!

### Keyboard Shortcuts

Quick Actions:
- **B**: Change background color
- **E**: Export with current options
- **Shift+E**: Export all frames
- **O**: Open custom frame options
- **P**: Open palette editor
- **Shift+P**: Export palette
- **R**: Reset to original
- **D**: Debug info
- **V**: Toggle view mode (single/custom)


## Custom Palette Format

- **Fashion palettes:** `chr###_w#.pal` (e.g., `chr001_w47.pal`)
- **Hair palettes:** `chr###_#.pal` (e.g., `chr001_5.pal`)
- Place custom palettes in the `exports/custom_pals/` folder

## Quick Start

### For Windows Users:
1. Install Python 3.7+ from [python.org](https://python.org)
2. Type "Environment" in Windows Start search and Add the location of the
   Python folder to your "Paths"
3. Restart
4. Open terminal/command prompt in the folder & run `pip install Pillow`
5. **Double-click `run_previewer.bat`** to start the application
   - This will automatically check for Python and required folders
   - If you get dependency errors, run: `pip install Pillow`
   - If you're on the version WITHOUT the bat/launcher, then type in the
      terminal `py fashionpreviewer.py`

### For Linux:
1. Install Python 3.7+ from [python.org](https://python.org)
2. Open terminal/command prompt in the folder & run `pip install pillow`
3. Double-left click `run_previewer.sh` or run in the
   terminal `python launch_previewer.py`


### For Other Operating Systems:
1. Install Python 3.7+ from [python.org](https://python.org)
2. Open terminal/command prompt in this folder
3. Run: `pip install pillow`
4. Run: `python launch_previewer.py` or `python fashionpreviewer.py`

## Requirements

- **Python 3.7 or higher**
- **Pillow library** (for image processing)
- **Required folder structure** (see below)

## Required Folder Structure

The application expects the following folders to be present:

```
FashionPreviewer/
├── changelog.md              # Obvious
├── README.md                # This document :3c
├── LICENSE                  # Legally binding license
├── run_windows.bat          # Windows launcher
├── run_linux.sh            # Linux launcher
├── AAA Legacy/             # Old Versions
│   ├── v2.0/               
│   ├── v2.1/               
│   └── ...                 # Other versions
├── AAA Tutorials/          # Tutorial Images
│   ├── EditorTutorial.png/ # How to use the editor in general           
│   └── pythonpathwind.png/ # How to add Python to Environment Paths  
├── exports/                # Export directory
│   ├── images/             # Exported BMPs and PNGs 
│   └── custom_pals/        # Exported custom palettes             
└── src/                    # Core assets folder
    ├── fashionpreviewer.py # da main sauce
    ├── launch_previewer.py # Cross-platform launcher
    ├── rawbmps/           # Character images
    │   ├── chr001/        # Bunny 1st Job images (bmps able to be removed/deleted)
    │   ├── chr002/        # Buffalo 1st Job images (bmps able to be removed/deleted)
    │   ├── myshop_base.bmp # Base image for MyShop exports
    │   └── ...           # Other character folders (bmps able to be removed/deleted)
    └── vanilla_pals/      # Default game palettes
        ├── fashion/       # Fashion palettes
        │   ├── chr001_w00.pal
        │   ├── chr001_w01.pal
        │   └── ...
        ├── hair/         # Hair palettes
        │   ├── chr001_1.pal
        │   ├── chr001_2.pal
        │   └── ...
        └── 3rd_default_fashion/  # 3rd job base fashion
            ├── chr017/
            ├── chr018/
            └── ...

```

## Tips

1. When using multi-select, hold down shift and click the last color you want to select a whole bunch at once :3!
2. Make sure to always save in case it crashes too...This is vibe-coded, after all.
3. If Custom Palettes are loading weird:
   - Make sure you DID NOT MOVE THE PALS FOLDER INTO THE CUSTOM PALS FOLDER (don't do that!!!!!!!!!!!!)
   - Double check that the palette is correct in another palette editor and compare it to a vanilla of a
      similar type, including the transparent indexes

## Troubleshooting

### "Previewer and fashion doesn't load"

**Most Common Causes:**

1. **Wrong Working Directory**
   - **IMPORTANT**: The application must be run from the FashionPreviewer folder
   - Use `run_previewer.bat` (Windows), `run_previewer.sh` (Linux), or `launch_previewer.py` to ensure correct directory
   - Don't double-click the .py file directly - it may run from the wrong directory

2. **Missing Python Dependencies**
   - Run: `pip install Pillow`
   - Make sure Python is installed and added to PATH

3. **Missing Required Folders**
   - Ensure `src/rawbmps/` folder exists with character images
   - Ensure `src/pals/` folder exists with fashion and hair palettes
   - Check that folder names match exactly (case-sensitive)

4. **Python Not in PATH**
   - Reinstall Python and check "Add to PATH" during installation
   - Restart computer after Python installation

### Error Messages

1. **"ModuleNotFoundError: No module named 'PIL'"**
   - Run: `pip install Pillow`

2. **"FileNotFoundError" or "No images found"**
   - Check that `src/rawbmps/` folder exists with character subfolders
   - Verify image files are .bmp or .png format
   - Make sure you're running from the correct directory

3. **"No palettes found"**
   - Check that `src/pals/fashion/` and `src/pals/hair/` folders exist
   - Verify palette files are .pal format
   - Make sure you're running from the correct directory

4. **"No custom palettes found"**
   - Check that `src/custom_pals/` folder exists
   - Verify palette files are .pal format
   - Make sure you're running from the correct directory

5. **"ModuleNotFoundError: No module named 'PIL'"**
   - Run: `pip install Pillow`

### Other Common Errors

1. **Colors don't save when I am trying to save them in the pal editor!**
   - Are you sure you're following the tutorial PNG? Right clicking to select a
      color to save/change, and then left clicking to use to replace a cell?
      There's now a button and help dialogue to help!

### "Intended" Hardcoded User "Issues"

1. **Custom Pals only respond to chr###_w# format!**
   - Vanilla format--easier to keep up with tbh

2. **Vanilla pal files are not able to be renamed in the program!**
   - I've considered making a read-only label in the program for you, but I haven't decided how
      to do it yet (maybe by the middle index of each or something or user label or both? Would
      require work. I'll think about it some more.)

3. **The character folders are named weird!**
   - They're named in congruence with how they appear in the libconfig.

4. **Fashion is labeled in weird categories**
   - Look, I tried to do it from memory, ok? Forgive me. :( It's a LOT of work labeling these as
      it is. I'll fix it later, probably.

### "Fixed" Bugs

They may be back. Or not properly fixed. We don't know. Better safe than sorry.

(These *should* be fixed in v2.1+)

1. **Sliders move on their own sometimes**
   - Program's haunted (vibecoded); needs a priest (real coder)
   - Uses divine intuition to tell what your colors *should* be, for sure. Definitely.

2. **Sliders keep resetting**
   - Stop trying to make black move it's not going to like it at all, we don't
      know why--please be nice this is vibecoded and free :(

(These *should* be fixed in v2.2+)

3. **Fox First Job fashion (purse) shows green hair when selected**
   - UPDATE ALREADY!!!!!!!!!! (pls)

(These *should* be fixed in v2.3+)

4. **Third Job Dragon Fashion doesn't show the right indexes**
   - Should be fixed in v2.3

5. **Third Job Dragon Fashion sometimes has buttons disappear**
   - Should be fixed in v2.3

(These *should* be fixed in v3.0+)

6. **Paula fashion is improperly labeled!**
   - Should be fixed in v3.0

7. **Custom pals only support 2 numbers!**
   - Goes infinitely in v3.0 now

(These *should* be fixed in v3.2+)

8. **Gloves, Satchels, and Shoes are all being sorted together for Bard**
   - Should be fixed in v3.2

9. **BMP BG Style options don't ungrey when BMP is selected**
   - Should be fixed in v3.2

10. **Scroll wheel doesn't work with the scroll boxes**
   - Should be fixed in v3.2


### Debug Information

The application now includes debug output that shows:
- Current working directory
- Paths where it's looking for files
- Summary of loaded data

If you see "Looking for rawbmps folder at: C:\Some\Wrong\Path", then the working directory is wrong.

### Manual Installation Steps

If the launchers don't work:

1. **Install Python:**
   - Download from [python.org](https://python.org)
   - During installation, **check "Add Python to PATH"**
   - Restart your computer

2. **Install Dependencies:**
   - Open Command Prompt as Administrator
   - Navigate to FashionPreviewer folder
   - Run: `pip install Pillow`

3. **Run the Application:**
   - Open Command Prompt
   - Navigate to FashionPreviewer folder
   - Run: `python fashionpreviewer.py`


## Support

If you continue to have issues:
1. Check that all required folders exist
2. Verify Python and Pillow are properly installed
3. Try running from Command Prompt to see error messages
4. **Most importantly**: Ensure you're running from the correct directory
5. Use the provided launcher scripts to avoid working directory issues
