# Fashion Previewer - Troubleshooting Guide

This document contains all error messages that may appear in the Fashion Previewer application, along with their causes and solutions.

## General Troubleshooting Tips

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
   - Ensure `src/nonremovable_assets/` folder exists with `vanilla_pals` and `icon` and folders
   - Check `vanilla_pals` folder has `3rd_default_fashion`, `fashion`, and `hair` folders, with pallettes
   - Check `icons` folder has `chr001` - `chr027` folders with `BMP` and `PAL` folders inside each with their
      respective elements
   - Check that folder names match exactly (case-sensitive)

4. **Python Not in PATH**
   - Reinstall Python and check "Add to PATH" during installation
   - Restart computer after Python installation
   - There's now a tutorial image in `AAA Tutorials` to help you on Windows!

### If you're still having issues:

1. **Check the console output** - Many errors provide additional details in the console
2. **Verify file permissions** - Ensure the application has read/write access to all folders
3. **Check disk space** - Ensure you have enough free space for exports
4. **Restart the application** - Sometimes a simple restart resolves temporary issues
5. **Check file integrity** - Ensure all files are complete and not corrupted
6. **Update dependencies** - Make sure you have the latest version of Pillow: `pip install --upgrade Pillow`

### Common File Structure Issues:

- Ensure all required folders exist in the correct locations
- Check that image files are in supported formats (.bmp, .png)
- Verify palette files are valid VGA 24-bit format (.pal)
- Make sure you're running the application from the correct directory

### Still need help?

If you continue to experience issues not covered in this guide, please check the console output for additional error details and consider:
- Checking the application's GitHub repository for known issues
- Verifying your system meets the minimum requirements
- Ensuring all dependencies are properly installed

### "Intended" Hardcoded User "Issues"

1. **Custom Pals only respond to chr###_w# format!**
   - Vanilla format--easier to keep up with tbh

2. **Vanilla pal files are not able to be renamed in the program!**
   - I've considered making a read-only label in the program for you, but I haven't decided how
      to do it yet (maybe by the middle index of each or something or user label or both? Would
      require work. I'll think about it some more.)

3. **The character folders are named weird!**
   - They're named in congruence with how they appear in the libconfig.

4. **The QuickSave for icons sucks and makes light items dark!**
    - Yeah I know :/ It's because of how I have the palettes. Too lazy to rearrange them properly
        and index properly. Will probably be a future update.

## Error Messages

### Python Dependencies

1. **"ModuleNotFoundError: No module named 'PIL'"**
   - **Cause**: Pillow library not installed
   - **Solution**: Run `pip install Pillow`

### Launcher Errors

2. **"ERROR: Python is not installed or not in PATH!"**
   - **Cause**: Python not found in system PATH
   - **Solution**: Install Python and ensure it's added to PATH during installation

3. **"ERROR: src folder not found!"**
   - **Cause**: Launcher not in correct directory
   - **Solution**: Make sure launcher is in the same folder as the src folder

4. **"ERROR: src/launch_previewer.py not found!"**
   - **Cause**: Missing launcher file
   - **Solution**: Ensure launch_previewer.py is in the src folder

5. **"ERROR: src/fashionpreviewer.py not found!"**
   - **Cause**: Missing main application file
   - **Solution**: Ensure fashionpreviewer.py is in the src folder

6. **"ERROR: Application failed to start"**
   - **Cause**: Missing Python dependencies or corrupted files
   - **Solution**: Install required dependencies with `pip install Pillow`

7. **"ERROR: The application crashed or failed to start!"**
   - **Cause**: Application crash or missing dependencies
   - **Solution**: Check console for specific error details, install missing dependencies

### File Structure Warnings
8. **"WARNING: src/rawbmps folder not found! Character images may not load."**
   - **Cause**: Missing character image folder
   - **Solution**: Ensure `src/rawbmps/` folder exists with character subfolders

9. **"WARNING: src/nonremovable_assets/vanilla_pals folder not found! Fashion palettes may not load."**
   - **Cause**: Missing vanilla palette folder
   - **Solution**: Ensure `src/nonremovable_assets/vanilla_pals/` folder exists

10. **"WARNING: src/nonremovable_assets/icons folder not found! Icons may not export."**
    - **Cause**: Missing icon assets folder
    - **Solution**: Ensure `src/nonremovable_assets/icons/` folder exists

11. **"WARNING: Missing required folders"**
    - **Cause**: Essential folders missing
    - **Solution**: Ensure complete `FashionPreviewer` folder structure is present

### Directory Creation Errors

12. **"WARNING: Could not create [folder]: [error]"**
    - **Cause**: Permission issues or disk space problems
    - **Solution**: Check folder permissions and available disk space

### Palette Loading Errors

13. **"Warning: Invalid fashion palette file [file] - incorrect size: [X] bytes"**
    - **Cause**: Corrupted or invalid palette file
    - **Solution**: Re-download or recreate the palette file

14. **"Warning: Invalid fashion palette file [file] - invalid byte at position [X]"**
    - **Cause**: Corrupted palette data
    - **Solution**: Use a different palette file or recreate it

15. **"Warning: Failed to load fashion palette [file]: [error]"**
    - **Cause**: File corruption or access issues
    - **Solution**: Check file permissions and file integrity

16. **"Warning: Invalid custom fashion palette file [file] - incorrect size: [X] bytes"**
    - **Cause**: Custom palette file corruption
    - **Solution**: Recreate the custom palette file

17. **"Warning: Invalid custom fashion palette file [file] - invalid byte at position [X]"**
    - **Cause**: Corrupted custom palette data
    - **Solution**: Use a different custom palette file

18. **"Warning: Failed to load custom fashion palette [file]: [error]"**
    - **Cause**: Custom palette file access issues
    - **Solution**: Check file permissions and recreate if necessary

19. **"Warning: Invalid custom hair palette file [file] - incorrect size: [X] bytes"**
    - **Cause**: Custom hair palette corruption
    - **Solution**: Recreate the custom hair palette file

20. **"Warning: Invalid custom hair palette file [file] - invalid byte at position [X]"**
    - **Cause**: Corrupted custom hair palette data
    - **Solution**: Use a different custom hair palette file

21. **"Warning: Failed to load custom hair palette [file]: [error]"**
    - **Cause**: Custom hair palette access issues
    - **Solution**: Check file permissions and recreate if necessary

22. **"Warning: Invalid hair palette file [file] - incorrect size: [X] bytes"**
    - **Cause**: Hair palette file corruption
    - **Solution**: Re-download or recreate the hair palette file

23. **"Warning: Invalid hair palette file [file] - invalid byte at position [X]"**
    - **Cause**: Corrupted hair palette data
    - **Solution**: Use a different hair palette file

24. **"Warning: Failed to load hair palette [file]: [error]"**
    - **Cause**: Hair palette file access issues
    - **Solution**: Check file permissions and file integrity

25. **"Warning: Invalid 3rd job palette file [file] - incorrect size: [X] bytes"**
    - **Cause**: 3rd job palette corruption
    - **Solution**: Recreate the 3rd job palette file

26. **"Warning: Invalid 3rd job palette file [file] - invalid byte at position [X]"**
    - **Cause**: Corrupted 3rd job palette data
    - **Solution**: Use a different 3rd job palette file

27. **"Warning: Failed to load 3rd job palette [file]: [error]"**
    - **Cause**: 3rd job palette access issues
    - **Solution**: Check file permissions and recreate if necessary

### Application Errors

28. **"Failed to refresh assets: [error]"**
    - **Cause**: Asset loading failure during refresh
    - **Solution**: Check file permissions and folder structure

29. **"Failed to load palette [file_path]: [error]"**
    - **Cause**: Palette file loading failure
    - **Solution**: Check file path and file integrity

30. **"Unsupported image mode: [mode]"**
    - **Cause**: Image format not supported
    - **Solution**: Convert image to supported format (RGB, RGBA, P)

31. **"Failed to load image: [error]"**
    - **Cause**: Image file loading failure
    - **Solution**: Check file path and image file integrity

32. **"No image loaded"**
    - **Cause**: No image selected or loaded
    - **Solution**: Select a character and load an image first

33. **"No images found for this character"**
    - **Cause**: Character has no image files
    - **Solution**: Ensure character has images in `src/rawbmps/[character]/`

34. **"Please select a character first"**
    - **Cause**: No character selected
    - **Solution**: Select a character from the dropdown

35. **"Please load a character image first"**
    - **Cause**: No image loaded for export
    - **Solution**: Load a character image before attempting export

### Export Errors

36. **"MyShop base image not found. Please ensure myshop_base.bmp exists in the nonremovable_assets folder."**
    - **Cause**: Missing MyShop base image
    - **Solution**: Ensure myshop_base.bmp exists in `src/nonremovable_assets/`

37. **"Failed to export image: [error]"**
    - **Cause**: Image export failure
    - **Solution**: Check disk space and file permissions

38. **"Export failed: [error]"**
    - **Cause**: General export failure
    - **Solution**: Check disk space, permissions, and file paths

39. **"Failed to create export directory: [error]"**
    - **Cause**: Cannot create export folder
    - **Solution**: Check disk space and folder permissions

40. **"Failed to export any files"**
    - **Cause**: All export attempts failed
    - **Solution**: Check individual error messages for specific issues

41. **"No palette layers loaded"**
    - **Cause**: No palette data available
    - **Solution**: Load a character and select fashion/hair items

42. **"No active palette layers to export"**
    - **Cause**: No active palettes selected
    - **Solution**: Select fashion or hair items to create active layers

### Input Validation Errors

43. **"Frame number must be between 1 and [X]"**
    - **Cause**: Invalid frame number input
    - **Solution**: Enter a valid frame number within the range

44. **"Please enter a valid frame number"**
    - **Cause**: Non-numeric frame input
    - **Solution**: Enter a numeric value

45. **"Number of frames must be greater than 0"**
    - **Cause**: Invalid frame count
    - **Solution**: Enter a positive number

46. **"You cannot display more than [X] frames for lag purposes"**
    - **Cause**: Too many frames requested
    - **Solution**: Reduce the number of frames

47. **"Start frame must be greater than or equal to 0"**
    - **Cause**: Invalid start frame
    - **Solution**: Enter 0 or higher

48. **"End frame must be less than [X]"**
    - **Cause**: Invalid end frame
    - **Solution**: Enter a frame number less than the maximum

49. **"Start frame must be less than or equal to end frame"**
    - **Cause**: Invalid frame range
    - **Solution**: Ensure start frame ≤ end frame

50. **"Please enter a valid number"**
    - **Cause**: Non-numeric input
    - **Solution**: Enter a numeric value

### Icon Editor Errors

51. **"No active palette layer. Select Hair or a Fashion item first."**
    - **Cause**: No palette selected for icon editing
    - **Solution**: Select a hair or fashion item first

52. **"Could not determine character ID from layer name"**
    - **Cause**: Invalid layer name format
    - **Solution**: Ensure layer names follow proper format

53. **"Could not determine fashion type from layer"**
    - **Cause**: Invalid layer configuration
    - **Solution**: Check layer configuration

54. **"Failed to open icon editor: [error]"**
    - **Cause**: Icon editor initialization failure
    - **Solution**: Check system resources and try again

55. **"WARNING: Reference palette size not divisible by 3!"**
    - **Cause**: Invalid reference palette format
    - **Solution**: Use a valid VGA palette file

56. **"WARNING: Incomplete color data at offset [X]"**
    - **Cause**: Corrupted palette data
    - **Solution**: Use a different palette file

57. **"Error reading reference palette: [error]"**
    - **Cause**: Reference palette loading failure
    - **Solution**: Check file path and integrity

58. **"Error saving icon: [error]"**
    - **Cause**: Icon save failure
    - **Solution**: Check disk space and permissions

59. **"Error saving icon with colors: [error]"**
    - **Cause**: Icon with color save failure
    - **Solution**: Check disk space and file permissions

60. **"Error loading reference palette: [error]"**
    - **Cause**: Reference palette loading failure
    - **Solution**: Check file path and integrity

61. **"Error loading vanilla palette [path]: [error]"**
    - **Cause**: Vanilla palette loading failure
    - **Solution**: Check file path and integrity

62. **"Failed to save colors: [error]"**
    - **Cause**: Color save failure
    - **Solution**: Check disk space and permissions

63. **"Invalid color data format"**
    - **Cause**: Corrupted color data
    - **Solution**: Use a valid color file

64. **"Failed to load colors: [error]"**
    - **Cause**: Color loading failure
    - **Solution**: Check file path and integrity

65. **"Error, missing enough indexes in the imported palette file, compensating..."**
    - **Cause**: Palette file has insufficient colors
    - **Solution**: Use a complete VGA palette file

66. **"Failed to save icon"**
    - **Cause**: Icon save failure
    - **Solution**: Check disk space and permissions

67. **"Failed to export icon: [error]"**
    - **Cause**: Icon export failure
    - **Solution**: Check disk space and file permissions

68. **"Failed to open icon editor: unknown color name ''"**
    - **Cause**: Invalid or empty color data in the selected layer
    - **Solution**: Select a different layer with valid color data, or reload the character/fashion item

### Processing Errors

69. **"Error processing [image_path]: [error]"**
    - **Cause**: Image processing failure
    - **Solution**: Check image file integrity

70. **"Error updating preview: [error]"**
    - **Cause**: Preview update failure
    - **Solution**: Try refreshing the preview

71. **"Error handling preview click: [error]"**
    - **Cause**: Preview interaction failure
    - **Solution**: Try clicking again or refresh

72. **"Error handling preview zoom: [error]"**
    - **Cause**: Preview zoom failure
    - **Solution**: Try zooming again or refresh

### Live Palette Editor Errors

73. **"Error updating palette swatch [index]: [error]"**
    - **Cause**: Swatch display update failure in live editor
    - **Solution**: Try refreshing the live editor or restart

74. **"Error synchronizing palette swatches: [error]"**
    - **Cause**: Palette synchronization failure
    - **Solution**: Close and reopen the live palette editor

75. **"Error updating selection UI: [error]"**
    - **Cause**: Selection interface update failure
    - **Solution**: Try clicking a different color or refresh the editor

76. **"Error updating color picker: [error]"**
    - **Cause**: Color picker interface failure
    - **Solution**: Try selecting a different color or restart the editor

77. **"Error updating simple mode preview: [error]"**
    - **Cause**: Simple mode preview update failure
    - **Solution**: Switch to advanced mode temporarily or restart

78. **"Error updating advanced mode swatch [index]: [error]"**
    - **Cause**: Advanced mode swatch update failure
    - **Solution**: Try switching to simple mode or restart the editor

79. **"Error notifying icon editor of palette change: [error]"**
    - **Cause**: Communication failure between editors
    - **Solution**: Close icon editor and reopen from live palette editor

### Custom Palette Loading Errors

80. **"Error reading saved palette: [error]"**
    - **Cause**: Saved palette file corruption or access issue
    - **Solution**: Check file permissions and integrity, recreate if necessary

81. **"Failed to open icon editor: [error]"**
    - **Cause**: Icon editor initialization failure
    - **Solution**: Ensure valid layer is selected and try again

82. **"No valid color data found in the selected layer"**
    - **Cause**: Selected layer has invalid or missing color information
    - **Solution**: Select a different layer with valid palette data

83. **"No valid colors found in the selected layer"**
    - **Cause**: Layer contains no usable color data
    - **Solution**: Load a character and select fashion/hair items first

### Script Processing Errors

84. **"Error processing [image_path]: [error]"**
    - **Cause**: Image processing failure during batch operations
    - **Solution**: Check image file integrity and format

85. **"Unexpected error: [error]"**
    - **Cause**: Unhandled application error
    - **Solution**: Check console for details, restart application if needed

### Additional Validation Errors

86. **"Too Many Frames"**
    - **Cause**: Requested frame count exceeds maximum allowed
    - **Solution**: Reduce the number of frames requested

87. **"Warning: Invalid color [color] at index [index], using default gray"**
    - **Cause**: Corrupted color data in palette file
    - **Solution**: Use a different palette file or recreate the palette

88. **"Warning: Color values out of range at index [index]: [color]"**
    - **Cause**: Color values outside valid RGB range (0-255)
    - **Solution**: Fix the palette file or use a different one

89. **"Warning: Invalid color format at index [index]: [color]"**
    - **Cause**: Color data in unexpected format
    - **Solution**: Ensure palette file follows VGA 24-bit format

90. **"Warning: No valid colors extracted, using default colors"**
    - **Cause**: Entire palette file contains invalid data
    - **Solution**: Use a different, valid palette file

