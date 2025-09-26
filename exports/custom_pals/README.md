# Custom Palettes

This folder contains subfolders for different types of custom palette files that will be automatically loaded by the Fashion Previewer.

## Folder Structure

- `hair/` - Custom hair palette files
- `fashion/` - Custom fashion palette files

## Additional Export Folders

The Fashion Previewer also creates other folders in the `exports/` directory:

- `colors/icon/` - Icon palette files exported from the Icon Editor (no naming convention required)
- `colors/json/` - Saved color collections from the "saved colors" black boxes in editors (no naming convention required)
- `images/` - Exported character images (PNG/BMP files)
- `icons/` - Exported icon BMP files from the Icon Editor
- `custom_fashion_pals/` - Legacy folder for backward compatibility (still works but deprecated)

## Hair Palettes (`hair/` folder)

Custom hair palette files must follow this naming pattern:
```
chr###_#.pal
```

Where:
- `chr###` = Character number (e.g., chr001, chr017, chr025)
- `_#` = Any number of digits after the underscore (e.g., _1, _999, _12345)
- `.pal` = File extension

### Hair Examples

Valid filenames:
- `chr001_999.pal` - Custom hair palette for character 001
- `chr017_5.pal` - Custom hair palette for character 017  
- `chr025_12345.pal` - Custom hair palette for character 025

Invalid filenames:
- `chr1_1.pal` - Character number must be 3 digits
- `chr001_w1.pal` - Hair palettes don't use 'w' prefix (that's for fashion)
- `chr001.pal` - Must have underscore and number after character ID

## Fashion Palettes (`fashion/` folder)

Custom fashion palette files must follow this naming pattern:
```
chr###_w#.pal
```

Where:
- `chr###` = Character number (e.g., chr001, chr017, chr025)
- `_w#` = Fashion number with 'w' prefix (e.g., _w7, _w103, _w999)
- `.pal` = File extension

### Fashion Examples

Valid filenames:
- `chr001_w7.pal` - Custom fashion palette for character 001
- `chr017_w103.pal` - Custom fashion palette for character 017
- `chr025_w999.pal` - Custom fashion palette for character 025

Invalid filenames:
- `chr1_w7.pal` - Character number must be 3 digits
- `chr001_7.pal` - Fashion palettes must use 'w' prefix
- `chr001_w.pal` - Must have number after 'w'

## Usage

1. Place your custom `.pal` files in the appropriate subfolder (`hair/` or `fashion/`)
2. Start or restart the Fashion Previewer
3. Select the appropriate character
4. Custom palettes will appear marked with "(C)" in the respective sections
5. A warning will appear when selecting hair palettes since they don't affect in-game fashion

## Character ID Reference

| Character ID | Character Name | Job |
|--------------|----------------|-----|
| chr001 | Bunny | 1st Job |
| chr002 | Buffalo | 1st Job |
| chr003 | Sheep | 1st Job |
| chr004 | Dragon | 1st Job |
| chr005 | Fox | 1st Job |
| chr006 | Lion | 1st Job |
| chr007 | Cat | 1st Job |
| chr008 | Raccoon | 1st Job |
| chr009 | Bunny | 2nd Job |
| chr010 | Buffalo | 2nd Job |
| chr011 | Sheep | 2nd Job |
| chr012 | Dragon | 2nd Job |
| chr013 | Fox | 2nd Job |
| chr014 | Lion | 2nd Job |
| chr015 | Cat | 2nd Job |
| chr016 | Raccoon | 2nd Job |
| chr017 | Bunny | 3rd Job |
| chr018 | Buffalo | 3rd Job |
| chr019 | Sheep | 3rd Job |
| chr020 | Dragon | 3rd Job |
| chr021 | Fox | 3rd Job |
| chr022 | Lion | 3rd Job |
| chr023 | Cat | 3rd Job |
| chr024 | Raccoon | 3rd Job |
| chr025 | Paula | 1st Job |
| chr026 | Paula | 2nd Job |
| chr027 | Paula | 3rd Job |

## Technical Details

### Palette Files

- Palette files must be exactly 768 bytes (256 colors × 3 bytes RGB)
- All byte values must be in range 0-255
- Path handling is Linux-friendly using `os.path.join()`
- Custom palettes are loaded after vanilla palettes and sorted alphabetically
- The app maintains backward compatibility with the old `custom_fashion_pals/` folder

### Export Folders Details

- **`colors/icon/`**: Stores palette files (.pal) exported from the Icon Editor. These are standard 768-byte VGA palette files with no specific naming requirements.
- **`colors/json/`**: Stores saved color collections (.json) from the "saved colors" feature in both Live Palette Editor and Icon Editor. These contain 20 RGB color values and can be named anything.
- **`images/`**: Contains exported character images in PNG or BMP format with applied custom palettes.
- **`icons/`**: Contains exported icon BMP files from the Icon Editor with custom colors applied.

### Saved Colors Feature

The black color boxes in both editors allow you to:
- Save frequently used colors for quick access
- Export/import color collections as JSON files to `colors/json/` folder
- Apply saved colors to multiple palette indices
- Toggle between left-click save / right-click apply modes

### Icon Editor Colors
- Icon palette files (.pal) are saved to `colors/icon/` folder
- These are standard 768-byte VGA palette files
- No specific naming convention required - name them however you like
- Can be loaded back into the Icon Editor using "Load Icon Colors" button

## Migration

If you have existing palettes in the old `exports/custom_fashion_pals/` folder, they will still work but it's recommended to move them:
- Fashion palettes (`chr###_w#.pal`) → `exports/custom_pals/fashion/`
- Hair palettes (`chr###_#.pal`) → `exports/custom_pals/hair/`