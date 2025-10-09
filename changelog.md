# 1.0 - Initial features
- Zoom
- Change Background Color
- Transparent Export + Bulk Export
- Singular/All/Custom frame number preview
- Fashion palette exporter (for fun! :3c )
- All characters supported
- All jobs supported
- All vanilla (and custom, technically!) hair supported
- Debugging preview supported
- All fashion automatically sorts and categorizes by index
- All custom fashion is automatically marked as (C)
- Arrow keys to change the frames quickly (or buttons if you like!)

# 1.1 - Emergency Bugfix
- Fixed directory issue
- Fixed background coloring issue in All/Custom preview
- Added proper readme
- Added changelog
- Added new launcher debugger
- Added bat file for launching

# 2.0 - Straight Jump to the Next Level
- Live Pal Editing and Saving
- Multiselect for Pal Saving
- Bugfixes with Dragon 3rd Job UI
- VGA Output Support
- Save Custom Color Indexes
- Automatic refresh of custom pal folder
- Brightness/Hue/Saturation Sliders for Pal Editing

# 2.1 - Bug fixes
- Fixed bug where editing a range of white and black colors would choke the sliders
- Added manual refresh button
- Fixed issue where sliders jitter and reset when dealing with specific colors
- Added window resizing feature (Mainly because Dragon 3rd job bugged again, resize to view the buttons)
- Renamed given custom pals to better showcase example "vanilla structure"
- Included a small tutorial made by Dino!

# 2.2 - Addtnl Hotfix
- Fixed bug where selecting first job Fox + purse only would result in an evil green taking over the hair

# 2.3 - Bug fixes
- Added warning when editing hair or base 3rd job fashion as it cannot be implemented in game
- Added supporting text for saved colors
- Fixed bug where editing third job dragon coat was not showing the correct indexes 
- Adjusted minimum window size to avoid some buttons disappearing when viewing third job lion/dragon

# 3.0 - Restructure, Rebuild, Reform
- Restructured folder so it's easier for players to read/use
- Renamed .bat files for user QoL
- Renamed previewer file to stop driving me insane with updating it
- Updated License
- Added frame labeling (and an option to disable it in the gears menu)
- Added custom specified frame range displaying and options (as well as user tip on the side)
- Added Option Button + rotating text to change Live Pal Editor's Saving Colors Mouse Options
- Added BMP v24 export support
- Added "User Choice Frame Export" so you can specify a frame to export as for pals, bmps, and pngs
- Added "MyShop" and "Portrait" Exports for BMP to ease teams' efforts (both export functions
    use your preferred BG color!) in addition to the base BMP export:
        "MyShop" = MyShop Portrait Display (103x103 res w/ padding of chosen bg color)
        "Portrait" = Regular RClick Illustration (105x105 res w/ corners of chosen bg color)
- Expanded options for custom pal names to span up infinite numbers. Why? Why the hell not. It only 
    accepted up to 2 before.
- Made frame selected persist between "Single" and "Custom" modes
- Made Expanded Custom Preview Options gear menu to automatically set preview mode to "Custom"
- Fixed Paula Fashion Labeling
- Fixed UI a bit to fit the window a bit better

# 3.1 - Emergency Bugfix and what have you
- Added additional user control over BMP output regarding background
- Added palette export options in Custom Preview Options Menu for more artist colorpicking ease
- Fixed MyShop Portrait Display to be 135x135--proper MyShop resolution
- Fine-tuned the new UI on the Custom Preview Options Menu
- Fixed Custom Frame Display being finnicky with numbers (the numbers, Mason, what do they mean?!?!?)
- Fixed User Chosen Frame Export being turned on by default and causing problems

# 3.2 - Bugfixes again + More QoL
- Added cancel button to Custom Frame Settings UI
- Added keyboard shortcuts for quick use
- Added ability to adjust hair+fashion box vertical sizing
- Adjusted Custom Frame Settings UI a bit
- Scroll boxes are now affected by Scroll Wheel
- Scroll boxes now go back to the top when a new job/character is selected
- Removed redundant MyShop Mode
- Expanded custom frame and resolution support to PNG export (but transparent except for the cute frame)
- Fixed BMP BG Style not ungreying when Background BMP is selected
- Fixed Bard Fashion sorting
- Fixed User Choice Frame Export using old frame system (started at 0 instead of 1)

# 4.0 - Icon Upgrade + Bugfixes + Restructure
- Added Live Icon Editor (please note the index translator SUCKS rn for light colors and I'm sorry I'm lazy :( )
- Added guardrails to Live Icon Editor for only base fashion editing
- Added all jobs icons
- Added new/simpler UI to Live Icon Editor
- Added automatic character, job, fashion, pallette, and icon importer for Icon Editor
- Added icon display to Icon Editor
- Added intuitive "index-pick" from preview in Icon Editor
- Added zoom to preview on Icon Editor
- Added Inverse Order to Icon Editor (just in case)
- Added Quick Export/Live Icon Editor ask dialogue when saving a pal; Quick Export = export as pal name
- Added "Reset to Original" button on the Live Pal Editor
- Added excess scripts folder because why not. Enjoy. They're relevant to the program.
- Added highlights to the boxes on the Live Pal Editor
- Added "Simple" Live Pal Editor UI with working Live Preview
- Added user index picker to Live Pal Editor's simple Live Preview
- Added "Simple" and "Advanced" UI Options for the Live Pal Editor
- Added Credits button to Gears Menu UI
- Added Statistics button and a whole bunch of local statistics to track your progress (AND NOT SEND BACK
    TO ME--I DON'T WANT YOUR INFO!!!!!!!)
- Added automatic check and download of pillow & Python 3 dependencies to bat/sh files (even easier to use!)
- Added readme for custom exports folder
- Added frame skip guard rails to All Preview Mode
- Added visual guard rails to Main UI when Live Pal Editor is open to prevent excessive flickering (I tried ok?)
- Added Gradient tool to Simple Live Editors to streamline color variants even more
- Added HSL control over Gradient Tool application to give even more flexibility and control to users
- Added guard rails to HSL sliders & Gradient tool to avoid keying colors
- Added guard rails to Hair icon editing to prevent usage
- Added cache system to Live Editors so colors save as long as the editor's open
- Added eyedropper tool to Live Editors (not Advanced Pal) to allow more flexibility+streamlining with multiple
    palettes of the same color variant
- Adjusted padding on Main UI a bit to be more concise
- Adjusted Gears Menu UI to put two seperate boxes for Export + Portrait BG options
- Adjusted Hair/3rd job Live Palette edit warnings to be in red text so people get the point
- Centered the fking WINDOWS HOW HARD WAS IT CURSOR HOW HARD ALL THIS TIME
- Cleaned up all random ahh print statements
- Made a seperate document for all troubleshooting tips as well as the error messages and what they mean.
- Rearranged folder structure (again)
- Renamed the fashion labels to match what they are in game instead of the dumb placeholders
- Reindexed Fox 2nd job Fashion
- Removed guard rails on Zooming for Preview Modes
- Removed guard rails on importing custom hair (because people honestly want to but they should read the
    warning...)
- Reversed the Live Pal Editor's UI selection to make it more obvious
- Set "Simple" UI to default for the Live Pal Editor
- Tinkered with Live Pal Editor UI more
- Fixed a small error which caused the Live Edit Pallette to break on Linux
- Fixed Shoes not showing up for Fox 2nd job Fashion
- Fixed BG Choice, Frame choice, and Palette Format options not persisting when Gears Options menu closed
- Fixed double click bug in Live Pal Editor where all colors would reset to selected color in some way (mostly)
- Fixed jitter of boxes when selected in Live Pal Editor
- Fixed initial frame options not using user's frame options correctly
- Fixed All Mode being not properly switched in the Gears menu
- Fixed characters not centering on the main UI
- Fixed All/Custom views not populating rows/columns efficiently
- Fixed flickering of the main UI when Live Pal Editing

# 4.1 - Icon Editor & Bat Reparenting

## Additions

- Added guard rails to Live Pal Editor with 3rd job palettes and hair to not allow icon export
- Added cute headers to the bat/sh files :3c
- Added Admin Mode warning for dependency installations on bat/sh files (only needed once!)
- Added Quick Export Portrait to post-pal saving menu
    - Simple: Exports as the current Simple Viewer's frame with the palette (only current pal selection's visible)
    - Advanced: Uses Main UI's previewer to export the portrait (so all pal selections are visible)
- Added click-to-launch scripts to `AAA excess_scripts` and also organized the folders a little bit + with readme's
- Added hide checkmark box to Palette Format Options Box to hide by default
- Added Select All button to both Live Editors
- Added "Show Dev Buttons" Option to Custom Frame Settings to hide excess buttons by default on Main UI
- Added new directory `exports/full_pals` for the full pal files to seperate from the other palettes
- Added "Save Excess Colors to JSON" feature when opening the Live Icon Editor in case the translator doesn't work
    the way you like (sometimes it doesn't, I won't lie; I did my best, though.)
- Added checkboxes to the Excess Saving Colors feature to save the option for the session or forever
- Added a checkmark box to the JSON filtered colors dialogue that keeps it from showing again
- Added `settings.json` to store user settings and appropriate flags in launcher scripts to create the file if it
    doesn't already exist
- Added a check dialogue box when switching to "All" Preview Mode in order to flag for its heavy resource usage
- Added a dialogue check for "Custom" Preview Mode when displaying over 50 frames for old machines, which will
    highlight the settings you need to change in order to make it valid for what you want.

## Adjustments

- Adjusted Background Export name autopopulation to use the user's View Statistic of that character as the filename
    as well as change the end suffixes for the cropped and regular portraits
- Allowed Black in Icon Editor again
- Changed original "Quick Export" button to "Quick Export Icon"
- Changed default image export settings to be BMP / Portrait / Cute Background to make fashion creation even faster
- Changed default Palette Format to be the PNG Grid
- Changed default Save Colors Mode to reverse (Left click)
- Changed `icons/PNG` folders to be `icons/BMP` in `nonremovable_assets`
- Cleaned up excess print statements to only include Error Handling and necessary informational checks
- Reparented the Icon Editor's Color Translator to completely translate indexes properly
- Set the default export directory for Export Palette PNG to `exports/images`
- Updated the run scripts in the main directory (`run_linux.sh` & `run_windows.bat`) to be more versitile with checking
    and installing dependencies, handle the newly renamed folders

## Removals

- Removed "Inverse Order" on Icon Editor
- Removed Gradients Labeling on editor (was never supposed to be there--too many gradients, too bulky)
- Removed extrenuous debug statements; kept error ones for terminal

## Fixes

- Fixed the default export directory for saving icons malfunctioning
- Fixed Gradients adjusting Lightness instead of Value like the HSV sliders do
- Fixed Gradient Button not working properly with user multiselected options
- Fixed a numerous amount of icons
- Fixed QuickExport for the Live Pal Editor :3
- Fixed Advanced Pal Editor's UI to be wide enough to see the full palette again (sorry)
- Fixed pals not auto-refreshing after the Live Pal Editor closes
- Fixed Live Pal Editor Window not moving to the front post-edit warning
- Fixed conflicting Live Pal Editor Simple UI Mode ui code
- Fixed Save Colors Box on Live Pal Editor not being wide enough, again.
- Fixed Linux directories again
- Fixed Exports Folder being made in wrong directory upon startup
- Fixed Saving Colors not bringing the Live Pal Editor back to the front
- Fixed Icon Editor Gradient Button not having HSV Checkmark Boxes
- Fixed Icon Editor's Active Colors not/improperly displaying all actual active colors for characters like Sheep 1st
    Job - Bow (Magenta detection was fked)
- Fixed Third Job characters covering the UI buttons again (I have no idea if cursor did it this beta or last update)
- Fixed Gradient Button being missing in Live Pal Editor