import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Tuple
from PIL import Image, ImageTk
from palette_ranges import CHARACTER_RANGES
import time

# Character number mapping including alternate IDs
CHARACTER_MAPPING = {
    "chr001": {"name": "Bunny", "job": "1st Job"},
    "chr002": {"name": "Buffalo", "job": "1st Job"},
    "chr003": {"name": "Sheep", "job": "1st Job"},
    "chr004": {"name": "Dragon", "job": "1st Job"},
    "chr005": {"name": "Fox", "job": "1st Job"},
    "chr006": {"name": "Lion", "job": "1st Job"},
    "chr007": {"name": "Cat", "job": "1st Job"},
    "chr008": {"name": "Raccoon", "job": "1st Job"},
    "chr009": {"name": "Bunny", "job": "2nd Job"},
    "chr010": {"name": "Buffalo", "job": "2nd Job"},
    "chr011": {"name": "Sheep", "job": "2nd Job"},
    "chr012": {"name": "Dragon", "job": "2nd Job"},
    "chr013": {"name": "Fox", "job": "2nd Job"},
    "chr014": {"name": "Lion", "job": "2nd Job"},
    "chr015": {"name": "Cat", "job": "2nd Job"},
    "chr016": {"name": "Raccoon", "job": "2nd Job"},
    "chr017": {"name": "Bunny", "job": "3rd Job"},
    "chr018": {"name": "Buffalo", "job": "3rd Job"},
    "chr019": {"name": "Sheep", "job": "3rd Job"},
    "chr020": {"name": "Dragon", "job": "3rd Job"},
    "chr021": {"name": "Fox", "job": "3rd Job"},
    "chr022": {"name": "Lion", "job": "3rd Job"},
    "chr023": {"name": "Cat", "job": "3rd Job"},
    "chr024": {"name": "Raccoon", "job": "3rd Job"},
    "chr025": {"name": "Paula", "job": "1st Job", "alt_id": "chr100"},
    "chr026": {"name": "Paula", "job": "2nd Job", "alt_id": "chr101"},
    "chr027": {"name": "Paula", "job": "3rd Job", "alt_id": "chr102"},
    "chr100": {"name": "Paula", "job": "1st Job", "main_id": "chr025"},
    "chr101": {"name": "Paula", "job": "2nd Job", "main_id": "chr026"},
    "chr102": {"name": "Paula", "job": "3rd Job", "main_id": "chr027"},
}

class IndexTranslator:
    """Handles translation between original palette indexes and icon palette indexes."""
    
    def __init__(self):
        # Original palette ranges from fashionpreviewer.py
        self.original_ranges = CHARACTER_RANGES
        
        # Icon palette structure:
        # Index 0: Dummy/keying index (may be magenta or black)
        # Remaining indexes: Light to dark distribution of the actual colors
        self.icon_structure = {
            "dummy_index": 0,  # First index is always dummy/keying
            "color_start": 1,  # Actual colors start at index 1
        }
    
    def translate_to_icon_index(self, original_index: int, char_num: str, fashion_type: str) -> int:
        """
        Translate an original palette index to its corresponding icon palette index.
        
        Args:
            original_index: Index from the original palette
            char_num: Character number (e.g. '001')
            fashion_type: Type of fashion (e.g. 'fashion_1')
            
        Returns:
            Corresponding index in the icon palette, or 0 if it's a dummy/keying index
        """
        # If it's not in any of the valid ranges, it's a dummy/keying index
        ranges = self.original_ranges.get(char_num, {}).get(fashion_type, [])
        
        # Map ranges consecutively starting from index 1
        current_icon_index = self.icon_structure["color_start"]
        
        for r in ranges:
            if original_index in r:
                # Calculate position within this specific range
                relative_pos = original_index - r.start
                return current_icon_index + relative_pos
            else:
                # Move to the next range's starting position
                current_icon_index += len(r)
        
        # Return dummy index for any index not in the valid ranges
        return self.icon_structure["dummy_index"]
    
    def translate_from_icon_index(self, icon_index: int, char_num: str, fashion_type: str) -> int:
        """
        Translate an icon palette index back to its corresponding original palette index.
        
        Args:
            icon_index: Index from the icon palette
            char_num: Character number (e.g. '001')
            fashion_type: Type of fashion (e.g. 'fashion_1')
            
        Returns:
            Corresponding index in the original palette
        """
        # If it's the dummy index, return the first dummy index from original
        if icon_index == self.icon_structure["dummy_index"]:
            return 0
            
        # Get the valid ranges for this character/fashion type
        ranges = self.original_ranges.get(char_num, {}).get(fashion_type, [])
        if not ranges:
            return 0
            
        # Calculate which range this index maps to
        relative_pos = icon_index - self.icon_structure["color_start"]
        
        # Find the appropriate range and map back to original index
        current_pos = 0
        for r in ranges:
            range_size = len(r)
            if relative_pos < current_pos + range_size:
                # Found the right range, calculate original index
                return r.start + (relative_pos - current_pos)
            current_pos += range_size
        
        # If we get here, it's out of range, return dummy index
        return 0


class IconHandler:
    """Handles icon-related operations including file location and palette application."""
    
    # Class variable to track the single instance of IconPaletteEditor
    _icon_editor_instance = None
    
    # Get root directory for relative paths
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Fashion type mappings for different characters
    FASHION_NAMES = {
        "001": {  # chr001 - Bunny 1st Job
            "fashion_1": "Hoodie",
            "fashion_2": "Gloves", 
            "fashion_3": "Skort",
            "fashion_4": "Backpack",
            "fashion_5": "Shoes"
        },
        "002": {  # chr002 - Buffalo 1st Job
            "fashion_1": "Airshoes",
            "fashion_2": "Turtle Vest",
            "fashion_3": "Sash Belt", 
            "fashion_4": "Warmups",
            "fashion_5": "Wraps",
            "fashion_6": "Hair Tie"
        },
        "003": {  # chr003 - Sheep 1st Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bow",
            "fashion_5": "Bag",
            "fashion_6": "Hairpin"
        },
        "004": {  # chr004 - Dragon 1st Job
            "fashion_1": "Robe",
            "fashion_2": "Shirt",
            "fashion_3": "Jeans",
            "fashion_4": "Monk Shoes", 
            "fashion_5": "Cane"
        },
        "005": {  # chr005 - Fox 1st Job
            "fashion_1": "Coat",
            "fashion_2": "Heels",
            "fashion_3": "Slit Skirt",
            "fashion_4": "Tank",
            "fashion_5": "Tote"
        },
        "006": {  # chr006 - Lion 1st Job
            "fashion_1": "Jacket",
            "fashion_2": "Shorts",
            "fashion_3": "Trainers",
            "fashion_4": "Open Glove",
            "fashion_5": "T-neck"
        },
        "007": {  # chr007 - Cat 1st Job
            "fashion_1": "Ribbon",
            "fashion_2": "Dress",
            "fashion_3": "Boots",
            "fashion_4": "Gloves",
            "fashion_5": "Bag",
            "fashion_6": "Hairpin"
        },
        "008": {  # chr008 - Raccoon 1st Job
            "fashion_1": "Hoodie",
            "fashion_2": "Pants",
            "fashion_3": "Shoes"
        },
        "009": {  # chr009 - Bunny 2nd Job
            "fashion_1": "Jacket",
            "fashion_2": "Gloves",
            "fashion_3": "Skirt",
            "fashion_4": "Boots",
            "fashion_5": "Bag"
        },
        "010": {  # chr010 - Buffalo 2nd Job
            "fashion_1": "Vest",
            "fashion_2": "Gloves",
            "fashion_3": "Pants",
            "fashion_4": "Boots",
            "fashion_5": "Bag"
        },
        "011": {  # chr011 - Sheep 2nd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin"
        },
        "012": {  # chr012 - Dragon 2nd Job
            "fashion_1": "Robe",
            "fashion_2": "Gloves",
            "fashion_3": "Pants",
            "fashion_4": "Boots",
            "fashion_5": "Staff"
        },
        "013": {  # chr013 - Fox 2nd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin"
        },
        "014": {  # chr014 - Lion 2nd Job
            "fashion_1": "Jacket",
            "fashion_2": "Gloves",
            "fashion_3": "Pants",
            "fashion_4": "Boots",
            "fashion_5": "Bag"
        },
        "015": {  # chr015 - Cat 2nd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin"
        },
        "016": {  # chr016 - Raccoon 2nd Job
            "fashion_1": "Jacket",
            "fashion_2": "Pants",
            "fashion_3": "Boots"
        },
        "017": {  # chr017 - Bunny 3rd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin"
        },
        "018": {  # chr018 - Buffalo 3rd Job
            "fashion_1": "Jacket",
            "fashion_2": "Gloves",
            "fashion_3": "Pants",
            "fashion_4": "Boots",
            "fashion_5": "Bag"
        },
        "019": {  # chr019 - Sheep 3rd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin"
        },
        "020": {  # chr020 - Dragon 3rd Job
            "fashion_1": "Robe",
            "fashion_2": "Gloves",
            "fashion_3": "Pants",
            "fashion_4": "Boots",
            "fashion_5": "Staff"
        },
        "021": {  # chr021 - Fox 3rd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Hairpin"
        },
        "022": {  # chr022 - Lion 3rd Job
            "fashion_1": "Jacket",
            "fashion_2": "Gloves",
            "fashion_3": "Pants",
            "fashion_4": "Boots"
        },
        "023": {  # chr023 - Cat 3rd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin"
        },
        "024": {  # chr024 - Raccoon 3rd Job
            "fashion_1": "Jacket",
            "fashion_2": "Gloves",
            "fashion_3": "Pants",
            "fashion_4": "Boots",
            "fashion_5": "Bag"
        },
        "025": {  # chr025/100 - Paula 1st Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin",
            "fashion_6": "Full Set"
        },
        "026": {  # chr026/101 - Paula 2nd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin",
            "fashion_6": "Full Set"
        },
        "027": {  # chr027/102 - Paula 3rd Job
            "fashion_1": "Dress",
            "fashion_2": "Gloves",
            "fashion_3": "Boots",
            "fashion_4": "Bag",
            "fashion_5": "Hairpin",
            "fashion_6": "Full Set",
            "fashion_7": "Full Set Alt",
            "fashion_8": "Full Set Alt2"
        },
        # Alternate IDs for Paula
        "100": {"fashion_1": "Dress", "fashion_2": "Gloves", "fashion_3": "Boots", "fashion_4": "Bag", "fashion_5": "Hairpin", "fashion_6": "Full Set"},
        "101": {"fashion_1": "Dress", "fashion_2": "Gloves", "fashion_3": "Boots", "fashion_4": "Bag", "fashion_5": "Hairpin", "fashion_6": "Full Set"},
        "102": {"fashion_1": "Dress", "fashion_2": "Gloves", "fashion_3": "Boots", "fashion_4": "Bag", "fashion_5": "Hairpin", "fashion_6": "Full Set", "fashion_7": "Full Set Alt", "fashion_8": "Full Set Alt2"}
    }
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(self.script_dir)
        self.icons_dir = os.path.join(self.script_dir, "nonremovable_assets", "icons")
        
        # Fashion type mappings for different characters (copied from fashionpreviewer.py)
        self.FASHION_NAMES = {
            "001": {  # chr001
                "fashion_1": "Hoodie",
                "fashion_2": "Gloves", 
                "fashion_3": "Skort",
                "fashion_4": "Backpack",
                "fashion_5": "Shoes"
            },
            "002": {  # chr002
                "fashion_1": "Airshoes",
                "fashion_2": "Turtle Vest",
                "fashion_3": "Sash Belt", 
                "fashion_4": "Warmups",
                "fashion_5": "Wraps",
                "fashion_6": "Hair Tie"
            },
            "003": {  # chr003
                "fashion_1": "Blouse",
                "fashion_2": "Bow",
                "fashion_3": "Frill Dress",
                "fashion_4": "Flats",
                "fashion_5": "Socks",
                "fashion_6": "Spellbook"
            },
            "004": {  # chr004
                "fashion_1": "Robe",
                "fashion_2": "Shirt",
                "fashion_3": "Jeans",
                "fashion_4": "Monk Shoes", 
                "fashion_5": "Cane"
            },
            "005": {  # chr005
                "fashion_1": "Coat",
                "fashion_2": "Heels",
                "fashion_3": "Slit Skirt",
                "fashion_4": "Tank",
                "fashion_5": "Tote"
            },
            "006": {  # chr006
                "fashion_1": "Jacket",
                "fashion_2": "Shorts",
                "fashion_3": "Trainers",
                "fashion_4": "Open Glove",
                "fashion_5": "T-neck"
            },
            "007": {  # chr007
                "fashion_1": "Ribbon",
                "fashion_2": "Belt",
                "fashion_3": "Halter",
                "fashion_4": "Heels",
                "fashion_5": "Paws",
                "fashion_6": "Skirt"
            },
            "008": {  # chr008
                "fashion_1": "Blazer",
                "fashion_2": "Slacks",
                "fashion_3": "Dress Shoes"
            },
            "009": {  # chr009
                "fashion_1": "Robe",
                "fashion_2": "Boxing Glove",
                "fashion_3": "Shorts",
                "fashion_4": "Gloves",
                "fashion_5": "Boxing Shoes",
                "fashion_6": "Stocking"
            },
            "010": {  # chr010
                "fashion_1": "Fur Collar",
                "fashion_2": "Tunic",
                "fashion_3": "Bolero",
                "fashion_4": "Gauntlet",
                "fashion_5": "Leather Shoes"
            },
            "011": {  # chr011
                "fashion_1": "Checkered Dress",
                "fashion_2": "Ribbon",
                "fashion_3": "Minisack",
                "fashion_4": "Gloves",
                "fashion_5": "Ribbon Boots"
            },
            "012": {  # chr012
                "fashion_1": "Shawl",
                "fashion_2": "Beads Necklace",
                "fashion_3": "Robe",
                "fashion_4": "Wrap Skirt",
                "fashion_5": "Ankle Boots"
            },
            "013": {  # chr013
                "fashion_1": "Sports Suit",
                "fashion_2": "Tube Top",
                "fashion_3": "Elbow Wrap",
                "fashion_4": "Mittens",
                "fashion_5": "Walkers"
            },
            "014": {  # chr014
                "fashion_1": "Turtleneck",
                "fashion_2": "Coil Coat",
                "fashion_3": "Utility Belt",
                "fashion_4": "Glove",
                "fashion_5": "Boots"
            },
            "015": {  # chr015
                "fashion_1": "Hippie Shirt",
                "fashion_2": "Studded Belt",
                "fashion_3": "Checkered Skirt",
                "fashion_4": "Checkered Stockings",
                "fashion_5": "Heel Boots"
            },
            "016": {  # chr016
                "fashion_1": "Dress Shirt",
                "fashion_2": "Checkered Suit",
                "fashion_3": "Dress Shoes"
            },
            "017": {  # chr017
                "fashion_1": "Tube Top",
                "fashion_2": "Bolero Jacket",
                "fashion_3": "Gauntlets",
                "fashion_4": "Chord Skirt",
                "fashion_5": "Steel Boots"
            },
            "018": {  # chr018
                "fashion_1": "Asymmetrical Tee",
                "fashion_2": "Protector",
                "fashion_3": "Kilt",
                "fashion_4": "Steel Armlets",
                "fashion_5": "Ankle Shoes"
            },
            "019": {  # chr019
                "fashion_1": "Flower Ribbon",
                "fashion_2": "Puffy Blouse",
                "fashion_3": "Flower Brooch",
                "fashion_4": "Layered Dress",
                "fashion_5": "Flower Shoes"
            },
            "020": {  # chr020
                "fashion_1": "Wrap",
                "fashion_2": "Hooded Robe",
                "fashion_3": "Overcoat",
                "fashion_4": "Robe",
                "fashion_5": "Leather Boots"
            },
            "021": {  # chr021
                "fashion_1": "Zip-up Coat",
                "fashion_2": "Leather Shorts",
                "fashion_3": "Leather Wristlets",
                "fashion_4": "Buckle Boots",
                "fashion_5": "Unknown"
            },
            "022": {  # chr022
                "fashion_1": "Zip-up Jacket",
                "fashion_2": "Long Jacket",
                "fashion_3": "Shorts",
                "fashion_4": "Long Boots",
                "fashion_5": "Unknown"
            },
            "023": {  # chr023
                "fashion_1": "Double Coat",
                "fashion_2": "Shirring Skirt",
                "fashion_3": "Buckle Shoes",
                "fashion_4": "Blouse"
            },
            "024": {  # chr024 (Raccoon 3rd Job)
                "fashion_1": "Dress Shirt",
                "fashion_2": "Opera Cape",
                "fashion_3": "Frock Coat",
                "fashion_4": "Dress Pants",
                "fashion_5": "Full Suit",
                "fashion_6": "Formal Shoes"
            },
            "025": {  # chr025 (Paula 1st Job) - using 025 since icons are in chr025 folder
                "fashion_1": "Stadium Jacket",
                "fashion_2": "Sleeveless Dress",
                "fashion_3": "Knee Socks",
                "fashion_4": "School Loafers",
                "fashion_5": "Ribbon Chou",
                "fashion_6": "Cutie Satchel",
                "fashion_7": "Extra"
            },
            "026": {  # chr026 (Paula 2nd Job)
                "fashion_1": "Pocket One-piece",
                "fashion_2": "Animal Pocket Belt",
                "fashion_3": "Knee-high Boots",
                "fashion_4": "Ribbons",
                "fashion_5": "Arm Cover",
                "fashion_6": "Whip"
            },
            "027": {  # chr027 (Paula 3rd Job)
                "fashion_1": "Blouse",
                "fashion_2": "Trench Dress",
                "fashion_3": "Frilly Socks",
                "fashion_4": "Cutie Buckle Boots",
                "fashion_5": "Ribbon Rubber",
                "fashion_6": "Ribbon Brooch",
                "fashion_7": "Mini Pocket Belt",
                "fashion_8": "Leather Buckle Gloves"
            }
        }
        
    def _get_fashion_name(self, char_id: str, fashion_type: str) -> str:
        """Get the proper name for a fashion type based on character."""
        # Handle Paula character ID mapping - icons are in chr025/026/027 folders
        # but palettes use chr100/101/102 IDs
        if char_id == "chr100":
            char_id = "chr025"  # Paula 1st Job icons
        elif char_id == "chr101":
            char_id = "chr026"  # Paula 2nd Job icons
        elif char_id == "chr102":
            char_id = "chr027"  # Paula 3rd Job icons
        
        # Extract character number (e.g. '001' from 'chr001')
        char_num = char_id[3:] if char_id.startswith('chr') else char_id
        
        # Get the fashion name mapping for this character
        char_fashion_names = self.FASHION_NAMES.get(char_num, {})
        
        # Return the fashion name or a default
        result = char_fashion_names.get(fashion_type, fashion_type)
        print(f"Fashion name lookup: char_id='{char_id}' -> char_num='{char_num}', fashion_type='{fashion_type}' -> '{result}'")
        return result
    
    def _determine_keying_color(self, ref_colors: list) -> tuple:
        """Determine the keying color from reference palette (same logic as IconPaletteEditor)."""
        
        if not ref_colors:
            return (255, 0, 255)  # Default to magenta
        
        
        # Check first color
        if ref_colors[0] == (255, 0, 255):
            print("First color is magenta, using magenta")
            return (255, 0, 255)
        elif ref_colors[0] == (0, 0, 0):
            print("First color is black, using black")
            return (0, 0, 0)
        
        # Search for magenta or black in the palette (prioritize magenta)
        found_magenta = False
        found_black = False
        magenta_index = -1
        black_index = -1
        
        for i, color in enumerate(ref_colors):
            if color == (255, 0, 255) and not found_magenta:
                found_magenta = True
                magenta_index = i
                print(f"Found magenta at index {i}")
            elif color == (0, 0, 0) and not found_black:
                found_black = True
                black_index = i
                print(f"Found black at index {i}")
        
        # Prioritize magenta over black
        if found_magenta:
            return (255, 0, 255)
        elif found_black:
            return (0, 0, 0)
        
        # Default to magenta if no valid keying color found
        return (255, 0, 255)
    
    def open_icon_editor(self, palette_layers, live_editor_window=None):
        """Open the icon editor from the main screen."""
        import re
        from tkinter import messagebox
        
        # Check if icon editor is already open
        if IconHandler._icon_editor_instance and IconHandler._icon_editor_instance.window and IconHandler._icon_editor_instance.window.winfo_exists():
            IconHandler._icon_editor_instance._bring_to_front()
            return
        
        active_layers = [ly for ly in palette_layers if getattr(ly, "active", False)]
        if not active_layers:
            messagebox.showinfo("Icon Editor", "Please open a base fashion piece first.")
            return
            
        # Filter out hair and third job layers
        base_fashion_layers = [ly for ly in active_layers if hasattr(ly, "palette_type") and 
                             ly.palette_type.startswith("fashion_") and 
                             not (ly.name and ("hair" in ly.name.lower() or "third" in ly.name.lower()))]
                             
        if not base_fashion_layers:
            messagebox.showinfo("Icon Editor", "Please open a base fashion piece first.")
            return

        # Prefer an active fashion layer if present
        default_idx = 0
        for i, ly in enumerate(active_layers):
            if hasattr(ly, "palette_type") and ly.palette_type.startswith("fashion"):
                default_idx = i
                break

        ly = active_layers[default_idx]
        
        # Extract character ID and item name from the layer
        char_match = re.search(r'(?:chr)?(\d{3})', ly.name)
        if not char_match:
            messagebox.showerror("Error", "Could not determine character ID from layer name")
            return
        
        num = char_match.group(1)
        char_id = f"chr{num}"  # Normalize to chr format
        
        # Get the fashion type from the layer
        fashion_type = getattr(ly, "palette_type", "")
        if not fashion_type:
            messagebox.showerror("Error", "Could not determine fashion type from layer")
            return
        
        # Get current colors from the layer
        colors = ly.colors
        
        # Validate colors before proceeding
        if not colors or not isinstance(colors, list):
            messagebox.showerror("Error", "No valid color data found in the selected layer")
            return
        
        # Validate that colors contain valid RGB tuples
        valid_colors = []
        for i, color in enumerate(colors):
            if isinstance(color, (list, tuple)) and len(color) >= 3:
                try:
                    r, g, b = int(color[0]), int(color[1]), int(color[2])
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        valid_colors.append((r, g, b))
                    else:
                        print(f"Warning: Color values out of range at index {i}: {color}")
                        valid_colors.append((128, 128, 128))  # Default gray
                except (ValueError, TypeError):
                    print(f"Warning: Invalid color at index {i}: {color}")
                    valid_colors.append((128, 128, 128))  # Default gray
            else:
                print(f"Warning: Invalid color format at index {i}: {color}")
                valid_colors.append((128, 128, 128))  # Default gray
        
        if not valid_colors:
            messagebox.showerror("Error", "No valid colors found in the selected layer")
            return
        
        # Create a temporary palette path for the editor
        temp_palette_path = f"temp_{ly.name}.pal"
        
        try:
            # Open the icon palette editor directly
            editor = IconPaletteEditor(
                char_id=char_id,
                fashion_type=fashion_type,
                custom_palette=valid_colors,
                palette_path=temp_palette_path,
                palette_layers=palette_layers,
                live_editor_window=live_editor_window,
                is_quicksave_mode=False  # Editor mode - allow user to name file
            )
            
            # Store the instance and set up cleanup
            IconHandler._icon_editor_instance = editor
            editor.window.protocol("WM_DELETE_WINDOW", editor._close_editor)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open icon editor: {e}")
    
    def _get_character_folders(self, char_id: str) -> List[str]:
        """
        Get all possible character folders to check, handling Paula's special cases.
        For Paula, only check the original directories (chr025, chr026, chr027) since
        the icon files are only in those directories, not in chr100, chr101, chr102.
        """
        # For Paula, we need to check the original directories
        if char_id.startswith('chr'):
            num = char_id[3:]
        else:
            num = char_id
            
        folders_to_check = [f"chr{num}"]
        
        # If it's Paula's alternate IDs (chr100, chr101, chr102), check the original directories instead
        if num in ["100", "101", "102"]:
            original_num = f"{int(num) - 75:03d}"  # 100->025, 101->026, 102->027
            folders_to_check = [f"chr{original_num}"]
        
        
        return folders_to_check
    
    def _get_icon_paths(self, char_id: str, item_name: str) -> Tuple[str, str]:
        """
        Get paths to the icon PNG and PAL files.
        For Paula characters, checks both folders (e.g. chr025 and chr100).
        
        Args:
            char_id: Character ID (e.g. 'chr001' or 'chr025')
            item_name: Fashion type variable name (e.g. 'dress') - will be converted to actual name
            
        Returns:
            tuple[str, str]: (png_path, pal_path) for the icon files
            Returns the first matching pair found, checking all possible character folders
        """
        # Get the actual fashion name from the variable name
        actual_fashion_name = self._get_fashion_name(char_id, item_name)
        
        # Clean item name - remove spaces, uppercase, special characters and make lowercase
        clean_name = ''.join(c.lower() for c in actual_fashion_name if c.isalnum())
        
        # Debug output to see the conversion
        print(f"Icon path conversion: '{item_name}' -> '{actual_fashion_name}' -> '{clean_name}'")
        
        # Try all possible folders
        for folder in self._get_character_folders(char_id):
            char_icon_dir = os.path.join(self.icons_dir, folder)
            png_path = os.path.join(char_icon_dir, "PNG", f"{clean_name}.png")
            pal_path = os.path.join(char_icon_dir, "PAL", f"{clean_name}.pal")
            
            
            # If both files exist in this folder, use these paths
            if os.path.exists(png_path) and os.path.exists(pal_path):
                return png_path, pal_path
        
        # If no matching files found in any folder, return paths for the primary folder
        char_icon_dir = os.path.join(self.icons_dir, self._get_character_folders(char_id)[0])
        return (
            os.path.join(char_icon_dir, "PNG", f"{clean_name}.png"),
            os.path.join(char_icon_dir, "PAL", f"{clean_name}.pal")
        )
    
    def save_as_icon(self, char_id: str, fashion_type: str, custom_palette: list, palette_path: str = None) -> bool:
        """
        Save the current item as an icon with the custom palette applied.
        
        Args:
            char_id: Character ID (e.g. 'chr001')
            fashion_type: Type of fashion (e.g. 'fashion_1')
            custom_palette: List of (r,g,b) tuples representing the custom palette
            palette_path: Path to the saved custom palette file
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Get the actual item name from the fashion type
        item_name = self._get_fashion_name(char_id, fashion_type)
        # Get paths to reference PNG and PAL files
        png_path, ref_pal_path = self._get_icon_paths(char_id, item_name)
        
        # Verify files exist
        if not os.path.exists(png_path) or not os.path.exists(ref_pal_path):
            return False
            
        try:
            # Get exports/icons directory path
            export_dir = os.path.join(self.root_dir, "exports", "icons")
            
            # Get the character number without 'chr' prefix
            char_num = char_id[3:] if char_id.startswith('chr') else char_id
            
            # Get the valid ranges for this fashion type from the IndexTranslator
            translator = IndexTranslator()
            ranges = translator.original_ranges.get(char_num, {}).get(fashion_type, [])
            if not ranges:
                print(f"No ranges found for {char_id} {fashion_type}")
                return False
                
            # Convert reference palette to RGB tuples and find used indexes
            ref_colors = []
            used_indexes = []
            try:
                with open(ref_pal_path, 'rb') as f:
                    ref_pal_data = f.read()
                    
                    if len(ref_pal_data) % 3 != 0:
                        print(f"WARNING: Reference palette size not divisible by 3!")
                        
                    for i in range(0, len(ref_pal_data), 3):
                        if i + 2 >= len(ref_pal_data):
                            print(f"WARNING: Incomplete color data at offset {i}")
                            break
                            
                        r = ref_pal_data[i]
                        g = ref_pal_data[i+1]
                        b = ref_pal_data[i+2]
                        color = (r, g, b)
                        ref_colors.append(color)
                        # If it's not a keying color, add to used indexes in order
                        if color != (255, 0, 255) and color != (0, 0, 0):
                            used_indexes.append(i // 3)
                            
            except Exception as e:
                print(f"Error reading reference palette: {e}")
                return False
            
            
            # Get the valid color indexes from the vanilla ranges
            vanilla_indexes = []
            for r in ranges:
                vanilla_indexes.extend(range(r.start, r.stop))
            
            # Get the actual used indexes (non-keying colors) from the icon palette
            actual_used_indexes = []
            for idx in used_indexes:
                color = ref_colors[idx]
                if color not in [(255, 0, 255), (0, 0, 0), (0, 255, 0)]:
                    actual_used_indexes.append(idx)
                else:
                    pass
            
            icon_color_count = len(actual_used_indexes)

            # Get colors from vanilla ranges, ignoring keying colors (neon green and last index)
            vanilla_colors = []
            for r in ranges:
                for idx in range(r.start, r.stop):
                    # Skip if it's the last index in the range (keying color)
                    if idx == r.stop - 1:
                        continue
                        
                    if idx >= len(custom_palette):
                        continue
                        
                    color = custom_palette[idx]
                    # Skip neon green (0,255,0) and magenta/black keying colors
                    if color not in [(0, 255, 0), (255, 0, 255), (0, 0, 0)]:
                        vanilla_colors.append(color)
                    else:
                        pass
            
            # Sort by brightness
            vanilla_colors.sort(key=lambda c: (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]), reverse=True)
            
            
            # Take an even distribution of colors from the vanilla palette
            if vanilla_colors and icon_color_count > 0:
                
                # If we have more colors than slots, combine adjacent colors
                if len(vanilla_colors) > icon_color_count:
                    step = len(vanilla_colors) / icon_color_count
                    selected_colors = []
                    for i in range(icon_color_count):
                        start_idx = int(i * step)
                        end_idx = int((i + 1) * step)
                        # Take the middle color from this range
                        mid_idx = (start_idx + end_idx) // 2
                        mid_idx = min(mid_idx, len(vanilla_colors) - 1)
                        selected_colors.append(vanilla_colors[mid_idx])
                
                # If we have fewer colors than slots, duplicate colors evenly
                else:
                    repeats = icon_color_count / len(vanilla_colors)
                    selected_colors = []
                    for i, color in enumerate(vanilla_colors):
                        # Calculate how many times to repeat this color
                        count = int(round((i + 1) * repeats)) - int(round(i * repeats))
                        for _ in range(count):
                            selected_colors.append(color)
            else:
                selected_colors = []
                
            # Invert the order of selected colors
            selected_colors.reverse()
            
            # Create a new 256-color palette starting with black
            new_palette = [(0, 0, 0)] * 256
            
            # First, find and preserve ALL keying colors at their EXACT indexes
            keying_indexes = []
            for i, color in enumerate(ref_colors):
                if i >= 256:
                    break
                if color in [(255, 0, 255), (0, 0, 0), (0, 255, 0)]:
                    new_palette[i] = color
                    keying_indexes.append(i)
            
            # Now map our selected colors ONLY to the non-keying indexes
            color_idx = 0
            for target_idx in range(256):
                # Skip if this was a keying index
                if target_idx in keying_indexes:
                    continue
                    
                # Skip if we're out of colors
                if color_idx >= len(selected_colors):
                    break
                    
                new_palette[target_idx] = selected_colors[color_idx]
                color_idx += 1
            
            # Load and process the PNG
            if not os.path.exists(png_path):
                return False
                
            img = Image.open(png_path).convert("RGBA")
            
            # Use the same keying color detection logic as IconPaletteEditor
            keying_color = self._determine_keying_color(ref_colors)
            
            # Get alpha channel first
            alpha = img.split()[3]
            
            
            # Create a new RGB image
            new_img = Image.new("RGB", img.size)
            
            # Create mapping of original colors to new colors
            color_map = {}
            color_idx = 0
            
            # For each unique color in the PNG (except transparent), map to a color from our list
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    pixel = img.getpixel((x, y))
                    if pixel[3] > 0:  # Not transparent
                        if pixel not in color_map:
                            if color_idx < len(selected_colors):
                                color_map[pixel] = selected_colors[color_idx]
                                color_idx += 1
                            else:
                                color_map[pixel] = selected_colors[0] if selected_colors else (0, 0, 0)
            
            print(f"Created color mapping for {len(color_map)} unique colors")
            print(f"Keying color will be: RGB{keying_color}")
            
            # Apply the colors and keying
            transparent_count = 0
            opaque_count = 0
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if alpha.getpixel((x, y)) > 0:
                        pixel = img.getpixel((x, y))
                        new_color = color_map.get(pixel, (0, 0, 0))
                        new_img.putpixel((x, y), new_color)
                        opaque_count += 1
                    else:
                        # For transparent pixels, use the keying color from the reference palette
                        new_img.putpixel((x, y), keying_color)
                        transparent_count += 1
            
            
            # Save as 24-bit BMP
            icon_name = os.path.splitext(os.path.basename(palette_path))[0] + ".bmp"
            export_path = os.path.join(export_dir, icon_name)
            # Create directory if it doesn't exist when actually saving
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            new_img.save(export_path, "BMP")
            return True
            
        except Exception as e:
            print(f"Error saving icon: {e}")
            return False
    
    def save_as_icon_with_colors(self, char_id: str, fashion_type: str, colors: list, 
                                keying_color: tuple, png_path: str, export_path: str) -> bool:
        """Save icon with specific colors (used by IconPaletteEditor)."""
        try:
            # Load the original PNG
            img = Image.open(png_path).convert("RGBA")
            alpha = img.split()[3]
            
            # Create new RGB image
            new_img = Image.new("RGB", img.size)
            
            # Create color mapping
            color_map = {}
            color_idx = 0
            
            # Map original colors to our provided colors
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    pixel = img.getpixel((x, y))
                    if pixel[3] > 0:  # Not transparent
                        if pixel not in color_map:
                            if color_idx < len(colors):
                                color_map[pixel] = colors[color_idx]
                                color_idx += 1
                            else:
                                color_map[pixel] = colors[0] if colors else (0, 0, 0)
            
            # Apply colors
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if alpha.getpixel((x, y)) > 0:
                        pixel = img.getpixel((x, y))
                        new_color = color_map.get(pixel, (0, 0, 0))
                        new_img.putpixel((x, y), new_color)
                    else:
                        # Use keying color for transparent areas
                        new_img.putpixel((x, y), keying_color)
            
            # Save as 24-bit BMP
            # Create directory if it doesn't exist when actually saving
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            new_img.save(export_path, "BMP")
            return True
            
        except Exception as e:
            print(f"Error saving icon with colors: {e}")
            return False


class IconPaletteEditor:
    """A mini palette editor specifically for editing icon palettes with live preview."""
    
    def __init__(self, char_id: str, fashion_type: str, custom_palette: list, palette_path: str, palette_layers=None, live_editor_window=None, is_quicksave_mode=False):
        self.char_id = char_id
        self.fashion_type = fashion_type
        self.custom_palette = custom_palette
        self.palette_path = palette_path
        self.palette_layers = palette_layers or []
        self.live_editor_window = live_editor_window
        self.is_quicksave_mode = is_quicksave_mode
        
        # Initialize UI variables first
        self.multi_select_var = tk.BooleanVar(value=False)
        self.inverse_order_var = tk.BooleanVar(value=False)
        self.index_var = tk.StringVar(value="0")
        self.hex_var = tk.StringVar(value="#000000")
        self.hue_var = tk.IntVar(value=0)
        self.sat_var = tk.IntVar(value=0)
        self.val_var = tk.IntVar(value=0)
        self.selection_count_var = tk.StringVar(value="(0 selected)")
        self.selected_index = 0
        self.selected_indices = set()
        self.saved_colors = [(0, 0, 0)] * 20
        self.saved_mode = "L"  # "L" for left-click save, "R" for right-click save
        self.colorpicker_active = False  # Track colorpicker mode
        self.color_preview = None  # Will be set in _create_ui
        self.palette_squares = []  # Will be populated in _create_palette_grid
        self.preview_label = None  # Will be set in _create_ui
        self.index_entry = None  # Will be set in _create_ui
        self.hex_entry = None  # Will be set in _create_ui
        self.palette_canvas = None  # Will be set in _create_ui
        self.palette_frame = None  # Will be set in _create_ui
        self.saved_colors_frame = None  # Will be set in _create_ui
        self.preview_photo = None  # Will be set in _update_preview
        self.color_mapping = {}  # Maps original pixel colors to color indices
        self._last_palette_key = None  # Track the last selected palette
        self.zoom_level = 6  # Current zoom level (6x is the default for larger preview)
        self.min_zoom = 1  # Minimum zoom (100%)
        self.max_zoom = 16  # Maximum zoom (16x for larger preview area)
        self.edit_combo = None  # Will be set in _create_ui
        self._updating_selection = False  # Flag to prevent grid recreation during selection updates
        
        # Temporary palette cache to preserve changes during editor session
        self._temp_palette_cache = {}  # Cache for temporary changes during session
        self._original_palettes = {}  # Store original colors for cleanup when editor closes
        
        # Get paths to reference files
        self.icon_handler = IconHandler()
        item_name = self.icon_handler._get_fashion_name(char_id, fashion_type)
        self.png_path, self.ref_pal_path = self.icon_handler._get_icon_paths(char_id, item_name)
        
        # Load reference palette and extract colors
        self.ref_colors = []
        self.keying_color = (255, 0, 255)
        self._load_reference_palette()
        
        # Extract colors from custom palette (excluding keying colors and last index)
        self.editable_colors = self._extract_editable_colors()
        
        # Create the editor window
        self.window = tk.Toplevel()
        self.window.title(f"Icon Palette Editor - {item_name}")
        self.window.geometry("850x650")
        self.window.resizable(False, False)
        
        # Center the window on the screen
        self.window.update_idletasks()  # Update window size
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"+{x}+{y}")
        
        # Current edited colors (starts with extracted colors)
        self.current_colors = self.editable_colors.copy()
        
        # Create UI
        self._create_ui()
        
        # Load preview
        self._update_preview()
        
        # Initialize the last palette key
        self._last_palette_key = f"{self.char_id}_{self.fashion_type}"
        
        # Initialize temporary cache with current colors
        current_palette_key = f"{self.char_id}_{self.fashion_type}"
        self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
        self._original_palettes[current_palette_key] = self.editable_colors.copy()
        
        # Center the icon editor window after content is created
        self.window.update_idletasks()
        self._center_window_on_parent()
    
    def is_universal_keying_color(self, color):
        """Match the same 'universal keying' rules used in the main app."""
        r, g, b = color
        # Pure green
        if color == (0, 255, 0):
            return True
        # (0~25, 255, 0) pattern
        if g == 255 and b == 0 and 0 <= r <= 25:
            return True
        # (0, 255, 0~21) pattern
        if g == 255 and r == 0 and 0 <= b <= 21:
            return True
        return False

    def _is_keyed_color(self, rgb_color, palette_index=None):
        """Check if an RGB color is a keyed/transparency color that should be avoided"""
        r, g, b = rgb_color
        
        # Universal keying colors (same logic as main app)
        # Pure green (0, 255, 0)
        if rgb_color == (0, 255, 0):
            return True
        
        # (0~25, 255, 0) pattern
        if g == 255 and b == 0 and 0 <= r <= 25:
            return True
        
        # (0, 255, 0~21) pattern
        if g == 255 and r == 0 and 0 <= b <= 21:
            return True
        
        # Magenta (chroma key)
        if rgb_color == (255, 0, 255):
            return True
        
        # Black is generally allowed ("Never make black transparent")
        # Exception: chr004 specifically treats black as keyed
        if rgb_color == (0, 0, 0):
            if hasattr(self, 'char_id') and self.char_id:
                char_num = self.char_id[3:]  # Extract number from chr###
                if char_num == "004":
                    return True  # Black is keyed for chr004
            # Black is allowed for all other characters
            return False
        
        return False
    
    def _find_nearest_non_keyed_color(self, target_rgb, adjustment_direction='both'):
        """Find the nearest non-keyed color by adjusting RGB values"""
        r, g, b = target_rgb
        
        # If the color is not keyed, return it as-is
        if not self._is_keyed_color(target_rgb):
            return target_rgb
        
        # Try different adjustment strategies
        for offset in range(1, 20):  # Try up to 20 units of adjustment
            candidates = []
            
            if adjustment_direction in ['both', 'up']:
                # Try increasing values
                candidates.extend([
                    (min(255, r + offset), g, b),
                    (r, min(255, g + offset), b),
                    (r, g, min(255, b + offset)),
                    (min(255, r + offset), min(255, g + offset), b),
                    (min(255, r + offset), g, min(255, b + offset)),
                    (r, min(255, g + offset), min(255, b + offset)),
                ])
            
            if adjustment_direction in ['both', 'down']:
                # Try decreasing values
                candidates.extend([
                    (max(0, r - offset), g, b),
                    (r, max(0, g - offset), b),
                    (r, g, max(0, b - offset)),
                    (max(0, r - offset), max(0, g - offset), b),
                    (max(0, r - offset), g, max(0, b - offset)),
                    (r, max(0, g - offset), max(0, b - offset)),
                ])
            
            # Check each candidate
            for candidate in candidates:
                if not self._is_keyed_color(candidate):
                    return candidate
        
        # If we can't find a good alternative, return a safe default
        return (128, 128, 128)  # Gray as fallback
    
    def _load_reference_palette(self):
        """Load the reference palette and determine keying color."""
        try:
            with open(self.ref_pal_path, 'rb') as f:
                ref_pal_data = f.read()
                
            # Convert to RGB tuples
            for i in range(0, len(ref_pal_data), 3):
                if i + 2 < len(ref_pal_data):
                    r = ref_pal_data[i]
                    g = ref_pal_data[i+1]
                    b = ref_pal_data[i+2]
                    self.ref_colors.append((r, g, b))
            
            # Determine keying color (always use first index)
            if self.ref_colors:
                first_color = self.ref_colors[0]
                
                # Verify if first index is a valid keying color (magenta or black)
                if first_color == (255, 0, 255):
                    self.keying_color = (255, 0, 255)
                elif first_color == (0, 0, 0):
                    self.keying_color = (0, 0, 0)
                else:
                    # First index is not a valid keying color, shift palette down by 1
                    self.keying_color = (255, 0, 255)
                    
                    # Shift all colors down by 1 index (skip the invalid first color)
                    shifted_colors = []
                    for i in range(1, len(self.ref_colors)):
                        shifted_colors.append(self.ref_colors[i])
                    
                    # Ensure we have exactly 256 colors (remove last if needed, then pad if needed)
                    if len(shifted_colors) > 256:
                        shifted_colors = shifted_colors[:256]  # Remove excess colors
                    elif len(shifted_colors) < 256:
                        # Pad with magenta to reach 256 colors
                        while len(shifted_colors) < 256:
                            shifted_colors.append((255, 0, 255))
                    
                    self.ref_colors = shifted_colors
            else:
                self.keying_color = (255, 0, 255)
                        
        except Exception as e:
            print(f"Error loading reference palette: {e}")
    
    def _extract_editable_colors(self):
        """Extract colors from custom palette, using only index 0 for keying and last index in ranges."""
        # Validate custom_palette
        if not self.custom_palette or not isinstance(self.custom_palette, list):
            print("Warning: Invalid or empty custom_palette, using default colors")
            return [(128, 128, 128)] * 8  # Return default gray colors
        
        # Get the valid ranges for this fashion type
        char_num = self.char_id[3:] if self.char_id.startswith('chr') else self.char_id
        translator = IndexTranslator()
        ranges = translator.original_ranges.get(char_num, {}).get(self.fashion_type, [])
        
        editable_colors = []
        for r in ranges:
            for idx in range(r.start, r.stop - 1):  # Skip last index in each range
                if idx < len(self.custom_palette):
                    color = self.custom_palette[idx]
                    
                    # Validate color tuple
                    if not isinstance(color, (list, tuple)) or len(color) != 3:
                        print(f"Warning: Invalid color at index {idx}: {color}, using default")
                        color = (128, 128, 128)  # Default gray
                    else:
                        # Ensure color values are valid integers
                        try:
                            r_val, g_val, b_val = int(color[0]), int(color[1]), int(color[2])
                            if not (0 <= r_val <= 255 and 0 <= g_val <= 255 and 0 <= b_val <= 255):
                                print(f"Warning: Color values out of range at index {idx}: {color}, using default")
                                color = (128, 128, 128)  # Default gray
                            else:
                                color = (r_val, g_val, b_val)
                        except (ValueError, TypeError):
                            print(f"Warning: Invalid color values at index {idx}: {color}, using default")
                            color = (128, 128, 128)  # Default gray
                    
                    # Only skip if it's index 0 (keying color) or the last index in the range
                    if idx == 0:
                        continue  # Skip index 0 (keying color)
                    if idx == r.stop - 1:
                        continue  # Skip last index in range
                    # Include all other colors
                    editable_colors.append(color)
        
        # If no valid colors were extracted, provide defaults
        if not editable_colors:
            print("Warning: No valid colors extracted, using default colors")
            editable_colors = [(128, 128, 128)] * 8
        
        # Sort by brightness (darkest to lightest for consistent display)
        editable_colors.sort(key=lambda c: (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]), reverse=False)
        
        return editable_colors
    
    def _create_ui(self):
        """Create the user interface using grid-based palette editor like the live editor."""
        # Main frame with more padding
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text=f"Editing Icon Palette for {self.icon_handler._get_fashion_name(self.char_id, self.fashion_type)}", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 5))
        
        # Create paned window for split layout
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Controls and Palette grid (larger)
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=4)  # Increased weight for larger controls area
        
        # Add more padding to the right side of the left frame for better balance
        left_frame.configure(padding=(0, 0, 15, 0))
        
        # Color picker section with border (moved to left side)
        color_picker_frame = ttk.Frame(left_frame, relief="solid", borderwidth=1)
        color_picker_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(color_picker_frame, text="Color Picker", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5, 2))
        
        # Index display with Go button
        index_frame = ttk.Frame(color_picker_frame)
        index_frame.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(index_frame, text="Index:").pack(side=tk.LEFT)
        self.index_entry = ttk.Entry(index_frame, textvariable=self.index_var, width=8)
        self.index_entry.pack(side=tk.LEFT, padx=(5, 5))
        go_btn = ttk.Button(index_frame, text="Go", command=self._go_to_index)
        go_btn.pack(side=tk.LEFT)
        
        # Hex display with Apply button
        hex_frame = ttk.Frame(color_picker_frame)
        hex_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(hex_frame, text="Hex #RRGGBB:").pack(side=tk.LEFT)
        self.hex_entry = ttk.Entry(hex_frame, textvariable=self.hex_var, width=10)
        self.hex_entry.pack(side=tk.LEFT, padx=(5, 5))
        apply_btn = ttk.Button(hex_frame, text="Apply", command=self._apply_hex_color)
        apply_btn.pack(side=tk.LEFT)
        
        # Colorpicker button
        self.colorpicker_btn = ttk.Button(hex_frame, text="🎨 Pick", command=self._toggle_colorpicker)
        self.colorpicker_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Gradient button with rainbow colors (using tk.Button for colors)
        self.gradient_btn = tk.Button(hex_frame, text="🌈", command=self._open_gradient_menu,
                                    bg="#FF4081", activebackground="#E91E63", width=3, height=1,
                                    font=("Arial", 10, "bold"), relief="raised")
        self.gradient_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # HSV sliders
        
        # Hue slider
        hue_frame = ttk.Frame(color_picker_frame)
        hue_frame.pack(fill=tk.X, pady=1)
        ttk.Label(hue_frame, text="Hue:").pack(side=tk.LEFT)
        hue_scale = ttk.Scale(hue_frame, from_=0, to=360, variable=self.hue_var, 
                             command=self._on_color_change, orient=tk.HORIZONTAL)
        hue_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(hue_frame, textvariable=self.hue_var, width=4).pack(side=tk.RIGHT)
        
        # Saturation slider
        sat_frame = ttk.Frame(color_picker_frame)
        sat_frame.pack(fill=tk.X, pady=1)
        ttk.Label(sat_frame, text="Sat:").pack(side=tk.LEFT)
        sat_scale = ttk.Scale(sat_frame, from_=0, to=100, variable=self.sat_var,
                             command=self._on_color_change, orient=tk.HORIZONTAL)
        sat_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(sat_frame, textvariable=self.sat_var, width=4).pack(side=tk.RIGHT)
        
        # Value slider
        val_frame = ttk.Frame(color_picker_frame)
        val_frame.pack(fill=tk.X, pady=1)
        ttk.Label(val_frame, text="Val:").pack(side=tk.LEFT)
        val_scale = ttk.Scale(val_frame, from_=0, to=100, variable=self.val_var,
                             command=self._on_color_change, orient=tk.HORIZONTAL)
        val_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(val_frame, textvariable=self.val_var, width=4).pack(side=tk.RIGHT)
        
        # Color preview bar (smaller for left side) - ensure valid color
        try:
            preview_color = "#000000"  # Default black
            if self.current_colors and len(self.current_colors) > 0:
                first_color = self.current_colors[0]
                if isinstance(first_color, (list, tuple)) and len(first_color) >= 3:
                    r, g, b = int(first_color[0]), int(first_color[1]), int(first_color[2])
                    r = max(0, min(255, r))
                    g = max(0, min(255, g))
                    b = max(0, min(255, b))
                    preview_color = f"#{r:02x}{g:02x}{b:02x}"
        except (ValueError, TypeError, IndexError):
            preview_color = "#000000"  # Default black
        
        self.color_preview = tk.Frame(color_picker_frame, width=200, height=30, bg=preview_color, relief=tk.SUNKEN, bd=2)
        self.color_preview.pack(pady=5)
        
        # Multi-select controls (moved below color picker)
        multi_frame = ttk.Frame(left_frame)
        multi_frame.pack(fill=tk.X, pady=(0, 5))
        
        multi_check = ttk.Checkbutton(multi_frame, text="Multi-select", variable=self.multi_select_var)
        multi_check.pack(side=tk.LEFT)
        
        inverse_check = ttk.Checkbutton(multi_frame, text="Inverse order", variable=self.inverse_order_var, command=self._on_inverse_order_changed)
        inverse_check.pack(side=tk.LEFT, padx=(10, 0))
        
        clear_sel_btn = ttk.Button(multi_frame, text="Clear Sel", command=self._clear_selection)
        clear_sel_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        self.selection_count_var = tk.StringVar(value="(0 selected)")
        selection_label = ttk.Label(multi_frame, textvariable=self.selection_count_var)
        selection_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Palette grid label with load/save buttons
        header_frame = ttk.Frame(left_frame)
        header_frame.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(header_frame, text="Icon Palette Colors", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Load Icon Colors", command=self._load_saved_colors).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(header_frame, text="Save Icon Colors", command=self._save_colors).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Create a container frame for canvas and scrollbar (limited height for 3 rows max)
        canvas_container = ttk.Frame(left_frame)
        canvas_container.pack(fill=tk.X, pady=(0, 5))  # Changed from expand=True to fill=tk.X
        
        # Create canvas for palette grid inside the container (reduced by 40px from 330)
        self.palette_canvas = tk.Canvas(canvas_container, highlightthickness=0, height=290)  # Reduced by 40px for more compact UI
        palette_scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.palette_canvas.yview)
        self.palette_canvas.configure(yscrollcommand=palette_scrollbar.set)
        
        # Create frame inside canvas for palette squares
        self.palette_frame = ttk.Frame(self.palette_canvas)
        self.palette_canvas.create_window((0, 0), window=self.palette_frame, anchor="nw")
        
        # Pack canvas and scrollbar in the container
        self.palette_canvas.pack(side="left", fill=tk.BOTH, expand=True)
        palette_scrollbar.pack(side="right", fill="y")
        
        # Bind canvas resize event to update grid layout
        self.palette_canvas.bind("<Configure>", self._on_canvas_resize)
        
        # Create palette squares for the editable colors
        self.palette_squares = []
        self._create_palette_grid()
        
        # Right side - Preview, dropdown, and saved colors
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)  # Reduced weight for smaller preview area
        
        # Preview section - centered and larger
        preview_header_frame = ttk.Frame(right_frame)
        preview_header_frame.pack(fill=tk.X, pady=(0, 1))
        
        ttk.Label(preview_header_frame, text="Live Preview", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        ttk.Label(preview_header_frame, text="(Click to select color, scroll to zoom)", font=("Arial", 8), foreground="gray").pack(anchor=tk.W)
        
        # Create a container frame for the preview with minimal padding
        preview_container = ttk.Frame(right_frame)
        preview_container.pack(fill=tk.BOTH, expand=True, pady=(0, 2), padx=(1, 1))
        
        # Center the preview label within the container
        self.preview_label = ttk.Label(preview_container, text="Loading preview...")
        self.preview_label.pack(expand=True)  # No internal padding to avoid cutting off the image
        
        # Bind click event to preview for color selection/colorpicking
        self.preview_label.bind("<Button-1>", self._on_preview_click)
        
        # Bind mouse wheel for zooming
        self.preview_label.bind("<MouseWheel>", self._on_preview_zoom)
        
        # Change cursor to indicate clickability
        self.preview_label.bind("<Enter>", lambda e: self.preview_label.configure(cursor="hand2"))
        self.preview_label.bind("<Leave>", lambda e: self.preview_label.configure(cursor=""))
        
        # Edit which palette dropdown (kept under preview as requested)
        edit_frame = ttk.Frame(right_frame)
        edit_frame.pack(fill=tk.X, pady=(1, 1))  # Minimal vertical padding
        ttk.Label(edit_frame, text="Edit which:").pack(side=tk.LEFT)
        
        # Populate dropdown with all active palettes
        palette_options = []
        current_palette_name = f"{self.icon_handler._get_fashion_name(self.char_id, self.fashion_type)} — {os.path.basename(self.palette_path)}"
        
        if self.palette_layers:
            active_layers = [ly for ly in self.palette_layers if getattr(ly, "active", False)]
            for layer in active_layers:
                if hasattr(layer, 'name') and hasattr(layer, 'palette_type'):
                    # Skip hair layers - don't include them in the dropdown
                    if layer.palette_type == 'hair':
                        continue
                    
                    # Extract character and fashion info from layer name
                    import re
                    char_match = re.search(r'(?:chr)?(\d{3})', layer.name)
                    if char_match:
                        char_id = f"chr{char_match.group(1).zfill(3)}"
                        fashion_name = self.icon_handler._get_fashion_name(char_id, layer.palette_type)
                        palette_options.append(f"{fashion_name} — {layer.name}")
        
        # If no active layers found, just show current palette
        if not palette_options:
            palette_options = [current_palette_name]
        
        # Determine if dropdown should be disabled (when opened from live editor or quicksave mode)
        dropdown_state = "disabled" if (self.live_editor_window or self.is_quicksave_mode) else "readonly"
        
        self.edit_var = tk.StringVar(value=current_palette_name)
        self.edit_combo = ttk.Combobox(edit_frame, textvariable=self.edit_var, values=palette_options, state=dropdown_state, width=35)
        self.edit_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.edit_combo.bind("<<ComboboxSelected>>", self._on_palette_selected)
        
        # Saved Colors section (moved to right side)
        ttk.Label(right_frame, text="Saved Colors", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(2, 1))
        
        # Saved colors buttons
        saved_btn_frame = ttk.Frame(right_frame)
        saved_btn_frame.pack(fill=tk.X, pady=(0, 1))
        ttk.Button(saved_btn_frame, text="Save", command=self._save_color).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(saved_btn_frame, text="Load", command=self._load_color).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(saved_btn_frame, text="Clear", command=self._clear_saved_colors).pack(side=tk.LEFT, padx=(0, 5))
        self.saved_mode_button = ttk.Button(saved_btn_frame, text="L", command=self._toggle_saved_mode, width=3)
        self.saved_mode_button.pack(side=tk.RIGHT)
        
        # Saved colors instructions on one line (dynamic based on mode)
        self.saved_instructions_label = ttk.Label(right_frame, text="Left click below to save color / Right click above to apply color", font=("Arial", 8))
        self.saved_instructions_label.pack(anchor=tk.W, pady=(0, 1))
        
        # Saved colors grid
        self.saved_colors_frame = ttk.Frame(right_frame)
        self.saved_colors_frame.pack(fill=tk.X, pady=(0, 1))
        self._create_saved_colors_grid()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_frame, text="Export as Icon", command=self._export_icon).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Reset to Original", command=self._reset_colors).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Close", command=self._close_editor).pack(side=tk.RIGHT)
        
        # Initialize UI
        self._update_color_picker()
        self._update_preview()
    
    def _create_palette_grid(self):
        """Create the palette grid showing only the editable colors."""
        # Clear existing squares
        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        self.palette_squares = []
        
        # Display all available colors (no limit)
        colors_to_display = self.current_colors
        
        # Get canvas width to calculate how many columns fit
        self.palette_canvas.update_idletasks()
        canvas_width = self.palette_canvas.winfo_width()
        if canvas_width <= 1:  # Canvas not yet sized
            canvas_width = 400  # Default width
        
        # Account for scrollbar width (typically ~17px)
        scrollbar_width = 17
        available_canvas_width = canvas_width - scrollbar_width
        
        # Calculate square size (2.5x larger: 32 * 2.5 = 80x80) and minimal padding
        square_size = 80
        padding = 2
        total_square_width = square_size + (padding * 2)
        
        # Fixed 5 columns per row
        cols = 5
        
        # Use the full available width - let it span the entire length
        # All colors will be displayed with scrolling for overflow
        
        # No centering - let the grid span the full width
        left_padding = 0
        
        # Create a grid of color squares with 5 columns (unlimited rows with scrolling)
        for i, color in enumerate(colors_to_display):
            row = i // cols
            col = i % cols
            
            # No row limit - scrollbar will handle overflow
            
            # Create color square (2x bigger)
            square = tk.Canvas(self.palette_frame, width=square_size, height=square_size, 
                             highlightthickness=1, highlightbackground="black")
            
            # Apply left padding to first column for alignment
            if col == 0:
                square.grid(row=row, column=col, padx=(left_padding + padding, padding), pady=padding)
            else:
                square.grid(row=row, column=col, padx=padding, pady=padding)
            
            # Fill with color - validate color values first
            try:
                r, g, b = int(color[0]), int(color[1]), int(color[2])
                # Ensure values are within valid range
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
            except (ValueError, TypeError, IndexError):
                print(f"Warning: Invalid color {color} at index {i}, using default gray")
                hex_color = "#808080"  # Default gray
            
            square.create_rectangle(0, 0, square_size, square_size, fill=hex_color, outline="black")
            
            # Bind click events for left and right click
            square.bind("<Button-1>", lambda e, idx=i: self._on_palette_square_click(idx, "left", e.state))
            square.bind("<Button-3>", lambda e, idx=i: self._on_palette_square_click(idx, "right", e.state))
            
            # Store reference
            self.palette_squares.append(square)
        
        # Update canvas scroll region
        self.palette_frame.update_idletasks()
        self.palette_canvas.configure(scrollregion=self.palette_canvas.bbox("all"))
        
        # Select first color by default
        if self.palette_squares:
            self._select_color(0, "left", 0)
    
    def _on_canvas_resize(self, event):
        """Handle canvas resize to update grid layout."""
        # Don't recreate grid if we're currently updating selection
        if self._updating_selection:
            return
            
        # Only recreate grid if canvas width actually changed significantly
        if hasattr(self, '_last_canvas_width') and abs(self._last_canvas_width - event.width) < 10:
            return
        
        self._last_canvas_width = event.width
        # Recreate the palette grid with new dimensions
        self._create_palette_grid()
    
    def _select_color(self, index, button, state):
        """Select a color in the palette grid."""
        # Prevent clicks during palette switching to avoid cross-palette contamination
        current_time = time.time()
        switch_time = getattr(self, '_palette_switch_time', 0)
        if current_time - switch_time < 0.1:  # 100ms debounce for clicks
            return
        
        shift_pressed = bool(state & 0x1)  # Check if Shift key is pressed
        
        # Ensure index is within bounds of current_colors (not just displayed colors)
        if index >= len(self.current_colors):
            return
        
        # Set flag to prevent grid recreation during selection updates
        self._updating_selection = True
        
        if button == "left":
            if shift_pressed and self.multi_select_var.get():
                # Shift+click: select range from last selected to current
                if self.selected_indices:
                    last_selected = max(self.selected_indices)
                    start_idx = min(last_selected, index)
                    end_idx = max(last_selected, index)
                    for i in range(start_idx, end_idx + 1):
                        if i < len(self.current_colors):  # Ensure within bounds
                            self.selected_indices.add(i)
                else:
                    self.selected_indices.add(index)
                # Always update selected_index to the clicked color
                self.selected_index = index
            elif self.multi_select_var.get():
                # Multi-select mode (regular click)
                if index in self.selected_indices:
                    self.selected_indices.remove(index)
                else:
                    self.selected_indices.add(index)
                # Always update selected_index to the clicked color
                self.selected_index = index
            else:
                # Single select mode
                self.selected_indices = {index}
                self.selected_index = index
        elif button == "right":
            # Right click - apply saved color from first non-empty slot
            # Find first non-empty saved color
            for i, saved_color in enumerate(self.saved_colors):
                if saved_color != (0, 0, 0):  # Not empty (black)
                    # Apply the saved color to the clicked square
                    self.current_colors[index] = saved_color
                    # Update the visual square (only if it's displayed)
                    if index < len(self.palette_squares):
                        square = self.palette_squares[index]
                        hex_color = f"#{saved_color[0]:02x}{saved_color[1]:02x}{saved_color[2]:02x}"
                        square.delete("all")
                        square.create_rectangle(0, 0, 80, 80, fill=hex_color, outline="black")
                    # Update color picker if this is the selected color
                    if index == self.selected_index:
                        self._update_color_picker()
                    # Update live preview
                    self._update_preview()
                    break
        
        # Always update color picker to show the most recently clicked color
        self._update_color_picker()
        
        # Update selection highlights (only for displayed squares)
        # Keep highlightthickness consistent to prevent grid movement
        for i, square in enumerate(self.palette_squares):
            if i in self.selected_indices:
                square.configure(highlightbackground="red", highlightthickness=1)
            else:
                square.configure(highlightbackground="black", highlightthickness=1)
        
        # Update selection count
        count = len(self.selected_indices)
        self.selection_count_var.set(f"({count} selected)")
        
        # Clear the flag to allow grid recreation again
        self._updating_selection = False
    
    def _refresh_selection_highlights(self):
        """Refresh the selection highlights for all palette squares."""
        # Update selection highlights (only for displayed squares)
        # Keep highlightthickness consistent to prevent grid movement
        for i, square in enumerate(self.palette_squares):
            if i in self.selected_indices:
                square.configure(highlightbackground="red", highlightthickness=1)
            else:
                square.configure(highlightbackground="black", highlightthickness=1)
    
    def _update_color_picker(self):
        """Update the color picker with the selected color."""
        if self.selected_index < len(self.current_colors):
            color = self.current_colors[self.selected_index]
            
            # Update index and hex display
            self.index_var.set(str(self.selected_index))
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            self.hex_var.set(hex_color)
            
            # Convert RGB to HSV
            import colorsys
            h, s, v = colorsys.rgb_to_hsv(color[0]/255.0, color[1]/255.0, color[2]/255.0)
            
            # Update sliders (without triggering change event)
            self.hue_var.set(int(h * 360))
            self.sat_var.set(int(s * 100))
            self.val_var.set(int(v * 100))
            
            # Update color preview (only if it exists)
            if self.color_preview is not None:
                self.color_preview.configure(bg=hex_color)
    
    def _on_color_change(self, value=None):
        """Handle color picker changes - apply HSV shifts to selected colors only."""
        if not self.selected_indices:
            return
        
        # Prevent color changes during palette switching to avoid cross-palette contamination
        if getattr(self, '_updating_selection', False):
            return
        
        # Additional protection: Check if we just switched palettes recently (debounce)
        current_time = time.time()
        switch_time = getattr(self, '_palette_switch_time', 0)
        if current_time - switch_time < 0.2:  # 200ms debounce
            return
        
        # Verify we're still on the same palette to prevent cross-contamination
        current_name = self.edit_var.get()
        if hasattr(self, '_current_palette_name') and current_name != self._current_palette_name:
            return
            
        import colorsys
        
        H_new = int(self.hue_var.get())
        S_new = int(self.sat_var.get())
        V_new = int(self.val_var.get())
        
        targets = sorted(self.selected_indices)
        use_relative = self.multi_select_var.get() and len(targets) > 1
        
        if use_relative:
            # Use relative HSV shifts like the live palette editor
            base_i = self.selected_index
            br, bg, bb = self.current_colors[base_i]
            bh, bs, bv = colorsys.rgb_to_hsv(br/255.0, bg/255.0, bb/255.0)
            bh = int(round(bh * 360))
            bs = int(round(bs * 100))
            bv = int(round(bv * 100))
            
            dH = H_new - bh
            EPS = 1  # treat <=1% as zero-ish to avoid stuck scaling
            use_scaleS = bs > EPS
            use_scaleV = bv > EPS
            scaleS = (S_new/100.0) / (bs/100.0) if use_scaleS else None
            scaleV = (V_new/100.0) / (bv/100.0) if use_scaleV else None
            dS = (S_new - bs) if not use_scaleS else 0
            dV = (V_new - bv) if not use_scaleV else 0
        else:
            dH = 0; scaleS = 1.0; scaleV = 1.0; dS = 0; dV = 0
        
        for idx in targets:
            if idx < len(self.current_colors):
                r, g, b = self.current_colors[idx]
                h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                h = int(round(h * 360)); s = int(round(s * 100)); v = int(round(v * 100))
                
                if use_relative:
                    h = (h + dH) % 360
                    EPS_TGT = 2
                    # Saturation per-swatch: additive if target near zero or scale unavailable; else multiplicative
                    if s <= EPS_TGT or scaleS is None:
                        s = max(0, min(100, int(round(s + dS))))
                    else:
                        s = max(0, min(100, int(round(s * scaleS))))
                    # Value per-swatch: additive if target near zero or scale unavailable; else multiplicative
                    if v <= EPS_TGT or scaleV is None:
                        v = max(0, min(100, int(round(v + dV))))
                    else:
                        v = max(0, min(100, int(round(v * scaleV))))
                else:
                    h, s, v = H_new % 360, max(0, min(100, S_new)), max(0, min(100, V_new))
                
                # Skip if current color is keyed
                current_color = self.current_colors[idx]
                if (self.is_universal_keying_color(current_color) or 
                    current_color == (255, 0, 255) or  # Magenta
                    (hasattr(self, 'is_chr003_keying_color') and self.is_chr003_keying_color(current_color)) or  # Sheep
                    (hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(current_color)) or  # Raccoon
                    (hasattr(self, 'is_chr011_keying_color') and self.is_chr011_keying_color(current_color)) or  # Sheep 2nd Job
                    (hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(current_color)) or  # Lion 2nd Job
                    (hasattr(self, 'is_palette_keying_color') and self.is_palette_keying_color(current_color, idx, self.char_id))):  # Any other character-specific rules
                    continue

                rr, gg, bb = colorsys.hsv_to_rgb((h % 360)/360.0, s/100.0, v/100.0)
                rr, gg, bb = int(round(rr*255)), int(round(gg*255)), int(round(bb*255))
                
                # Check if new color would be a keying color
                candidate_color = (rr, gg, bb)
                if (self.is_universal_keying_color(candidate_color) or 
                    candidate_color == (255, 0, 255) or  # Magenta
                    (hasattr(self, 'is_chr003_keying_color') and self.is_chr003_keying_color(candidate_color)) or  # Sheep
                    (hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(candidate_color)) or  # Raccoon
                    (hasattr(self, 'is_chr011_keying_color') and self.is_chr011_keying_color(candidate_color)) or  # Sheep 2nd Job
                    (hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(candidate_color)) or  # Lion 2nd Job
                    (hasattr(self, 'is_palette_keying_color') and self.is_palette_keying_color(candidate_color, idx, self.char_id))):  # Any other character-specific rules
                    candidate_color = self._find_nearest_non_keyed_color(candidate_color)
                    rr, gg, bb = candidate_color
                
                self.current_colors[idx] = (rr, gg, bb)
                
                # Update temp cache with the new colors
                current_palette_key = f"{self.char_id}_{self.fashion_type}"
                if hasattr(self, '_temp_palette_cache'):
                    self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
                
                # Update the palette square (only if it's displayed)
                if idx < len(self.palette_squares):
                    square = self.palette_squares[idx]
                    hex_color = f"#{rr:02x}{gg:02x}{bb:02x}"
                    square.delete("all")
                    # Use the same size as in _create_palette_grid (80x80)
                    square.create_rectangle(0, 0, 80, 80, fill=hex_color, outline="black")
        
        # Update hex display with the focused color
        focus = self.selected_index
        if focus < len(self.current_colors):
            fr, fg, fb = self.current_colors[focus]
            hex_color = f"#{fr:02x}{fg:02x}{fb:02x}"
            self.hex_var.set(hex_color)
            
            # Update color preview (only if it exists)
            if self.color_preview is not None:
                self.color_preview.configure(bg=hex_color)
        
        # Update live preview
        self._update_preview()
        
        # Refresh selection highlights to ensure they persist after color changes
        self._refresh_selection_highlights()
    
    def _on_inverse_order_changed(self):
        """Handle inverse order checkbox change."""
        # Update the preview immediately when inverse order is toggled
        self._update_preview()
    
    def _close_editor(self):
        """Close the editor and clean up the instance."""
        # Clean up temporary cache
        if hasattr(self, '_temp_palette_cache'):
            delattr(self, '_temp_palette_cache')
        if hasattr(self, '_original_palettes'):
            delattr(self, '_original_palettes')
        
        from icon_handler import IconHandler
        IconHandler._icon_editor_instance = None
        self.window.destroy()
    
    def _bring_to_front(self):
        """Bring the icon editor window to the front with multiple methods for reliability across platforms."""
        try:
            if self.window and self.window.winfo_exists():
                import platform
                system = platform.system().lower()
                
                # Common methods that work on both platforms
                self.window.deiconify()  # Ensure window is not minimized
                self.window.lift()  # Bring to front in stacking order
                
                if system == "windows":
                    # Windows-specific focus handling
                    self.window.focus_force()  # Force keyboard focus
                    self.window.attributes('-topmost', True)  # Temporarily make topmost
                    self.window.after(100, lambda: self.window.attributes('-topmost', False))  # Remove topmost after 100ms
                    
                    # Additional Windows focus methods
                    try:
                        self.window.wm_attributes('-topmost', 1)
                        self.window.after(10, lambda: self.window.wm_attributes('-topmost', 0))
                    except:
                        pass
                        
                elif system == "linux":
                    # Linux-specific focus handling
                    self.window.focus_set()  # Set focus (gentler than focus_force)
                    self.window.tkraise()  # Raise window in stacking order
                    
                    # Try to activate the window (X11 specific)
                    try:
                        self.window.wm_attributes('-topmost', True)
                        self.window.after(50, lambda: self.window.wm_attributes('-topmost', False))
                    except:
                        pass
                        
                    # Additional method for some Linux window managers
                    try:
                        self.window.focus()
                    except:
                        pass
                        
                else:
                    # Fallback for other systems (macOS, etc.)
                    self.window.focus_set()
                    self.window.tkraise()
                
        except Exception as e:
            pass
    
    def _show_auto_close_warning(self, title, message):
        """Show a warning dialog that automatically closes after 7 seconds."""
        import tkinter as tk
        from tkinter import messagebox
        
        # Create a custom dialog
        dialog = tk.Toplevel(self.window)
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog on the parent window
        dialog.update_idletasks()
        parent_x = self.window.winfo_x()
        parent_y = self.window.winfo_y()
        parent_width = self.window.winfo_width()
        parent_height = self.window.winfo_height()
        
        dialog_width = 400
        dialog_height = 150
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Create content
        tk.Label(dialog, text=message, wraplength=350, justify="center").pack(pady=20)
        
        # Add countdown label
        countdown_label = tk.Label(dialog, text="This dialog will close automatically in 7 seconds...", 
                                 font=("Arial", 8), fg="gray")
        countdown_label.pack(pady=(0, 10))
        
        # Add OK button
        ok_button = tk.Button(dialog, text="OK", command=dialog.destroy, width=10)
        ok_button.pack(pady=(0, 10))
        
        # Auto-close functionality
        def countdown(seconds_left):
            if seconds_left > 0:
                countdown_label.config(text=f"This dialog will close automatically in {seconds_left} seconds...")
                dialog.after(1000, lambda: countdown(seconds_left - 1))
            else:
                dialog.destroy()
        
        # Start countdown
        countdown(7)
        
        # Bring dialog to front
        dialog.lift()
        dialog.focus_set()
    
    def _center_window_on_parent(self):
        """Center the icon editor window on its parent window."""
        try:
            if self.live_editor_window and self.live_editor_window.winfo_exists():
                # Get actual window dimensions after content is rendered
                window_width = self.window.winfo_width()
                window_height = self.window.winfo_height()
                
                # Get the live editor's position and dimensions
                parent_x = self.live_editor_window.winfo_x()
                parent_y = self.live_editor_window.winfo_y()
                parent_width = self.live_editor_window.winfo_width()
                parent_height = self.live_editor_window.winfo_height()
                
                # Calculate center position relative to parent
                x = parent_x + (parent_width - window_width) // 2
                y = parent_y + (parent_height - window_height) // 2
                
                # Set the window position (keep current size)
                self.window.geometry(f"+{x}+{y}")
            else:
                # If no live editor, center on screen
                window_width = self.window.winfo_width()
                window_height = self.window.winfo_height()
                screen_width = self.window.winfo_screenwidth()
                screen_height = self.window.winfo_screenheight()
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                self.window.geometry(f"+{x}+{y}")
        except Exception as e:
            # Fallback to center on screen
            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            self.window.geometry(f"+{x}+{y}")
    
    def _on_palette_selected(self, event=None):
        """Handle palette selection from dropdown."""
        selected_text = self.edit_var.get()
        
        # Save current palette's temporary changes to cache before switching
        if hasattr(self, '_temp_palette_cache'):
            old_palette_key = f"{self.char_id}_{self.fashion_type}"
            if old_palette_key not in self._temp_palette_cache:
                # Initialize with original colors if not yet cached
                self._temp_palette_cache[old_palette_key] = self.current_colors.copy()
                self._original_palettes[old_palette_key] = self.editable_colors.copy()
            else:
                # Save current state to temp cache
                self._temp_palette_cache[old_palette_key] = self.current_colors.copy()
        
        # Set protection flags to prevent rapid switching issues
        self._updating_selection = True
        self._palette_switch_time = time.time()
        self._current_palette_name = selected_text
        
        # Find the corresponding layer
        if self.palette_layers:
            active_layers = [ly for ly in self.palette_layers if getattr(ly, "active", False)]
            for layer in active_layers:
                if hasattr(layer, 'name') and hasattr(layer, 'palette_type'):
                    import re
                    char_match = re.search(r'(?:chr)?(\d{3})', layer.name)
                    if char_match:
                        char_id = f"chr{char_match.group(1).zfill(3)}"
                        fashion_name = self.icon_handler._get_fashion_name(char_id, layer.palette_type)
                        layer_name = f"{fashion_name} — {layer.name}"
                        
                        if layer_name == selected_text:
                            # Switch to this palette
                            self.char_id = char_id
                            self.fashion_type = layer.palette_type
                            
                            # Get new icon paths for the selected character/fashion type
                            item_name = self.icon_handler._get_fashion_name(char_id, layer.palette_type)
                            self.png_path, self.ref_pal_path = self.icon_handler._get_icon_paths(char_id, item_name)
                            
                            # Load the new reference palette
                            self._load_reference_palette()
                            
                            # Check if this specific palette was exported/saved
                            # Look for a saved .pal file that matches this character and fashion type
                            import os
                            exports_dir = os.path.join(self.icon_handler.root_dir, "exports", "custom_pals", "fashion")
                            
                            # Try multiple filename patterns that might match this character/fashion combination
                            possible_filenames = []
                            
                            # Pattern 1: chr###_w#.pal (standard fashion palette format)
                            if layer.palette_type.startswith('fashion_'):
                                fashion_num = layer.palette_type.split('_')[1]
                                possible_filenames.append(f"{char_id}_w{fashion_num}.pal")
                            
                            # Pattern 2: chr###_#.pal (hair palette format)
                            if layer.palette_type == 'hair':
                                # Extract hair number from layer name if possible
                                hair_match = re.search(r'_(\d+)\.pal', layer.name)
                                if hair_match:
                                    hair_num = hair_match.group(1)
                                    possible_filenames.append(f"{char_id}_{hair_num}.pal")
                            
                            # Pattern 3: Generic chr###_palette_type.pal format
                            possible_filenames.append(f"{char_id}_{layer.palette_type}.pal")
                            
                            # Pattern 4: Look for any palette file that contains the character ID and matches the layer name
                            if os.path.exists(exports_dir):
                                for filename in os.listdir(exports_dir):
                                    if filename.lower().endswith('.pal') and char_id in filename.lower():
                                        # Check if this palette file corresponds to the current layer
                                        # by examining the layer name for matching patterns
                                        base_layer_name = os.path.splitext(layer.name)[0]  # Remove .pal extension
                                        if base_layer_name.lower() in filename.lower():
                                            possible_filenames.append(filename)
                            
                            # Try to find the first existing saved palette
                            saved_palette_path = None
                            for filename in possible_filenames:
                                test_path = os.path.join(exports_dir, filename)
                                if os.path.exists(test_path):
                                    saved_palette_path = test_path
                                    break
                            
                            if saved_palette_path:
                                # Validate that this saved palette truly matches the selected fashion and character
                                saved_filename = os.path.basename(saved_palette_path)
                                is_valid_match = self._validate_palette_match(saved_filename, char_id, layer.palette_type, layer.name)
                                
                                if is_valid_match:
                                    # Use the saved palette colors
                                    try:
                                        with open(saved_palette_path, 'rb') as f:
                                            pal_data = f.read()
                                        
                                        # Parse the saved palette
                                        saved_palette = []
                                        for i in range(0, len(pal_data), 3):
                                            if i + 2 < len(pal_data):
                                                r, g, b = pal_data[i], pal_data[i+1], pal_data[i+2]
                                                saved_palette.append((r, g, b))
                                        
                                        self.custom_palette = saved_palette
                                    except Exception as e:
                                        # Fallback to layer colors
                                        self.custom_palette = layer.colors if hasattr(layer, 'colors') else []
                                else:
                                    print(f"Saved palette {saved_filename} does not match current selection, using layer colors")
                                    self.custom_palette = layer.colors if hasattr(layer, 'colors') else []
                            else:
                                # No saved palette found, load the vanilla palette for this specific fashion item
                                print(f"No saved palette found for {char_id} {layer.palette_type}, loading vanilla palette for this item")
                                # Load the vanilla palette file for this specific character and fashion type
                                vanilla_palette = self._load_vanilla_palette_for_item(char_id, layer.palette_type, layer.name)
                                if vanilla_palette:
                                    self.custom_palette = vanilla_palette
                                else:
                                    # Fallback to layer colors if vanilla palette can't be loaded
                                    self.custom_palette = layer.colors if hasattr(layer, 'colors') else []
                                    print(f"Fallback to layer colors")
                            
                            # Extract editable colors and update the editable_colors attribute
                            self.editable_colors = self._extract_editable_colors()
                            
                            # Check if we have cached temporary changes for this palette
                            new_palette_key = f"{char_id}_{layer.palette_type}"
                            if hasattr(self, '_temp_palette_cache') and new_palette_key in self._temp_palette_cache:
                                # Restore from temp cache to preserve temporary changes
                                self.current_colors = self._temp_palette_cache[new_palette_key].copy()
                            else:
                                # Use the extracted colors and add to cache
                                self.current_colors = self.editable_colors.copy()
                                if hasattr(self, '_temp_palette_cache'):
                                    self._temp_palette_cache[new_palette_key] = self.current_colors.copy()
                                    self._original_palettes[new_palette_key] = self.editable_colors.copy()
                            
                            # Store the current palette key
                            self._last_palette_key = f"{char_id}_{layer.palette_type}"
                            
                            # Refresh the UI completely
                            
                            # Reset selection state
                            self.selected_index = 0
                            self.selected_indices = set()
                            
                            # Force a complete UI refresh
                            self._create_palette_grid()
                            self._update_color_picker()
                            self._update_preview()
                            
                            # Force window update
                            self.window.update_idletasks()
                            
                            # Update window title
                            self.window.title(f"Icon Palette Editor - {item_name}")
                            
                            # Clear protection flags after successful switch with delay
                            self._clear_protection_flags()
                            return  # Exit after successful switch
                            
        print(f"DEBUG: No matching layer found for selection: {selected_text}")
        # Clear protection flags even if no match found
        self._clear_protection_flags()
    
    def _clear_protection_flags(self):
        """Clear protection flags after a delay to ensure palette switching is complete"""
        def clear_flags():
            self._updating_selection = False
            self._current_palette_name = getattr(self, '_current_palette_name', None)
        
        # Use a delay to ensure all UI updates are complete before allowing color changes
        try:
            self.window.after(250, clear_flags)  # 250ms delay
        except:
            # Fallback if window doesn't exist
            clear_flags()
    
    def _validate_palette_match(self, saved_filename: str, char_id: str, palette_type: str, layer_name: str) -> bool:
        """
        Validate that a saved palette file truly matches the selected character and fashion type.
        
        Args:
            saved_filename: Name of the saved palette file (e.g., "chr001_w7.pal")
            char_id: Character ID (e.g., "chr001")
            palette_type: Palette type (e.g., "fashion_1", "hair")
            layer_name: Full layer name (e.g., "chr001_w7.pal")
            
        Returns:
            True if the saved palette matches the current selection, False otherwise
        """
        import re
        import os
        
        # Extract character from saved filename
        saved_char_match = re.search(r'(chr\d{3})', saved_filename.lower())
        if not saved_char_match:
            return False
        saved_char_id = saved_char_match.group(1)
        
        # Character must match exactly
        if saved_char_id != char_id.lower():
            print(f"Character mismatch: saved={saved_char_id}, current={char_id.lower()}")
            return False
        
        # For fashion palettes, check the fashion number
        if palette_type.startswith('fashion_'):
            expected_fashion_num = palette_type.split('_')[1]
            
            # Check if saved filename follows chr###_w#.pal pattern
            fashion_match = re.search(r'_w(\d+)\.pal$', saved_filename.lower())
            if fashion_match:
                saved_fashion_num = fashion_match.group(1)
                if saved_fashion_num == expected_fashion_num:
                    return True
                else:
                    print(f"Fashion number mismatch: saved=w{saved_fashion_num}, expected=w{expected_fashion_num}")
                    return False
        
        # For hair palettes, check the hair number
        elif palette_type == 'hair':
            # Extract hair number from layer name
            layer_hair_match = re.search(r'_(\d+)\.pal', layer_name)
            if layer_hair_match:
                expected_hair_num = layer_hair_match.group(1)
                
                # Check if saved filename follows chr###_#.pal pattern (hair)
                saved_hair_match = re.search(r'_(\d+)\.pal$', saved_filename.lower())
                if saved_hair_match:
                    saved_hair_num = saved_hair_match.group(1)
                    if saved_hair_num == expected_hair_num:
                        return True
                    else:
                        print(f"Hair number mismatch: saved=_{saved_hair_num}, expected=_{expected_hair_num}")
                        return False
        
        # For other palette types, do a more general match
        else:
            # Check if the layer name (without extension) is contained in the saved filename
            base_layer_name = os.path.splitext(layer_name)[0].lower()
            base_saved_name = os.path.splitext(saved_filename)[0].lower()
            
            if base_layer_name == base_saved_name:
                return True
            else:
                print(f"Generic name mismatch: saved={base_saved_name}, expected={base_layer_name}")
                return False
        
        print(f"No match found for {saved_filename} with {char_id} {palette_type}")
        return False
    
    def refresh_dropdown_options(self):
        """Refresh the Edit Which dropdown options based on current palette layers."""
        if not hasattr(self, 'edit_combo') or not self.edit_combo:
            return
        
        # Populate dropdown with all active palettes
        palette_options = []
        current_palette_name = f"{self.icon_handler._get_fashion_name(self.char_id, self.fashion_type)} — {os.path.basename(self.palette_path)}"
        
        if self.palette_layers:
            active_layers = [ly for ly in self.palette_layers if getattr(ly, "active", False)]
            for layer in active_layers:
                if hasattr(layer, 'name') and hasattr(layer, 'palette_type'):
                    # Skip hair layers - don't include them in the dropdown
                    if layer.palette_type == 'hair':
                        continue
                    
                    # Extract character and fashion info from layer name
                    import re
                    char_match = re.search(r'(?:chr)?(\d{3})', layer.name)
                    if char_match:
                        char_id = f"chr{char_match.group(1).zfill(3)}"
                        fashion_name = self.icon_handler._get_fashion_name(char_id, layer.palette_type)
                        palette_options.append(f"{fashion_name} — {layer.name}")
        
        # If no active layers found, just show current palette
        if not palette_options:
            palette_options = [current_palette_name]
        
        # Update the combobox values
        self.edit_combo.configure(values=palette_options)
        
        # Update the current selection if it's no longer valid
        current_selection = self.edit_var.get()
        if current_selection not in palette_options and palette_options:
            self.edit_var.set(palette_options[0])
        
    
    def _load_vanilla_palette_for_item(self, char_id: str, palette_type: str, layer_name: str):
        """Load the vanilla palette file for a specific character and fashion type."""
        import os
        import re
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        vanilla_fashion_dir = os.path.join(script_dir, "nonremovable_assets", "vanilla_pals", "fashion")
        
        # Try to find the vanilla palette file that matches this layer
        if os.path.exists(vanilla_fashion_dir):
            # Extract the base name from the layer name (e.g., "chr001_w12.pal" -> "chr001_w12")
            base_layer_name = os.path.splitext(layer_name)[0] if layer_name.endswith('.pal') else layer_name
            
            # Look for a matching vanilla palette file
            for filename in os.listdir(vanilla_fashion_dir):
                if filename.lower().endswith('.pal'):
                    base_filename = os.path.splitext(filename)[0]
                    if base_filename.lower() == base_layer_name.lower():
                        vanilla_path = os.path.join(vanilla_fashion_dir, filename)
                        
                        try:
                            with open(vanilla_path, 'rb') as f:
                                pal_data = f.read()
                            
                            # Parse the vanilla palette
                            vanilla_palette = []
                            for i in range(0, len(pal_data), 3):
                                if i + 2 < len(pal_data):
                                    r, g, b = pal_data[i], pal_data[i+1], pal_data[i+2]
                                    vanilla_palette.append((r, g, b))
                            
                            return vanilla_palette
                        except Exception as e:
                            print(f"Error loading vanilla palette {vanilla_path}: {e}")
                            continue
        
        print(f"DEBUG: No vanilla palette found for {char_id} {palette_type} ({layer_name})")
        return None
    
    def update_palette_layers(self, new_palette_layers):
        """Update the palette layers and refresh the dropdown."""
        self.palette_layers = new_palette_layers or []
        self.refresh_dropdown_options()
    
    def _go_to_index(self):
        """Go to a specific index in the palette."""
        try:
            index = int(self.index_var.get())
            if 0 <= index < len(self.current_colors):
                self._select_color(index, "left", 0)
                # If the index is beyond the displayed range, we still select it
                # but the user won't see the visual highlight unless they scroll
        except ValueError:
            pass
    
    def _apply_hex_color(self):
        """Apply a hex color to the selected color(s)."""
        # Prevent color changes during palette switching to avoid cross-palette contamination
        if getattr(self, '_updating_selection', False):
            return
        
        # Additional protection: Check if we just switched palettes recently (debounce)
        current_time = time.time()
        switch_time = getattr(self, '_palette_switch_time', 0)
        if current_time - switch_time < 0.2:  # 200ms debounce
            return
        
        # Verify we're still on the same palette to prevent cross-contamination
        current_name = self.edit_var.get()
        if hasattr(self, '_current_palette_name') and current_name != self._current_palette_name:
            return
        
        try:
            hex_color = self.hex_var.get().strip()
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]
            
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                new_color = (r, g, b)
                
                # Apply to all selected colors
                for idx in self.selected_indices:
                    if idx < len(self.current_colors):
                        self.current_colors[idx] = new_color
                
                # Update temp cache with the new colors
                current_palette_key = f"{self.char_id}_{self.fashion_type}"
                if hasattr(self, '_temp_palette_cache'):
                    self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
                
                # Update the grid (this will only update displayed squares)
                self._create_palette_grid()
                self._update_color_picker()
                self._update_preview()
                
                # Refresh selection highlights after recreating the grid
                self._refresh_selection_highlights()
        except ValueError:
            pass
    
    def _clear_selection(self):
        """Clear all selected colors."""
        self.selected_indices = set()
        self.selected_index = 0
        self._update_selection_highlights()
        self._update_color_picker()
    
    def _update_selection_highlights(self):
        """Update the selection highlights in the grid."""
        # Keep highlightthickness consistent to prevent grid movement
        for i, square in enumerate(self.palette_squares):
            if i in self.selected_indices:
                square.configure(highlightbackground="red", highlightthickness=1)
            else:
                square.configure(highlightbackground="black", highlightthickness=1)
        
        count = len(self.selected_indices)
        self.selection_count_var.set(f"({count} selected)")
    
    def _create_saved_colors_grid(self):
        """Create the saved colors grid."""
        # Clear existing saved colors
        for widget in self.saved_colors_frame.winfo_children():
            widget.destroy()
        self.saved_color_squares = []  # Store references to the squares
        
        # Get the frame width to calculate square size
        self.saved_colors_frame.update_idletasks()
        frame_width = self.saved_colors_frame.winfo_width()
        if frame_width <= 1:  # Frame not yet sized
            frame_width = 300  # Default width
        
        # Fixed square size of 28x28 pixels (smaller to fit 10 per row)
        square_size = 28
        
        # Calculate spacing to evenly distribute across available width
        total_square_width = 10 * square_size  # 10 squares per row
        available_width = frame_width - 20  # Account for some margin
        extra_space = max(0, available_width - total_square_width)
        horizontal_spacing = extra_space // 9 if extra_space > 0 else 2  # 9 gaps between 10 squares
        
        # Use minimum spacing of 2px, maximum of 8px for reasonable appearance
        horizontal_spacing = max(2, min(8, horizontal_spacing))
        vertical_spacing = 3  # Fixed vertical spacing
        
        # Create 2 rows of 10 saved color squares with calculated spacing
        for i in range(20):
            row = i // 10
            col = i % 10
            
            square = tk.Canvas(self.saved_colors_frame, width=square_size, height=square_size,
                             highlightthickness=1, highlightbackground="black")
            
            # Use calculated horizontal spacing, fixed vertical spacing
            padx = (horizontal_spacing // 2, horizontal_spacing // 2) if col < 9 else (horizontal_spacing // 2, 0)
            square.grid(row=row, column=col, padx=padx, pady=vertical_spacing)
            self.saved_color_squares.append(square)  # Store reference
            
            # Fill with saved color
            color = self.saved_colors[i]
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            square.create_rectangle(0, 0, square_size, square_size, fill=hex_color, outline="black")
            
            # Bind click events
            square.bind("<Button-1>", lambda e, idx=i: self._on_saved_color_click(idx, "left"))
            square.bind("<Button-3>", lambda e, idx=i: self._on_saved_color_click(idx, "right"))
    
    def _update_saved_color_square(self, slot_index):
        """Update a specific saved color square without recreating the entire grid."""
        if hasattr(self, 'saved_color_squares') and slot_index < len(self.saved_color_squares):
            square = self.saved_color_squares[slot_index]
            color = self.saved_colors[slot_index]
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            square.delete("all")
            # Use the same size as calculated in _create_saved_colors_grid
            square_size = square.winfo_width()
            square.create_rectangle(0, 0, square_size, square_size, fill=hex_color, outline="black")
    
    def _save_to_slot(self, slot_index):
        """Save current color to a saved color slot (only if in L mode)."""
        if self.saved_mode == "L" and self.selected_index < len(self.current_colors):
            self.saved_colors[slot_index] = self.current_colors[self.selected_index]
            # Update only the specific square instead of recreating the entire grid
            self._update_saved_color_square(slot_index)
    
    def _load_from_slot(self, slot_index):
        """Load color from a saved color slot to selected color(s) (only if in R mode)."""
        if self.saved_mode == "R" and self.saved_colors[slot_index] != (0, 0, 0):  # Only load if slot is not empty
            color = self.saved_colors[slot_index]
            
            # Apply to all selected colors
            for idx in self.selected_indices:
                if idx < len(self.current_colors):
                    self.current_colors[idx] = color
            
            # Update temp cache with the new colors
            current_palette_key = f"{self.char_id}_{self.fashion_type}"
            if hasattr(self, '_temp_palette_cache'):
                self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
            
            # Update only the affected palette squares
            for idx in self.selected_indices:
                if idx < len(self.palette_squares):
                    square = self.palette_squares[idx]
                    hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                    square.delete("all")
                    square.create_rectangle(0, 0, 80, 80, fill=hex_color, outline="black")
            
            self._update_color_picker()
            self._update_preview()
            
            # Refresh selection highlights after updating colors
            self._refresh_selection_highlights()
    
    def _save_color(self):
        """Save saved colors collection to JSON file."""
        from tkinter import filedialog
        import json
        
        # Default to exports/colors/json directory for saved colors
        default_dir = os.path.join(self.icon_handler.root_dir, "exports", "colors", "json")
        os.makedirs(default_dir, exist_ok=True)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            title="Save Colors",
            initialdir=default_dir
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.saved_colors, f)
            messagebox.showinfo("Success", f"Colors saved to {os.path.basename(file_path)}")
            self._bring_to_front()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save colors: {e}")
            self._bring_to_front()
    
    def _load_color(self):
        """Load saved colors collection from JSON file."""
        from tkinter import filedialog
        import json
        
        # Default to exports/colors/json directory for saved colors
        default_dir = os.path.join(self.icon_handler.root_dir, "exports", "colors", "json")
        os.makedirs(default_dir, exist_ok=True)
        
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")],
            title="Load Colors",
            initialdir=default_dir
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Validate and convert the data
            if isinstance(data, list) and all(isinstance(t, (list, tuple)) and len(t) == 3 for t in data):
                data = [tuple(int(x) for x in t) for t in data][:16]  # Limit to 16 slots
                if len(data) < 16:
                    data += [(0, 0, 0)] * (16 - len(data))  # Pad with black
                self.saved_colors = data
                
                # Update all saved color squares
                for i in range(16):
                    self._update_saved_color_square(i)
                
                messagebox.showinfo("Success", f"Colors loaded from {os.path.basename(file_path)}")
                self._bring_to_front()
            else:
                messagebox.showerror("Error", "Invalid color data format")
                self._bring_to_front()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load colors: {e}")
            self._bring_to_front()
    
    def _clear_saved_colors(self):
        """Clear all saved colors."""
        self.saved_colors = [(0, 0, 0)] * 20
        # Update all saved color squares
        for i in range(16):
            self._update_saved_color_square(i)
    
    def _toggle_saved_mode(self):
        """Toggle between L (left-click save) and R (right-click save) mode."""
        if self.saved_mode == "L":
            self.saved_mode = "R"
            # Update button text to show current mode
            self.saved_mode_button.configure(text="R")
            # Update instructions text
            self.saved_instructions_label.configure(text="Right click below to save color / Left click above to apply color")
        else:
            self.saved_mode = "L"
            # Update button text to show current mode
            self.saved_mode_button.configure(text="L")
            # Update instructions text
            self.saved_instructions_label.configure(text="Left click below to save color / Right click above to apply color")
    
    def _load_saved_palette(self):
        """Load saved palette (same as Load Saved Colors)."""
        self._load_saved_colors()
    
    def _create_color_control(self, parent, index, color, column_index, column_position):
        """Create a color editing control for a single color."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        # Add horizontal divider (except for the first color in each column)
        if column_position > 0:
            separator = ttk.Separator(parent, orient='horizontal')
            separator.pack(fill=tk.X, pady=(0, 2))
        
        # Color preview
        color_canvas = tk.Canvas(frame, width=30, height=20, highlightthickness=1, highlightbackground="black")
        color_canvas.pack(side=tk.LEFT, padx=(0, 10))
        color_canvas.create_rectangle(2, 2, 28, 18, fill=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}")
        
        # RGB sliders
        rgb_frame = ttk.Frame(frame)
        rgb_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Red slider
        red_frame = ttk.Frame(rgb_frame)
        red_frame.pack(fill=tk.X)
        ttk.Label(red_frame, text="R:", width=3).pack(side=tk.LEFT)
        red_var = tk.IntVar(value=color[0])
        red_scale = ttk.Scale(red_frame, from_=0, to=255, variable=red_var, 
                             command=lambda v: self._update_color(index, 0, int(float(v))))
        red_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(red_frame, textvariable=red_var, width=4).pack(side=tk.RIGHT)
        
        # Green slider
        green_frame = ttk.Frame(rgb_frame)
        green_frame.pack(fill=tk.X)
        ttk.Label(green_frame, text="G:", width=3).pack(side=tk.LEFT)
        green_var = tk.IntVar(value=color[1])
        green_scale = ttk.Scale(green_frame, from_=0, to=255, variable=green_var,
                               command=lambda v: self._update_color(index, 1, int(float(v))))
        green_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(green_frame, textvariable=green_var, width=4).pack(side=tk.RIGHT)
        
        # Blue slider
        blue_frame = ttk.Frame(rgb_frame)
        blue_frame.pack(fill=tk.X)
        ttk.Label(blue_frame, text="B:", width=3).pack(side=tk.LEFT)
        blue_var = tk.IntVar(value=color[2])
        blue_scale = ttk.Scale(blue_frame, from_=0, to=255, variable=blue_var,
                              command=lambda v: self._update_color(index, 2, int(float(v))))
        blue_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(blue_frame, textvariable=blue_var, width=4).pack(side=tk.RIGHT)
        
        # Store references
        self.color_controls.append({
            'canvas': color_canvas,
            'red_var': red_var,
            'green_var': green_var,
            'blue_var': blue_var,
            'red_scale': red_scale,
            'green_scale': green_scale,
            'blue_scale': blue_scale
        })
    
    def _update_color(self, index, channel, value):
        """Update a color value and refresh preview."""
        if 0 <= index < len(self.current_colors):
            color = list(self.current_colors[index])
            color[channel] = value
            self.current_colors[index] = tuple(color)
            
            # Update color preview (only if it's displayed)
            if index < len(self.palette_squares):
                square = self.palette_squares[index]
                hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                square.delete("all")
                square.create_rectangle(0, 0, 40, 40, fill=hex_color, outline="black")
            
            # Update preview
            self._update_preview()
    
    def _update_preview(self):
        """Update the live preview of the icon."""
        try:
            
            # Load the original PNG
            img = Image.open(self.png_path).convert("RGBA")
            alpha = img.split()[3]
            
            # Create new RGB image
            new_img = Image.new("RGB", img.size)
            
            # Create color mapping
            color_map = {}
            self.color_mapping = {}  # Store mapping for click detection
            color_idx = 0
            
            # Get colors to use (reverse if inverse order is checked)
            colors_to_use = self.current_colors.copy()
            if self.inverse_order_var.get():
                colors_to_use.reverse()
            
            # Map original colors to our edited colors
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    pixel = img.getpixel((x, y))
                    if pixel[3] > 0:  # Not transparent
                        if pixel not in color_map:
                            if color_idx < len(colors_to_use):
                                color_map[pixel] = colors_to_use[color_idx]
                                self.color_mapping[pixel] = color_idx  # Store for click detection
                                color_idx += 1
                            else:
                                color_map[pixel] = colors_to_use[0] if colors_to_use else (0, 0, 0)
                                self.color_mapping[pixel] = 0  # Store for click detection
            
            # Apply colors
            transparent_count = 0
            opaque_count = 0
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if alpha.getpixel((x, y)) > 0:
                        pixel = img.getpixel((x, y))
                        new_color = color_map.get(pixel, (0, 0, 0))
                        new_img.putpixel((x, y), new_color)
                        opaque_count += 1
                    else:
                        # Use keying color for transparent areas
                        new_img.putpixel((x, y), self.keying_color)
                        transparent_count += 1
            
            # Resize for preview using current zoom level (capped to prevent overflow)
            # Calculate maximum allowed zoom based on image size to prevent overflow
            # Account for new 4:1 column ratio - right column is smaller but allow reasonable zoom
            max_allowed_width = 230  # Allow 10px more stretch for zoom
            max_allowed_height = 230  # Match width for square aspect ratio
            
            max_zoom_x = max_allowed_width / new_img.size[0] if new_img.size[0] > 0 else self.zoom_level
            max_zoom_y = max_allowed_height / new_img.size[1] if new_img.size[1] > 0 else self.zoom_level
            max_allowed_zoom = min(max_zoom_x, max_zoom_y, self.zoom_level)
            
            # Use the smaller of current zoom or max allowed zoom
            effective_zoom = min(self.zoom_level, max_allowed_zoom)
            
            preview_size = (int(new_img.size[0] * effective_zoom), int(new_img.size[1] * effective_zoom))
            preview_img = new_img.resize(preview_size, Image.NEAREST)
            
            # Convert to PhotoImage for tkinter
            self.preview_photo = ImageTk.PhotoImage(preview_img)
            if self.preview_label is not None:
                self.preview_label.configure(image=self.preview_photo)
            
        except Exception as e:
            print(f"Error updating preview: {e}")
    
    def _toggle_colorpicker(self):
        """Toggle colorpicker mode on/off."""
        self.colorpicker_active = not self.colorpicker_active
        
        if self.colorpicker_active:
            self.colorpicker_btn.configure(text="🎨 Exit")
            # Change cursor for all clickable areas
            self.preview_label.configure(cursor="crosshair")
            for square in self.palette_squares:
                square.configure(cursor="crosshair")
            if hasattr(self, 'saved_color_squares'):
                for square in self.saved_color_squares:
                    square.configure(cursor="crosshair")
        else:
            self.colorpicker_btn.configure(text="🎨 Pick")
            # Reset cursors
            self.preview_label.configure(cursor="hand2")
            for square in self.palette_squares:
                square.configure(cursor="")
            if hasattr(self, 'saved_color_squares'):
                for square in self.saved_color_squares:
                    square.configure(cursor="")
    
    def _colorpick_from_preview(self, event):
        """Pick color from preview image."""
        try:
            # Get the click coordinates relative to the preview label
            click_x = event.x
            click_y = event.y
            
            # The preview is scaled up by effective zoom, so we need to scale down the coordinates
            # Calculate the same effective zoom as in _update_preview
            img = Image.open(self.png_path).convert("RGBA")
            max_allowed_width = 230  # Same as in _update_preview
            max_allowed_height = 230  # Same as in _update_preview
            
            max_zoom_x = max_allowed_width / img.size[0] if img.size[0] > 0 else self.zoom_level
            max_zoom_y = max_allowed_height / img.size[1] if img.size[1] > 0 else self.zoom_level
            max_allowed_zoom = min(max_zoom_x, max_zoom_y, self.zoom_level)
            
            effective_zoom = min(self.zoom_level, max_allowed_zoom)
            
            original_x = int(click_x / effective_zoom)
            original_y = int(click_y / effective_zoom)
            
            # Check if the click is within the image bounds
            if 0 <= original_x < img.size[0] and 0 <= original_y < img.size[1]:
                # Get the pixel color at the clicked position
                pixel = img.getpixel((original_x, original_y))
                
                # Check if the pixel is not transparent
                if pixel[3] > 0:  # Not transparent
                    # Get the actual color being displayed (after color mapping)
                    if pixel in self.color_mapping:
                        # Get the mapped color from current_colors
                        color_index = self.color_mapping[pixel]
                        
                        # If inverse order is enabled, translate the index
                        if self.inverse_order_var.get():
                            reversed_index = len(self.current_colors) - 1 - color_index
                            color_index = reversed_index
                        
                        if 0 <= color_index < len(self.current_colors):
                            picked_color = self.current_colors[color_index]
                        else:
                            picked_color = (0, 0, 0)
                    else:
                        # Fallback to black if mapping not found
                        picked_color = (0, 0, 0)
                else:
                    # Clicked on transparent area - pick the keying/background color
                    picked_color = self.keying_color
                
                # Check if picked color is a keying color and find alternative if needed
                if self._is_keyed_color(picked_color):
                    picked_color = self._find_nearest_non_keyed_color(picked_color)
                    print(f"Avoided keying color, using alternative: {picked_color}")
                
                # Apply the picked color to selected palette indices
                self._apply_colorpicked_color(picked_color)
                
        except Exception as e:
            print(f"Error picking color from preview: {e}")
    
    def _colorpick_from_palette(self, index):
        """Pick color from palette square."""
        if 0 <= index < len(self.current_colors):
            picked_color = self.current_colors[index]
            
            # Check if picked color is a keying color and find alternative if needed
            if self._is_keyed_color(picked_color):
                picked_color = self._find_nearest_non_keyed_color(picked_color)
                print(f"Avoided keying color, using alternative: {picked_color}")
            
            self._apply_colorpicked_color(picked_color)
    
    def _colorpick_from_saved(self, slot_index):
        """Pick color from saved color slot."""
        if 0 <= slot_index < len(self.saved_colors):
            picked_color = self.saved_colors[slot_index]
            if picked_color != (0, 0, 0):  # Only pick non-empty slots
                # Check if picked color is a keying color and find alternative if needed
                if self._is_keyed_color(picked_color):
                    picked_color = self._find_nearest_non_keyed_color(picked_color)
                    print(f"Avoided keying color, using alternative: {picked_color}")
                
                self._apply_colorpicked_color(picked_color)
    
    def _apply_colorpicked_color(self, picked_color):
        """Apply a picked color to the selected palette indices."""
        # Double-check that picked color is not a keying color before applying
        if self._is_keyed_color(picked_color):
            picked_color = self._find_nearest_non_keyed_color(picked_color)
            print(f"Final keying color check: avoided {picked_color}, using alternative")
        
        # Apply to all selected colors
        for idx in self.selected_indices:
            if idx < len(self.current_colors):
                self.current_colors[idx] = picked_color
        
        # Update temp cache with the new colors
        current_palette_key = f"{self.char_id}_{self.fashion_type}"
        if hasattr(self, '_temp_palette_cache'):
            self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
        
        # Update only the affected palette squares
        for idx in self.selected_indices:
            if idx < len(self.palette_squares):
                square = self.palette_squares[idx]
                hex_color = f"#{picked_color[0]:02x}{picked_color[1]:02x}{picked_color[2]:02x}"
                square.delete("all")
                square.create_rectangle(0, 0, 80, 80, fill=hex_color, outline="black")
        
        self._update_color_picker()
        self._update_preview()
        
        # Refresh selection highlights after updating colors
        self._refresh_selection_highlights()
        
        # Exit colorpicker mode after picking
        if self.colorpicker_active:
            self._toggle_colorpicker()
    
    def _on_palette_square_click(self, index, button, state):
        """Handle palette square clicks - either for selection or colorpicking."""
        if self.colorpicker_active:
            self._colorpick_from_palette(index)
        else:
            self._select_color(index, button, state)
    
    def _on_saved_color_click(self, slot_index, button):
        """Handle saved color clicks - either for normal operation or colorpicking."""
        if self.colorpicker_active:
            self._colorpick_from_saved(slot_index)
        else:
            if button == "left":
                self._save_to_slot(slot_index)
            elif button == "right":
                self._load_from_slot(slot_index)
    
    def _on_preview_click(self, event):
        """Handle click on preview image to select corresponding color index or pick color."""
        if self.colorpicker_active:
            self._colorpick_from_preview(event)
            return
        
        # Original preview click behavior for color selection
        try:
            # Get the click coordinates relative to the preview label
            click_x = event.x
            click_y = event.y
            
            # The preview is scaled up by effective zoom, so we need to scale down the coordinates
            # Calculate the same effective zoom as in _update_preview
            img = Image.open(self.png_path).convert("RGBA")
            max_allowed_width = 230  # Same as in _update_preview (10px more stretch)
            max_allowed_height = 230  # Same as in _update_preview
            
            max_zoom_x = max_allowed_width / img.size[0] if img.size[0] > 0 else self.zoom_level
            max_zoom_y = max_allowed_height / img.size[1] if img.size[1] > 0 else self.zoom_level
            max_allowed_zoom = min(max_zoom_x, max_zoom_y, self.zoom_level)
            
            effective_zoom = min(self.zoom_level, max_allowed_zoom)
            
            original_x = int(click_x / effective_zoom)
            original_y = int(click_y / effective_zoom)
            
            # Load the original image to get the pixel color at the clicked position
            img = Image.open(self.png_path).convert("RGBA")
            
            # Check if the click is within the image bounds
            if 0 <= original_x < img.size[0] and 0 <= original_y < img.size[1]:
                # Get the pixel color at the clicked position
                pixel = img.getpixel((original_x, original_y))
                
                # Check if the pixel is not transparent
                if pixel[3] > 0:  # Not transparent
                    # Look up the color index from our mapping
                    if pixel in self.color_mapping:
                        color_index = self.color_mapping[pixel]
                        
                        # If inverse order is enabled, translate the index to the reversed order
                        if self.inverse_order_var.get():
                            # When inverse is enabled, the colors are reversed in _update_preview
                            # So we need to translate the original index to the reversed index
                            reversed_index = len(self.current_colors) - 1 - color_index
                            color_index = reversed_index
                        
                        # Select the corresponding color in the palette
                        if 0 <= color_index < len(self.current_colors):
                            self._select_color(color_index, "left", 0)
                        else:
                            print(f"Color index {color_index} out of range")
                    else:
                        print(f"Pixel color {pixel} not found in color mapping")
                else:
                    print("Clicked on transparent area")
            else:
                print(f"Click coordinates ({original_x}, {original_y}) out of image bounds")
                
        except Exception as e:
            print(f"Error handling preview click: {e}")
    
    def _on_preview_zoom(self, event):
        """Handle mouse wheel zoom on preview image."""
        try:
            # Determine zoom direction (delta is positive for scroll up, negative for scroll down)
            if event.delta > 0:
                # Scroll up - zoom in
                new_zoom = self.zoom_level + 1
            else:
                # Scroll down - zoom out
                new_zoom = self.zoom_level - 1
            
            # Clamp zoom level to limits
            new_zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))
            
            # Only update if zoom level changed
            if new_zoom != self.zoom_level:
                self.zoom_level = new_zoom
                
                # Update the preview with new zoom level
                self._update_preview()
                
        except Exception as e:
            print(f"Error handling preview zoom: {e}")
    
    def _reset_colors(self):
        """Reset colors to original extracted colors."""
        current_palette_key = f"{self.char_id}_{self.fashion_type}"
        
        # Reset to original colors
        if hasattr(self, '_original_palettes') and current_palette_key in self._original_palettes:
            self.current_colors = self._original_palettes[current_palette_key].copy()
        else:
            self.current_colors = self.editable_colors.copy()
        
        # Update temp cache with reset colors
        if hasattr(self, '_temp_palette_cache'):
            self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
        
        # Recreate the palette grid (this will show the 27 color warning if needed)
        self._create_palette_grid()
        
        # Update color picker and preview
        self._update_color_picker()
        self._update_preview()
    
    def _load_saved_colors(self):
        """Load saved colors from a palette file."""
        try:
            # Open file dialog to select a palette file
            file_path = filedialog.askopenfilename(
                title="Load Saved Colors",
                filetypes=[("VGA 24-bit Palette Files", "*.pal"), ("All Files", "*.*")]
            )
            
            # Bring the icon editor window back to front after file dialog closes
            self._bring_to_front()
            
            if file_path:
                # Read the palette file
                with open(file_path, 'rb') as f:
                    pal_data = f.read()
                
                # Convert to RGB tuples
                saved_colors = []
                for i in range(0, len(pal_data), 3):
                    if i + 2 < len(pal_data):
                        r = pal_data[i]
                        g = pal_data[i+1]
                        b = pal_data[i+2]
                        saved_colors.append((r, g, b))
                
                # Simple approach: take the first N colors from the saved palette
                # where N is the number of editable colors we expect
                expected_count = len(self.editable_colors)
                
                # Filter out keying colors: pure black, neon green, and magenta
                valid_colors = [color for color in saved_colors if color not in [(0, 0, 0), (0, 255, 0), (255, 0, 255)]]
                
                # Check if we have enough valid colors
                if len(valid_colors) < expected_count:
                    # Show error message about missing colors with auto-close
                    self._show_auto_close_warning(
                        "Missing Colors", 
                        f"Error, missing enough indexes in the imported palette file, compensating..."
                    )
                    # Bring the icon editor window to the front after showing the warning
                    self._bring_to_front()
                    
                    # Compensation logic: create a full set of compensated colors
                    if valid_colors:
                        loaded_colors = []
                        
                        # Create a full set of colors by distributing the available colors
                        # and creating variations with saturation shifts
                        for position in range(expected_count):
                            # Choose which source color to use (cycle through available colors)
                            source_color = valid_colors[position % len(valid_colors)]
                            
                            # Calculate saturation shift based on position
                            # Earlier positions get higher saturation, later positions get lower
                            saturation_shift = (expected_count - position) / expected_count
                            
                            # Convert to HSV, modify saturation, convert back to RGB
                            import colorsys
                            r, g, b = source_color
                            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                            
                            # Apply saturation shift (multiply by 0.5 to 1.5 range)
                            new_s = max(0.0, min(1.0, s * (0.5 + saturation_shift)))
                            
                            # Convert back to RGB
                            new_r, new_g, new_b = colorsys.hsv_to_rgb(h, new_s, v)
                            new_color = (int(new_r * 255), int(new_g * 255), int(new_b * 255))
                            
                            loaded_colors.append(new_color)
                    else:
                        # No valid colors found, use black as fallback
                        loaded_colors = [(0, 0, 0)] * expected_count
                else:
                    # We have enough colors, just take what we need
                    loaded_colors = valid_colors[:expected_count]
                
                # Update current colors
                self.current_colors = loaded_colors[:expected_count]
                
                # Update temp cache with loaded colors
                current_palette_key = f"{self.char_id}_{self.fashion_type}"
                if hasattr(self, '_temp_palette_cache'):
                    self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
                
                # Recreate the palette grid (this will show the 27 color warning if needed)
                self._create_palette_grid()
                
                # Update color picker and preview
                self._update_color_picker()
                self._update_preview()
                messagebox.showinfo("Success", f"Loaded colors from {os.path.basename(file_path)}")
                self._bring_to_front()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load colors: {e}")
            self._bring_to_front()
    
    def _save_colors(self):
        """Save current colors to a palette file."""
        try:
            # Set default directory to exports/colors
            default_dir = os.path.join(self.icon_handler.root_dir, "exports", "colors", "icon")
            os.makedirs(default_dir, exist_ok=True)
            
            # Open file dialog to save palette
            file_path = filedialog.asksaveasfilename(
                title="Save Colors",
                defaultextension=".pal",
                filetypes=[("VGA 24-bit Palette Files", "*.pal"), ("All Files", "*.*")],
                initialdir=default_dir
            )
            
            # Bring the icon editor window back to front after file dialog closes
            self._bring_to_front()
            
            if file_path:
                # Save in the same format as the regular palette editor
                # Create a 256-color palette filled with black
                vga_colors = [(0, 0, 0)] * 256
                
                # Place our current colors at the beginning
                for i, color in enumerate(self.current_colors):
                    if i < 256:
                        vga_colors[i] = color
                
                # Write VGA 24-bit format: each color as 3 bytes (R, G, B) in sequence
                with open(file_path, "wb") as f:
                    for r, g, b in vga_colors:
                        f.write(bytes([r, g, b]))
                
                messagebox.showinfo("Success", f"Colors saved to {os.path.basename(file_path)}")
                self._bring_to_front()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save colors: {e}")
            self._bring_to_front()

    def _open_gradient_menu(self):
        """Open the gradient/hue adjustment menu for icon editor."""
        import colorsys
        
        # Create gradient menu window
        gradient_window = tk.Toplevel(self.window)
        gradient_window.title("Gradient Hue Adjustment")
        gradient_window.resizable(False, False)
        gradient_window.transient(self.window)
        gradient_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(gradient_window)
        main_frame.pack(padx=15, pady=15)
        
        # Title
        tk.Label(main_frame, text="Adjust all colors to match hue:", font=("Arial", 10, "bold")).pack(pady=(0, 10))
        
        # Define expanded gradient colors with light/dark variants and additional colors
        gradient_colors = [
            # Row 1: Pastel variants
            ("Pastel Pink", "#FFD1DC", 350, "pastel"),
            ("Pastel Peach", "#FFDBCC", 20, "pastel"),
            ("Pastel Yellow", "#FFFACD", 60, "pastel"),
            ("Pastel Mint", "#F0FFF0", 120, "pastel"),
            ("Pastel Blue", "#E6E6FA", 240, "pastel"),
            ("Pastel Lavender", "#E6E6FA", 270, "pastel"),
            ("Pastel Rose", "#F8BBD0", 330, "pastel"),
            ("Pastel Aqua", "#E0FFFF", 180, "pastel"),
            
            # Row 2: Light variants
            ("Light Red", "#FFB3B3", 0, "light"),
            ("Light Orange", "#FFD9B3", 30, "light"), 
            ("Light Yellow", "#FFFF99", 60, "light"),
            ("Light Green", "#B3FFB3", 120, "light"),
            ("Light Blue", "#B3B3FF", 240, "light"),
            ("Light Purple", "#D9B3FF", 270, "light"),
            ("Pink", "#FF69B4", 330),
            ("Cyan", "#00FFFF", 180),
            
            # Row 3: Standard colors (ROYGBIV + extras)
            ("Red", "#FF0000", 0),
            ("Orange", "#FF8000", 30), 
            ("Yellow", "#FFFF00", 60),
            ("Green", "#00FF00", 120),
            ("Blue", "#0000FF", 240),
            ("Purple", "#8000FF", 270),
            ("Magenta", "#FF00FF", 300),
            ("Teal", "#008080", 180),
            
            # Row 4: Dark variants
            ("Dark Red", "#800000", 0, "dark"),
            ("Dark Orange", "#CC4400", 30, "dark"), 
            ("Dark Yellow", "#CCCC00", 60, "dark"),
            ("Dark Green", "#008000", 120, "dark"),
            ("Dark Blue", "#000080", 240, "dark"),
            ("Dark Purple", "#4B0082", 270, "dark"),
            ("Brown", "#8B4513", 30, "brown"),
            ("Navy", "#191970", 240, "dark"),
            
            # Row 5: Cool colors
            ("Cool Blue", "#0080FF", 210, "cool"),
            ("Cool Cyan", "#00BFFF", 195, "cool"),
            ("Cool Teal", "#008B8B", 180, "cool"),
            ("Cool Green", "#00FF80", 150, "cool"),
            ("Cool Purple", "#8000FF", 270, "cool"),
            ("Cool Violet", "#4000FF", 255, "cool"),
            ("Cool Indigo", "#4B0082", 275, "cool"),
            ("Cool Mint", "#00FF9F", 165, "cool"),
            
            # Row 6: Warm colors
            ("Warm Red", "#FF4000", 15, "warm"),
            ("Warm Orange", "#FF8000", 30, "warm"),
            ("Warm Yellow", "#FFD700", 51, "warm"),
            ("Warm Pink", "#FF69B4", 330, "warm"),
            ("Warm Coral", "#FF7F50", 16, "warm"),
            ("Warm Peach", "#FFCBA4", 28, "warm"),
            ("Warm Gold", "#FFD700", 51, "warm"),
            ("Warm Amber", "#FFBF00", 45, "warm"),
            
            # Row 7: Secondary colors
            ("Orange", "#FF8000", 30, "secondary"),
            ("Green", "#00FF00", 120, "secondary"),
            ("Purple", "#8000FF", 270, "secondary"),
            ("Lime", "#80FF00", 90, "secondary"),
            ("Teal", "#00FF80", 150, "secondary"),
            ("Magenta", "#FF0080", 315, "secondary"),
            ("Chartreuse", "#80FF00", 90, "secondary"),
            ("Spring Green", "#00FF80", 150, "secondary"),
            
            # Row 8: Tertiary colors
            ("Red-Orange", "#FF4000", 15, "tertiary"),
            ("Yellow-Orange", "#FFBF00", 45, "tertiary"),
            ("Yellow-Green", "#80FF00", 90, "tertiary"),
            ("Blue-Green", "#00FF80", 150, "tertiary"),
            ("Blue-Purple", "#4000FF", 255, "tertiary"),
            ("Red-Purple", "#FF0080", 315, "tertiary"),
            ("Vermillion", "#FF4000", 15, "tertiary"),
            ("Turquoise", "#00FFBF", 165, "tertiary"),
            
            # Row 9: Neutrals and special
            ("Light Grey", "#C0C0C0", None, "light_grey"),
            ("Grey", "#808080", None, "grey"),
            ("Dark Grey", "#404040", None, "dark_grey"),
            ("White", "#FFFFFF", None, "white"),
            ("Black", "#000000", None, "black"),
            ("Beige", "#F5F5DC", 60, "beige"),
            ("Cream", "#FFFDD0", 60, "cream"),
            ("Tan", "#D2B48C", 30, "tan")
        ]
        
        # Create color buttons in a grid (9 rows of 8)
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=(0, 15))
        
        rows_data = [
            ("Pastel:", gradient_colors[:8]),
            ("Light:", gradient_colors[8:16]),
            ("Standard:", gradient_colors[16:24]),
            ("Dark:", gradient_colors[24:32]),
            ("Cool:", gradient_colors[32:40]),
            ("Warm:", gradient_colors[40:48]),
            ("Secondary:", gradient_colors[48:56]),
            ("Tertiary:", gradient_colors[56:64]),
            ("Neutral:", gradient_colors[64:72])
        ]
        
        for row_idx, (label, colors) in enumerate(rows_data):
            row = tk.Frame(button_frame)
            if row_idx < len(rows_data) - 1:  # All rows except last
                row.pack(pady=(0, 3), anchor="w")
            else:  # Last row
                row.pack(anchor="w")
            
            tk.Label(row, text=label, font=("Arial", 8)).pack(side="left", padx=(0, 5))
            
            for color_data in colors:
                if color_data:  # Check if color_data exists
                    name, hex_color = color_data[0], color_data[1]
                    target_hue = color_data[2] if len(color_data) > 2 else None
                    variant = color_data[3] if len(color_data) > 3 else None
                    btn = tk.Button(row, text="  ", bg=hex_color, width=3, height=1,
                                  command=lambda h=target_hue, n=name, v=variant: self._apply_gradient_hue(h, n, v))
                    btn.pack(side="left", padx=1)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=(10, 0))
        
        # Reset to Original button
        tk.Button(buttons_frame, text="Reset to Original", command=self._reset_gradient_colors).pack(side="left", padx=(0, 10))
        
        # Close button
        tk.Button(buttons_frame, text="Close", command=gradient_window.destroy).pack(side="left")
        
        # Center the window
        gradient_window.update_idletasks()
        width = gradient_window.winfo_width()
        height = gradient_window.winfo_height()
        x = self.window.winfo_x() + (self.window.winfo_width() - width) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - height) // 2
        gradient_window.geometry(f"+{x}+{y}")

    def _apply_gradient_hue(self, target_hue, color_name, variant=None):
        """Apply hue adjustment to all colors in the current icon palette."""
        import colorsys
        
        # Special handling for neutral colors and variants
        if target_hue is None or variant in ["grey", "light_grey", "dark_grey", "black", "white"]:
            if variant == "light_grey" or color_name == "Light Grey":
                # Convert to light greyscale
                for i in range(len(self.current_colors)):
                    r, g, b = self.current_colors[i]
                    grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                    # Make it lighter
                    light_grey = min(255, int(grey * 1.5))
                    self.current_colors[i] = (light_grey, light_grey, light_grey)
            elif variant == "dark_grey" or color_name == "Dark Grey":
                # Convert to dark greyscale
                for i in range(len(self.current_colors)):
                    r, g, b = self.current_colors[i]
                    grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                    # Make it darker
                    dark_grey = int(grey * 0.5)
                    self.current_colors[i] = (dark_grey, dark_grey, dark_grey)
            elif variant == "grey" or color_name == "Grey":
                # Convert all colors to greyscale
                for i in range(len(self.current_colors)):
                    r, g, b = self.current_colors[i]
                    grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                    self.current_colors[i] = (grey, grey, grey)
            elif variant == "black" or color_name == "Black":
                # Make all colors darker (reduce value significantly)
                for i in range(len(self.current_colors)):
                    r, g, b = self.current_colors[i]
                    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                    v = v * 0.2  # Reduce brightness to 20%
                    rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
                    self.current_colors[i] = (int(rr*255), int(gg*255), int(bb*255))
            elif variant == "white" or color_name == "White":
                # Make all colors lighter (increase value significantly)
                for i in range(len(self.current_colors)):
                    r, g, b = self.current_colors[i]
                    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                    v = min(1.0, v + (1.0 - v) * 0.8)  # Increase brightness towards white
                    rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
                    self.current_colors[i] = (int(rr*255), int(gg*255), int(bb*255))
        else:
            # Apply hue adjustment with optional lightness/darkness variants
            for i in range(len(self.current_colors)):
                r, g, b = self.current_colors[i]
                h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                
                # Only adjust hue if the color has some saturation (not grey/black/white)
                if s > 0.1:  # Threshold to avoid adjusting near-grey colors
                    # Calculate hue difference and apply it
                    current_hue = h * 360
                    hue_diff = target_hue - current_hue
                    
                    # Normalize hue difference to [-180, 180] range for shortest rotation
                    if hue_diff > 180:
                        hue_diff -= 360
                    elif hue_diff < -180:
                        hue_diff += 360
                        
                    new_hue = (current_hue + hue_diff) % 360
                    h = new_hue / 360.0
                
                # Apply lightness/darkness variants
                if variant == "pastel":
                    # Make colors very light and soft by increasing value and significantly reducing saturation
                    v = min(1.0, v + (1.0 - v) * 0.8)  # Increase brightness significantly
                    s = s * 0.3  # Reduce saturation significantly for soft pastel effect
                elif variant == "light":
                    # Make colors lighter by increasing value and reducing saturation slightly
                    v = min(1.0, v + (1.0 - v) * 0.6)  # Increase brightness
                    s = s * 0.7  # Reduce saturation for pastel effect
                elif variant == "dark":
                    # Make colors darker by decreasing value
                    v = v * 0.4  # Reduce brightness significantly
                elif variant in ["beige", "cream", "tan"]:
                    # Special handling for earth tones - reduce saturation and adjust value
                    s = s * 0.3  # Very low saturation
                    if variant == "cream":
                        v = min(1.0, v + (1.0 - v) * 0.7)  # Light
                    elif variant == "tan":
                        v = v * 0.8  # Medium
                    else:  # beige
                        v = min(1.0, v + (1.0 - v) * 0.4)  # Light-medium
                elif variant == "brown":
                    # Brown is essentially dark orange with low saturation
                    s = s * 0.6
                    v = v * 0.5
                elif variant == "cool":
                    # Cool colors: slightly increase saturation and maintain cooler hues
                    s = min(1.0, s * 1.2)  # Increase saturation slightly
                    v = min(1.0, v * 1.1)  # Slightly brighter
                elif variant == "warm":
                    # Warm colors: increase saturation and warmth
                    s = min(1.0, s * 1.3)  # Increase saturation more
                    v = min(1.0, v * 1.05)  # Slightly brighter
                elif variant == "secondary":
                    # Secondary colors: full saturation, balanced brightness
                    s = min(1.0, s * 1.5)  # High saturation
                    v = min(1.0, v * 1.1)  # Slightly brighter
                elif variant == "tertiary":
                    # Tertiary colors: balanced saturation and brightness
                    s = min(1.0, s * 1.2)  # Moderate saturation increase
                    v = min(1.0, v * 1.05)  # Slightly brighter
                
                # Skip if current color is keyed
                current_color = self.current_colors[i]
                if (self.is_universal_keying_color(current_color) or 
                    current_color == (255, 0, 255) or  # Magenta
                    (hasattr(self, 'is_chr003_keying_color') and self.is_chr003_keying_color(current_color)) or  # Sheep
                    (hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(current_color)) or  # Raccoon
                    (hasattr(self, 'is_chr011_keying_color') and self.is_chr011_keying_color(current_color)) or  # Sheep 2nd Job
                    (hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(current_color)) or  # Lion 2nd Job
                    (hasattr(self, 'is_palette_keying_color') and self.is_palette_keying_color(current_color, i, self.char_id))):  # Any other character-specific rules
                    continue
                    
                # Convert back to RGB
                rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
                candidate_color = (int(rr*255), int(gg*255), int(bb*255))
                
                # Check if new color would be a keying color
                if (self.is_universal_keying_color(candidate_color) or 
                    candidate_color == (255, 0, 255) or  # Magenta
                    (hasattr(self, 'is_chr003_keying_color') and self.is_chr003_keying_color(candidate_color)) or  # Sheep
                    (hasattr(self, 'is_chr008_keying_color') and self.is_chr008_keying_color(candidate_color)) or  # Raccoon
                    (hasattr(self, 'is_chr011_keying_color') and self.is_chr011_keying_color(candidate_color)) or  # Sheep 2nd Job
                    (hasattr(self, 'is_chr014_keying_color') and self.is_chr014_keying_color(candidate_color)) or  # Lion 2nd Job
                    (hasattr(self, 'is_palette_keying_color') and self.is_palette_keying_color(candidate_color, i, self.char_id))):  # Any other character-specific rules
                    candidate_color = self._find_nearest_non_keyed_color(candidate_color)
                
                self.current_colors[i] = candidate_color
        
        # Update temp cache with the new colors
        current_palette_key = f"{self.char_id}_{self.fashion_type}"
        if hasattr(self, '_temp_palette_cache'):
            self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
        
        # Update the UI
        self._create_palette_grid()
        self._update_color_picker()
        self._update_preview()
    
    def _reset_gradient_colors(self):
        """Reset colors to original extracted colors before gradient changes."""
        current_palette_key = f"{self.char_id}_{self.fashion_type}"
        
        # Reset to original colors
        if hasattr(self, '_original_palettes') and current_palette_key in self._original_palettes:
            self.current_colors = self._original_palettes[current_palette_key].copy()
        else:
            self.current_colors = self.editable_colors.copy()
        
        # Update temp cache with reset colors
        if hasattr(self, '_temp_palette_cache'):
            self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
        
        # Update the UI
        self._create_palette_grid()
        self._update_color_picker()
        self._update_preview()
    
    def _is_keyed_color(self, color, index):
        """Check if a color would be a keying color that should be avoided."""
        r, g, b = color
        # Check if it matches the keying color (magenta)
        if (r, g, b) == self.keying_color:
            return True
        # Check if it's very close to the keying color (within 10 units)
        kr, kg, kb = self.keying_color
        if abs(r - kr) < 10 and abs(g - kg) < 10 and abs(b - kb) < 10:
            return True
        return False
    
    def _find_nearest_non_keyed_color(self, color):
        """Find the nearest color that isn't a keying color."""
        r, g, b = color
        # Simple approach: adjust the color slightly to avoid keying
        if self._is_keyed_color((r, g, b), 0):
            # Try adjusting each channel slightly
            for offset in [5, -5, 10, -10, 15, -15]:
                for channel in ['r', 'g', 'b']:
                    test_color = [r, g, b]
                    if channel == 'r':
                        test_color[0] = max(0, min(255, r + offset))
                    elif channel == 'g':
                        test_color[1] = max(0, min(255, g + offset))
                    elif channel == 'b':
                        test_color[2] = max(0, min(255, b + offset))
                    
                    if not self._is_keyed_color(tuple(test_color), 0):
                        return tuple(test_color)
        
        # If all else fails, return the original color
        return color
    
    def _export_icon(self):
        """Export the edited icon."""
        try:
            # Get exports directory path
            export_dir = os.path.join(self.icon_handler.root_dir, "exports")
            
            # Check if this is QuickSave mode (no user input needed)
            if hasattr(self, 'is_quicksave_mode') and self.is_quicksave_mode:
                # QuickSave mode: use palette file name automatically
                icon_name = os.path.splitext(os.path.basename(self.palette_path))[0] + ".bmp"
                export_path = os.path.join(export_dir, icon_name)
            else:
                # Editor mode: ask user for filename
                from tkinter import filedialog
                
                # Default filename based on palette
                default_name = os.path.splitext(os.path.basename(self.palette_path))[0] + ".bmp"
                
                # Show save dialog
                export_path = filedialog.asksaveasfilename(
                    title="Save Icon As",
                    initialdir=export_dir,
                    initialfile=default_name,
                    defaultextension=".bmp",
                    filetypes=[("BMP files", "*.bmp"), ("All files", "*.*")]
                )
                
                # Bring the icon editor window back to front after file dialog closes
                self._bring_to_front()
                
                # If user cancelled, return early
                if not export_path:
                    return
                
                # Ensure the file has .bmp extension
                if not export_path.lower().endswith('.bmp'):
                    export_path += '.bmp'
            
            # Create directory if it doesn't exist when actually saving
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            
            # Use the icon handler to save with our edited colors
            success = self.icon_handler.save_as_icon_with_colors(
                self.char_id, self.fashion_type, self.current_colors, 
                self.keying_color, self.png_path, export_path
            )
            
            if success:
                messagebox.showinfo("Success", f"Icon saved to: {export_path}")
                self._bring_to_front()
                # Don't close the editor - let user continue editing
            else:
                messagebox.showerror("Error", "Failed to save icon")
                self._bring_to_front()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export icon: {e}")
            self._bring_to_front()
