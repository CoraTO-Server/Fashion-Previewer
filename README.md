# Fashion Previewer v4.0

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
- **Illustration and Icon Export**: To make your life simple with implementation!
- **Key Commands**: Commands to make your life simple and efficient!
- **Click to Index**: Jump to an index by clicking on the Live Preview!
- **Local Statistics**: For the funzies, to track your progress, saved ONLY on your PC!

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
- **Saved colors:** JSON for Saved Colors boxes, PAL for Icon Colors
   - JSON saved in `exports/colors/json` folder 
   - PAL saved in `exports/colors/icon` folder
- Saved colors **do not** have to be saved in these folders to be imported


## Quick Start

### For Windows Users:

1. Install Python 3.7+ from [python.org](https://python.org)
2. Type "Environment" in Windows Start search and Add the location of the
   Python folder to your "Paths" 
      **NOTE:** For this step, there IS a tutorial image in `AAA Tutorials`
3. Restart
4. **Double-click `run_previewer.bat`** to start the application
   - This will automatically check for Python and required folders
   - This SHOULD download all dependencies for you, if you haven't already.
   - If you get dependency errors, run: `pip install Pillow`
   - If you're on the version WITHOUT the bat/launcher, then type in the
      terminal `pip install Pillow` (your first time v4.0+) then 
      `py fashionpreviewer.py`


### For Linux:

1. Install Python 3.7+ from [python.org](https://python.org)
2. Double-left click `run_previewer.sh` or run in the terminal 
   `pip install pillow` (your first time v4.0+) and then 
   `python launch_previewer.py`


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
├── changelog.md                      # Obvious
├── README.md                         # This document :3c
├── LICENSE                           # Legally binding license
├── run_windows.bat                   # Windows launcher
├── run_linux.sh                      # Linux launcher
├── AAA Legacy/                       # Old Versions
│   ├── v2.0/               
│   ├── v2.1/               
│   └── ...                           # Other versions
├── AAA Tutorials/                    # Tutorial Images
│   ├── EditorTutorial.png/           # How to use the editor in general           
│   └── pythonpathwind.png/           # How to add Python to Environment Paths  
├── exports/                          # Export directory
│   ├── images/                       # Exported BMPs and PNGs
│   ├── custom_fashion_pals/          # Exported custom palettes
│   ├── icons/                        # Exported icons
│   └── colors/                       # Saved color collections
│       ├── json/                     # JSON color files from all editors
│       └── icon/                     # Icon color palette files
└── src/                              # Core assets folder
    ├── fashionpreviewer.py           # da main sauce
    ├── launch_previewer.py           # Cross-platform launcher
    ├── rawbmps/                      # Character images
    │   ├── chr001/                   # Bunny 1st Job images (bmps able to be removed/deleted)
    │   ├── chr002/                   # Buffalo 1st Job images (bmps able to be removed/deleted)
    │   └── ...                       # Other character folders (bmps able to be removed/deleted)
    └── nonremovable_assets/          # Assets that shouldn't be removed/modified
        ├── myshop_base.bmp           # Base image for MyShop exports
        ├── icons/                    # Icon assets
        │   ├── chr001/               # Bunny fashion icons
        │   │   ├── BMP/              # Icon BMPs
        │   │   └── PAL/              # Icon palettes
        │   └── ...                   # Other character icon folders
        └── vanilla_pals/             # Default game palettes
            ├── fashion/              # Fashion palettes
            │   ├── chr001_w00.pal
            │   ├── chr001_w01.pal
            │   └── ...
            ├── hair/                 # Hair palettes
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
4. The icon editor's color imports are finnicky--the inverse order operation should help adjust, but it
   is not perfect, and I am sorry. I may be trying to fix this in a future update.

## Troubleshooting

For a comprehensive list of error messages, their solutions, and other problems you may encounter, please see
    **[TROUBLESHOOTING.md](AAA%20TUTORIALS/TROUBLESHOOTING.md)** for more information.


This document contains detailed information about:
- Python dependency errors
- Launcher and startup issues
- File structure warnings
- Palette loading errors
- Export failures
- Input validation errors
- Icon editor issues
- "Intended" issues
- And much more!

Each error includes the exact message, cause, and solution.

## "Fixed" Bugs

They may be back. Or not properly fixed. We don't know. Better safe than sorry.

### (These *should* be fixed in v2.1+)

1. **Sliders move on their own sometimes**
   - Should be fixed in v2.1

2. **Sliders keep resetting**
   - Should be fixed in v2.1

### (These *should* be fixed in v2.2+)

3. **Fox First Job fashion (purse) shows green hair when selected**
   - Should be fixed in v2.2

### (These *should* be fixed in v2.3+)

4. **Third Job Dragon Fashion doesn't show the right indexes**
   - Should be fixed in v2.3

5. **Third Job Dragon Fashion sometimes has buttons disappear**
   - Should be fixed in v2.3

### (These *should* be fixed in v3.0+)

6. **Paula fashion is improperly labeled!**
   - Should be fixed in v3.0

7. **Custom pals only support 2 numbers!**
   - Goes infinitely in v3.0 now

### (These *should* be fixed in v3.2+)

8. **Gloves, Satchels, and Shoes are all being sorted together for Bard**
   - Should be fixed in v3.2

9. **BMP BG Style options don't ungrey when BMP is selected**
   - Should be fixed in v3.2

10. **Scroll wheel doesn't work with the scroll boxes**
   - Should be fixed in v3.2

### (These *should* be fixed in v4.0+)

11. **Live Edit Pallette editor breaks on Linux**
   - Should be fixed in v4.0 or v3.1 (if you want to downgrade, for whatever reason)

12. **Shoes are not showing up for Fox 2nd job Fashion**
   - Should be fixed in v4.0

13. **Some Gears Options don't stay when the menu closes**
   - Should be fixed in v4.0

14. **Double click bug in Live Pal Editor makes certain colors duplicate!**
   - Should be fixed in v4.0 (mostly; we can only do so much protection with
      this, I found, unfortunately.)

15. **Boxes jitter when selected in Live Pal Editor**
   - Should be fixed in v4.0, along with a simpler editor to use by default

16. **The program doesn't switch to All mode when max params are given**
   - Should be fixed in v4.0

17. **The program doesn't center the image on single view!**
   - Honestly I really delayed fixing this because I CBA to rip up the file sooner.
   - Should be fixed in v4.0

18. **The program doesn't support zoom past x% for Custom or All Previews**
   - Intentional guardrail--needed to program the canvas to clip better
   - Should be fixed in v4.0

19. **The program only populates in rows of 3!**
   - This was intentional for the zoom at the time
   - Should be fixed in v4.0

