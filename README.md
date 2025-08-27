# Fashion Previewer v2.2

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

## Features

- **Character Selection:** Choose from different characters and jobs
- **Fashion Customization:** Apply different fashion palettes
- **Hair Customization:** Apply different hair palettes
- **3rd Job Base Fashion:** Special handling for 3rd job characters
- **Custom Palettes:** Add your own custom palettes in `custom_pals/`
- **Export Options:** Export as transparent PNG or combined palette
- **Multiple Preview Modes:** Single frame, all frames, or custom range
- **Live Pal Editing**: Single or multiple indexes with sliders and saved colors

## Custom Palette Format

- **Fashion palettes:** `chr###_w##.pal` (e.g., `chr001_w47.pal`)
- **Hair palettes:** `chr###_#.pal` (e.g., `chr001_5.pal`)
- Place custom palettes in the `custom_pals/` folder

## Quick Start

### For Windows Users:
1. **Double-click `run_previewer.bat`** to start the application
   - This will automatically check for Python and required folders
   - If you get dependency errors, run: `pip install Pillow`

### For Linux:
1. Install Python 3.7+ from [python.org](https://python.org)
2. Open terminal/command prompt in the folder & run `pip install Pillow`
3. Double-left click `run_previewer.sh` or run in the
   terminal `python launch_previewer.py`


### For Other Operating Systems:
1. Install Python 3.7+ from [python.org](https://python.org)
2. Open terminal/command prompt in this folder
3. Run: `pip install Pillow`
4. Run: `python launch_previewer.py` or `python fashionpreviewer_v2.2.py`

## Requirements

- **Python 3.7 or higher**
- **Pillow library** (for image processing)
- **Required folder structure** (see below)

## Required Folder Structure

The application expects the following folders to be present:

```
FashionPreviewer/
├── fashionpreviewer_v2.2.py
├── run_previewer.bat          # Windows launcher
├── launch_previewer.py        # Cross-platform launcher
├── rawbmps/                   # Character images
│   ├── chr001/               # Bunny 1st Job images (bmps able to be removed/deleted)
│   ├── chr002/               # Buffalo 1st Job images (bmps able to be removed/deleted)
│   └── ...                   # Other character folders (bmps able to be removed/deleted)
├── pals/
│   ├── fashion/              # Fashion palettes
│   │   ├── chr001_w00.pal
│   │   ├── chr001_w01.pal
│   │   └── ...
│   ├── hair/                 # Hair palettes
│   │   ├── chr001_1.pal
│   │   ├── chr001_2.pal
│   │   └── ...
│   └── 3rd_default_fashion/  # 3rd job base fashion
│       ├── chr017/
│       ├── chr018/
│       └── ...
└── custom_pals/              # Custom palettes (optional; I included some bunny ones for Preview)
    ├── chr001_w07.pal		  # Can be named anything tbh; just following vanilla standards
    ├── chr001_w17.pal		  # Can be named anything tbh; just following vanilla standards
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
   - Ensure `rawbmps/` folder exists with character images
   - Ensure `pals/` folder exists with fashion and hair palettes
   - Check that folder names match exactly (case-sensitive)

4. **Python Not in PATH**
   - Reinstall Python and check "Add to PATH" during installation
   - Restart computer after Python installation

### Error Messages

1. **"ModuleNotFoundError: No module named 'PIL'"**
   - Run: `pip install Pillow`

2. **"FileNotFoundError" or "No images found"**
   - Check that `rawbmps/` folder exists with character subfolders
   - Verify image files are .bmp or .png format
   - Make sure you're running from the correct directory

3. **"No palettes found"**
   - Check that `pals/fashion/` and `pals/hair/` folders exist
   - Verify palette files are .pal format
   - Make sure you're running from the correct directory

4. **"ModuleNotFoundError: No module named 'PIL'"**
   - Run: `pip install Pillow`

### Other Common Errors

1. **Colors don't save when I am trying to save them in the pal editor!**
   - Are you sure you're following the tutorial PNG? Right clicking to select a
      color to save/change, and then left clicking to use to replace a cell?


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
   - Run: `python fashionpreviewer_v2.2.py`

### Other Bugs

(These *should* be fixed in v2.1+ but better safe than sorry)

1. **Sliders move on their own sometimes**
   - Program's haunted (vibecoded); needs a priest (real coder)
   - Uses divine intuition to tell what your colors *should* be, for sure. Definitely.

2. **Sliders keep resetting**
   - Stop trying to make black move it's not going to like it at all, we don't
      know why--please be nice this is vibecoded and free :(

(These *should* be fixed in v2.2+ but better safe than sorry)

3. **Fox First Job fashion (purse) shows green hair when selected**
   - UPDATE ALREADY!!!!!!!!!! (pls)



## Support

If you continue to have issues:
1. Check that all required folders exist
2. Verify Python and Pillow are properly installed
3. Try running from Command Prompt to see error messages
4. **Most importantly**: Ensure you're running from the correct directory
5. Use the provided launcher scripts to avoid working directory issues
