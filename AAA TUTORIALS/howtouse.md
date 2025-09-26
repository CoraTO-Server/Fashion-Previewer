# How to Use This Tool & Implement Fashion

## To implement fashion you need 4 things: 

- Custom pal
- Portrait (for each piece)
- Portrait (for the set)
- Icon

In the gear menu, you can select things such as the choice of frame to export (the 
	numbers are below the frames) if you aren't on single mode and don't want 
	to export the first frame in the series. Also, you need to select **BMP**, 
	**Portrait**, and feel free to select whether or not you want the background.
	To select the frame to export please put the number in **User Choice Export**.

To edit a pal, select it in the display, and then press Live Edit Pal.
When you click on the previews on the Live Pal Editor and the Live Icon Editor, you can
	select the color in the Colors to Edit (Active Colors) and adjust it using the 
	sliders. Or, just select the box itself and you're good to work on it.
When you save the pal, make sure you name it **chr###_w##**
It autopopulates with the base pal character name so you can just **change the numbers 
	after the w**.
The chr### needs to remain congruent with the original, so please don't change this.
	e.g. Bunny-1st job must always be chr001, Paula first job must always be 025, etc.
When you save the pal, it gives you the option to quicksave or edit the icon--edit the 
	icon and save it. **I HIGHLY SUGGEST USING THE ICON EDITOR INSTEAD OF QUICK SAVE**.
	Quick save is kinda fked. But I put it there anyway. I'll work on improving it and
	the icon logic later.


It's honestly more intuitive to use than you think, it's just, you need the specific files 
	and that specific format before implementing into the libconfig.

## Adding to Libconfig

# For people who don't know how to make custom fashion:

1. Locate in your libconfig the `ItemParamCM2` (or your appropriate ItemParam) table for an
	existing piece of fashion you wish to duplicate in TO-Toolbox (or export as a CSV--
	much quicker to search)

2. Check the `<PartFileName>` column for the appropriate pal

3. Duplicate the pal and rename it to something similar that you'll take note of (preferably
	something next in sequence that hasn't been taken yet to follow vanilla standard)

4. **Copy and paste the listing row and tinker the values on your copied-and-pasted row,
	specifically the following** (for most of them, this is a comprehensive list):

ID, Name, Comment, Use, FileName, InvFileName, CmtFileName, PartFileName, ShopFileName (only set
	this one if you plan on putting into myshop)

**UNDER NO CIRCUMSTANCES, IF YOU COPY AND PASTE, SHOULD YOU TOUCH THE FOLLOWING**: 
	*Class, Type, SubType, ItemFType, Options, ChrTypeFlags*

**TIP**: Also, program this item into a shop for easy access later for testing. Otherwise, 
	find another spot to put it at this point.

5. Use the [Fashion Editor](https://github.com/CoraTO-Server/Fashion-Previewer/) to make the pal,
	icon, and portrait

6. Edit the nri's for the icon/illustration and put them in the appropriate folders

7. Make sure the libconfig is properly set, the new pal file is in wearparts (or whereever you
	directed the PartFileName to in the libconfig), the appropriate nri's are where they should
	be, one last time, and then LAUNCH! Make sure you flipped the server off and on again!

8. Find where you put the fashion item in the libconfig then in-game and obtain it and test it out!