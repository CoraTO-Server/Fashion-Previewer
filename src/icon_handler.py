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
        self.root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
                "fashion_6": "Hood Tie"
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
        return result
    
    def _determine_keying_color(self, ref_colors: list) -> tuple:
        """Determine the keying color from reference palette (same logic as IconPaletteEditor)."""
        
        if not ref_colors:
            return (255, 0, 255)  # Default to magenta
        
        
        # Check first color
        if ref_colors[0] == (255, 0, 255):
            return (255, 0, 255)
        elif ref_colors[0] == (0, 0, 0):
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
            elif color == (0, 0, 0) and not found_black:
                found_black = True
                black_index = i
        
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
                        valid_colors.append((128, 128, 128))  # Default gray
                except (ValueError, TypeError):
                    valid_colors.append((128, 128, 128))  # Default gray
            else:
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
                is_quicksave_mode=False,  # Editor mode - allow user to name file
                icon_handler=self
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
        Get paths to the icon BMP and PAL files.
        For Paula characters, checks both folders (e.g. chr025 and chr100).
        
        Args:
            char_id: Character ID (e.g. 'chr001' or 'chr025')
            item_name: Fashion type variable name (e.g. 'dress') - will be converted to actual name
            
        Returns:
            tuple[str, str]: (bmp_path, pal_path) for the icon files
            Returns the first matching pair found, checking all possible character folders
        """
        # Get the actual fashion name from the variable name
        actual_fashion_name = self._get_fashion_name(char_id, item_name)
        
        # Clean item name - remove spaces, uppercase, special characters and make lowercase
        clean_name = ''.join(c.lower() for c in actual_fashion_name if c.isalnum())
        
        
        # Try all possible folders
        for folder in self._get_character_folders(char_id):
            char_icon_dir = os.path.join(self.icons_dir, folder)
            bmp_path = os.path.join(char_icon_dir, "BMP", f"{clean_name}.bmp")  # Use BMP for consistency
            pal_path = os.path.join(char_icon_dir, "PAL", f"{clean_name}.pal")
            
            
            # If both files exist in this folder, use these paths
            if os.path.exists(bmp_path) and os.path.exists(pal_path):
                return bmp_path, pal_path
        
        # If no matching files found in any folder, return paths for the primary folder
        char_icon_dir = os.path.join(self.icons_dir, self._get_character_folders(char_id)[0])
        return (
            os.path.join(char_icon_dir, "BMP", f"{clean_name}.bmp"),  # Use BMP for consistency
            os.path.join(char_icon_dir, "PAL", f"{clean_name}.pal")
        )
    
    def _find_base_bmp_name(self, char_id: str, fashion_type: str) -> str:
        """
        Find the base BMP name from the current character and fashion type.
        
        Args:
            char_id: Character ID (e.g. 'chr001')
            fashion_type: Type of fashion (e.g. 'fashion_1')
            
        Returns:
            str: Base BMP name (e.g. 'hoodie')
        """
        item_name = self._get_fashion_name(char_id, fashion_type)
        # Clean item name - remove spaces, uppercase, special characters and make lowercase
        clean_name = ''.join(c.lower() for c in item_name if c.isalnum())
        return clean_name
    
    def _find_matching_pal_file(self, char_id: str, base_bmp_name: str) -> str:
        """
        Find the matching fashion PAL file in the PAL folder next to the BMP folder.
        
        Args:
            char_id: Character ID (e.g. 'chr001')
            base_bmp_name: Base BMP name (e.g. 'hoodie')
            
        Returns:
            str: Path to the matching PAL file, or empty string if not found
        """
        # Try all possible folders for this character
        for folder in self._get_character_folders(char_id):
            char_icon_dir = os.path.join(self.icons_dir, folder)
            pal_path = os.path.join(char_icon_dir, "PAL", f"{base_bmp_name}.pal")
            
            if os.path.exists(pal_path):
                return pal_path
        
        return ""
    
    def _apply_sliders_to_pal(self, pal_path: str, custom_palette: list, char_id: str, fashion_type: str) -> list:
        """
        Apply the same slider adjustments to the PAL folder palette as were applied to the vanilla palette,
        except for the keying color (magenta).
        
        Args:
            pal_path: Path to the PAL folder palette file
            custom_palette: The adjusted vanilla palette
            char_id: Character ID
            fashion_type: Fashion type
            
        Returns:
            list: Adjusted PAL folder palette colors
        """
        try:
            # Load the PAL folder palette
            pal_colors = []
            with open(pal_path, 'rb') as f:
                pal_data = f.read()
                
                for i in range(0, len(pal_data), 3):
                    if i + 2 >= len(pal_data):
                        break
                    r = pal_data[i]
                    g = pal_data[i+1]
                    b = pal_data[i+2]
                    pal_colors.append((r, g, b))
            
            # Get the valid ranges for this fashion type
            char_num = char_id[3:] if char_id.startswith('chr') else char_id
            translator = IndexTranslator()
            ranges = translator.original_ranges.get(char_num, {}).get(fashion_type, [])
            
            # Load the original vanilla palette to compare changes
            vanilla_pal_name = f"{char_id}_{fashion_type.replace('fashion_', 'w')}.pal"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            vanilla_pal_path = os.path.join(script_dir, "nonremovable_assets", "vanilla_pals", "fashion", vanilla_pal_name)
            
            vanilla_colors = []
            if os.path.exists(vanilla_pal_path):
                with open(vanilla_pal_path, 'rb') as f:
                    vanilla_data = f.read()
                    
                    for i in range(0, len(vanilla_data), 3):
                        if i + 2 >= len(vanilla_data):
                            break
                        r = vanilla_data[i]
                        g = vanilla_data[i+1]
                        b = vanilla_data[i+2]
                        vanilla_colors.append((r, g, b))
            
            # Calculate the adjustment ratios from vanilla to custom palette
            adjusted_pal_colors = pal_colors.copy()
            
            # Apply adjustments to valid range colors, but skip magenta keying colors
            for r in ranges:
                for idx in range(r.start, min(r.stop, len(pal_colors), len(vanilla_colors), len(custom_palette))):
                    pal_color = pal_colors[idx] if idx < len(pal_colors) else (0, 0, 0)
                    vanilla_color = vanilla_colors[idx] if idx < len(vanilla_colors) else (0, 0, 0)
                    custom_color = custom_palette[idx] if idx < len(custom_palette) else (0, 0, 0)
                    
                    # Skip magenta keying colors
                    if pal_color == (255, 0, 255):
                        continue
                        
                    # Calculate adjustment ratios
                    if vanilla_color != (0, 0, 0):
                        r_ratio = custom_color[0] / max(1, vanilla_color[0])
                        g_ratio = custom_color[1] / max(1, vanilla_color[1])
                        b_ratio = custom_color[2] / max(1, vanilla_color[2])
                        
                        # Apply ratios to PAL color
                        new_r = min(255, max(0, int(pal_color[0] * r_ratio)))
                        new_g = min(255, max(0, int(pal_color[1] * g_ratio)))
                        new_b = min(255, max(0, int(pal_color[2] * b_ratio)))
                        
                        adjusted_pal_colors[idx] = (new_r, new_g, new_b)
            
            return adjusted_pal_colors
            
        except Exception as e:
            # Return the PAL colors as-is if adjustment fails
            try:
                pal_colors = []
                with open(pal_path, 'rb') as f:
                    pal_data = f.read()
                    
                    for i in range(0, len(pal_data), 3):
                        if i + 2 >= len(pal_data):
                            break
                        r = pal_data[i]
                        g = pal_data[i+1]
                        b = pal_data[i+2]
                        pal_colors.append((r, g, b))
                
                return pal_colors
            except:
                return []

    def save_as_icon(self, char_id: str, fashion_type: str, custom_palette: list, palette_path: str = None) -> bool:
        """
        Save the current item as an icon with the custom palette applied.
        Uses the new system: finds base BMP name, matches PAL folder palette, 
        and applies the same slider adjustments as the vanilla palette.
        
        Args:
            char_id: Character ID (e.g. 'chr001')
            fashion_type: Type of fashion (e.g. 'fashion_1')
            custom_palette: List of (r,g,b) tuples representing the custom palette
            palette_path: Path to the saved custom palette file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Step 1: Find the base BMP name
            base_bmp_name = self._find_base_bmp_name(char_id, fashion_type)
            
            # Step 2: Find the matching fashion PAL file in PAL folder
            pal_file_path = self._find_matching_pal_file(char_id, base_bmp_name)
            if not pal_file_path:
                return False
            
            # Step 3: For quicksave, directly use the saved palette colors instead of applying slider adjustments
            # Load the base PAL file structure but replace the colors with saved palette colors
            base_pal_colors = []
            with open(pal_file_path, 'rb') as f:
                pal_data = f.read()
                for i in range(0, len(pal_data), 3):
                    if i + 2 >= len(pal_data):
                        break
                    r = pal_data[i]
                    g = pal_data[i+1]
                    b = pal_data[i+2]
                    base_pal_colors.append((r, g, b))
            
            # Create adjusted palette by mapping saved colors to the correct indexes
            adjusted_pal_colors = base_pal_colors.copy()  # Start with base structure
            char_num = char_id[3:] if char_id.startswith('chr') else char_id
            translator = IndexTranslator()
            ranges = translator.original_ranges.get(char_num, {}).get(fashion_type, [])
            
            # Map saved palette colors to the correct indexes in the base PAL structure
            # For main UI mode, use direct index mapping without translation
            # For quicksave mode, use the existing translation logic
            if hasattr(self, 'is_quicksave_mode') and not self.is_quicksave_mode:
                # Main UI mode: Direct index-to-index mapping
                for r in ranges:
                    for idx in range(r.start, r.stop):  # Include full range
                        if (idx < len(adjusted_pal_colors) and idx < len(custom_palette) and 
                            idx != 0 and idx != 255):  # Skip index 0 (keying) AND index 255 (last palette index)
                            # Use the saved palette color at the SAME index position
                            adjusted_pal_colors[idx] = custom_palette[idx]
            else:
                # Quicksave mode: Use translation logic
                for r in ranges:
                    for idx in range(r.start, r.stop):  # Include full range
                        if (idx < len(adjusted_pal_colors) and idx < len(custom_palette) and 
                            idx != 0 and idx != 255):  # Skip index 0 (keying) AND index 255 (last palette index)
                            # Use the saved palette color at the SAME index position
                            adjusted_pal_colors[idx] = custom_palette[idx]
            
            # Count how many colors were actually mapped
            mapped_count = 0
            for r in ranges:
                for idx in range(r.start, r.stop):
                    if (idx < len(adjusted_pal_colors) and idx < len(custom_palette) and 
                        idx != 0 and idx != 255):
                        mapped_count += 1
            
            # Step 4: Get the image path (use BMP files only)
            icon_dir = os.path.dirname(pal_file_path)
            icon_dir = os.path.normpath(os.path.join(icon_dir, ".."))
            
            # Use only BMP files for consistency
            bmp_path = os.path.join(icon_dir, "BMP", f"{base_bmp_name}.bmp")
            
            if os.path.exists(bmp_path):
                image_path = bmp_path
            else:
                return False
                
            # Get exports/icons directory path
            export_dir = os.path.join(self.root_dir, "exports", "icons")
            
            # Get the actual used indexes (non-keying colors) from the adjusted PAL palette
            # Only use colors that match the valid indexes, excluding keying colors
            used_colors = []
            char_num = char_id[3:] if char_id.startswith('chr') else char_id
            translator = IndexTranslator()
            ranges = translator.original_ranges.get(char_num, {}).get(fashion_type, [])
            
            # Extract ONLY the valid colors from the ranges, excluding keying colors and last indexes
            for r in ranges:
                for idx in range(r.start, r.stop - 1):  # Skip last index in each range
                    if idx < len(adjusted_pal_colors):
                        color = adjusted_pal_colors[idx]
                        # Skip ALL keying colors: magenta, neon green, and character-specific keyed patterns
                        if (idx != 0 and idx != 255 and  # Skip index 0 (always keying) and 255 (last index)
                            not self.is_universal_keying_color(color) and  # Skip universal keying colors
                            color != (255, 0, 255) and  # Skip magenta
                            not self._is_keyed_color(color, idx)):  # Use comprehensive keying detection
                            used_colors.append(color)
            
            # Load and process the image
            img = Image.open(image_path).convert("RGBA")
            
            # Get alpha channel first
            alpha = img.split()[3]
            
            # Create a new RGB image (for BMP output with keying)
            new_img = Image.new("RGB", img.size)
            
            # Load the original image as palette mode to get the palette indices
            original_img_palette = Image.open(image_path).convert("P")
            original_pixel_data = list(original_img_palette.getdata())
            
            # Get the original BMP's palette
            original_bmp_palette = original_img_palette.getpalette()
            
            # Create a new palette-mode image with the custom palette
            new_palette_img = Image.new("P", img.size)
            
            # Map the custom palette colors to the icon palette structure
            # CORRECT FLOW: vanilla_pal ↔ _base.pal matching → BMP color mapping → final palette
            
            # Step 1: Load _base.pal colors
            base_pal_colors = []
            try:
                with open(pal_file_path, 'rb') as f:
                    base_pal_data = f.read()
                for i in range(0, len(base_pal_data), 3):
                    if i + 2 < len(base_pal_data):
                        r = base_pal_data[i]
                        g = base_pal_data[i+1]
                        b = base_pal_data[i+2]
                        base_pal_colors.append((r, g, b))
            except Exception as e:
                return False
            
            # Step 2: Color-based mapping from custom_palette to _base.pal using multi-pass matching
            base_to_custom_mapping = self._create_base_to_custom_mapping(
                base_pal_colors, custom_palette, char_id, fashion_type
            )
            
            # Step 3: Map BMP colors to _base.pal colors (exact matches)
            bmp_to_base_mapping = {}
            used_indices = sorted(set(original_pixel_data))
            
            for bmp_idx in used_indices:
                if bmp_idx < len(original_bmp_palette)//3:
                    # Get BMP color
                    r = original_bmp_palette[bmp_idx*3]
                    g = original_bmp_palette[bmp_idx*3+1]
                    b = original_bmp_palette[bmp_idx*3+2]
                    bmp_color = (r, g, b)
                    
                    # Skip magenta BMP indices
                    if (bmp_color == (255, 0, 255) or 
                        bmp_color == (0, 255, 0) or 
                        self.is_universal_keying_color(bmp_color)):
                        continue
                    
                    # Find exact match in _base.pal
                    for base_idx, base_color in enumerate(base_pal_colors):
                        if base_color == bmp_color:
                            bmp_to_base_mapping[bmp_idx] = base_idx
                            break
            
            # Step 3: Map _base.pal colors to BMP colors (should be identical)
            base_to_bmp_mapping = {}  # _base.pal_index -> bmp_index
            used_indices = sorted(set(original_pixel_data))
            
            for bmp_idx in used_indices:
                if bmp_idx < len(original_bmp_palette)//3:
                    # Get BMP color
                    r = original_bmp_palette[bmp_idx*3]
                    g = original_bmp_palette[bmp_idx*3+1]
                    b = original_bmp_palette[bmp_idx*3+2]
                    bmp_color = (r, g, b)
                    
                    # Find this BMP color in _base.pal (skip magenta)
                    for base_idx, base_color in enumerate(base_pal_colors):
                        if (base_color == bmp_color and 
                            base_color != (255, 0, 255) and  # SKIP magenta mapping
                            not self.is_universal_keying_color(base_color)):  # SKIP keying colors
                            base_to_bmp_mapping[base_idx] = bmp_idx
                            break
                    
                    # If it's magenta, explicitly skip it
                    if bmp_color == (255, 0, 255):
                        continue
            
            # Step 4: Create final icon palette
            
            new_palette = []
            used_indices = sorted(set(original_pixel_data))
            
            for i in range(256):
                final_color = (255, 0, 255)  # Default magenta background
                
                # SIMPLIFIED: Direct BMP to used_colors mapping (skip magenta)
                if i < len(original_bmp_palette)//3:
                    # Get BMP color
                    r = original_bmp_palette[i*3]
                    g = original_bmp_palette[i*3+1]
                    b = original_bmp_palette[i*3+2]
                    bmp_color = (r, g, b)
                    
                    # Skip keying colors, use 1:1 mapping from vanilla indices to _base.pal
                    if not (bmp_color == (255, 0, 255) or 
                           bmp_color == (0, 255, 0) or 
                           self.is_universal_keying_color(bmp_color)):
                        
                        # Find this BMP color in _base.pal to get the _base.pal index
                        base_pal_idx = None
                        for base_idx, base_color in enumerate(base_pal_colors):
                            if base_color == bmp_color:
                                base_pal_idx = base_idx
                                break
                        
                        if base_pal_idx is not None:
                            # Use the mapped custom palette color for this base palette index
                            if base_pal_idx in base_to_custom_mapping:
                                final_color = base_to_custom_mapping[base_pal_idx]
                            else:
                                final_color = (255, 0, 255)  # Use magenta for unmapped colors
                        else:
                            final_color = (255, 0, 255)  # Use magenta if not found in base palette
                    else:
                        final_color = (255, 0, 255)  # Use magenta for keying colors
                
                new_palette.extend([final_color[0], final_color[1], final_color[2]])
            
            
            new_palette_img.putpalette(new_palette)
            new_palette_img.putdata(original_pixel_data)
            
            # Convert to RGB for final processing
            new_img = new_palette_img.convert("RGB")
            
            new_img_sample = list(new_img.getdata())
            unique_colors_after = set(new_img_sample)
            
            # Count pixels of each color
            color_counts = {}
            for color in new_img_sample:
                color_counts[color] = color_counts.get(color, 0) + 1
            
            # Check what specific palette indices are being used and what colors they map to
            for idx in sorted(set(original_pixel_data)):
                if idx < 256:
                    palette_start = idx * 3
                    if palette_start + 2 < len(new_palette):
                        r = new_palette[palette_start]
                        g = new_palette[palette_start + 1] 
                        b = new_palette[palette_start + 2]
                        pixel_count = original_pixel_data.count(idx)
            
            
            # Handle transparency by replacing transparent pixels with keying color
            transparent_count = 0
            opaque_count = 0
            new_img_data = list(new_img.getdata())
            
            for i, pixel in enumerate(new_img_data):
                y = i // img.size[0]
                x = i % img.size[0]
                
                if alpha.getpixel((x, y)) == 0:  # Transparent pixel
                    new_img_data[i] = (255, 0, 255)  # Use magenta for transparent areas (proper BMP keying)
                    transparent_count += 1
                else:
                    opaque_count += 1
            
            new_img.putdata(new_img_data)
            
            # Save as 24-bit BMP
            if palette_path:
                icon_name = os.path.splitext(os.path.basename(palette_path))[0] + ".bmp"
            else:
                icon_name = f"{char_id}_{fashion_type}_{base_bmp_name}.bmp"
            export_path = os.path.join(export_dir, icon_name)
            
            # Create directory if it doesn't exist when actually saving
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            new_img.save(export_path, "BMP")
            return True
            
        except Exception as e:
            return False
    
    def save_as_icon_with_colors(self, char_id: str, fashion_type: str, colors: list, 
                                keying_color: tuple, bmp_path: str, export_path: str) -> bool:
        """Save icon with specific colors (used by IconPaletteEditor)."""
        try:
            # Load the original BMP
            img = Image.open(bmp_path).convert("RGBA")
            alpha = img.split()[3]
            
            # Create new RGB image
            new_img = Image.new("RGB", img.size)
            
            # Load the original image as palette mode to get the palette indices
            original_img_palette = Image.open(bmp_path).convert("P")
            original_pixel_data = list(original_img_palette.getdata())
            
            # Create a new palette-mode image with the provided colors
            new_palette_img = Image.new("P", img.size)
            
            # Create icon palette from the provided colors
            # The colors list is a full 256-element palette where index i is for palette index i
            new_palette = []
            
            # Indices 0-255: Use the provided colors directly (they're already in the correct order)
            for i in range(256):
                if i < len(colors):
                    color = colors[i]
                    new_palette.extend([color[0], color[1], color[2]])
                else:
                    new_palette.extend([0, 0, 0])  # Fill with black
            
            
            new_palette_img.putpalette(new_palette)
            new_palette_img.putdata(original_pixel_data)
            
            # Convert to RGB for final processing
            new_img = new_palette_img.convert("RGB")
            
            new_img_sample = list(new_img.getdata())
            unique_colors_after = set(new_img_sample)
            
            # Handle transparency by replacing transparent pixels with keying color
            new_img_data = list(new_img.getdata())
            
            for i, pixel in enumerate(new_img_data):
                y = i // img.size[0]
                x = i % img.size[0]
                
                if alpha.getpixel((x, y)) == 0:  # Transparent pixel
                    new_img_data[i] = keying_color
            
            new_img.putdata(new_img_data)
            
            # Save as 24-bit BMP
            # Create directory if it doesn't exist when actually saving
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            new_img.save(export_path, "BMP")
            return True
            
        except Exception as e:
            return False

    def _create_base_to_custom_mapping(self, base_pal_colors, custom_palette, char_id, fashion_type):
        """Create a mapping from base palette indices to custom palette colors using multi-pass matching.
        
        Args:
            base_pal_colors: List of RGB tuples from the base/reference palette
            custom_palette: List of RGB tuples from the custom/vanilla palette  
            char_id: Character ID (e.g. 'chr003')
            fashion_type: Fashion type (e.g. 'fashion_2')
            
        Returns:
            dict: base_palette_index -> custom_palette_color mapping
        """
        char_num = char_id[3:] if char_id.startswith('chr') else char_id
        translator = IndexTranslator()
        ranges = translator.original_ranges.get(char_num, {}).get(fashion_type, [])
        
        # Collect candidate colors from custom palette
        candidates = {}  # vanilla_idx -> color
        for r in ranges:
            for idx in range(r.start, r.stop):
                if idx < len(custom_palette) and idx != 0 and idx != 255:
                    color = custom_palette[idx]
                    
                    # Validate color tuple
                    if isinstance(color, (list, tuple)) and len(color) == 3:
                        try:
                            r_val, g_val, b_val = int(color[0]), int(color[1]), int(color[2])
                            if 0 <= r_val <= 255 and 0 <= g_val <= 255 and 0 <= b_val <= 255:
                                color = (r_val, g_val, b_val)
                                # Filter out keying colors
                                if (color != (255, 0, 255) and color != (0, 255, 0) and
                                    not self.is_universal_keying_color(color) and
                                    not self._is_keyed_color(color, idx)):
                                    candidates[idx] = color
                        except (ValueError, TypeError):
                            continue
        
        # Create base_pal to custom_palette mapping using multi-pass matching
        base_to_custom_mapping = {}  # base_pal_index -> custom_palette_color
        matched_base_indices = set()
        unmatched_candidates = dict(candidates)
        
        
        # Pass 1: Direct index-to-index matching
        for vanilla_idx, vanilla_color in list(unmatched_candidates.items()):
            if vanilla_idx < len(base_pal_colors):
                base_color = base_pal_colors[vanilla_idx]
                
                # Check if base palette has a non-keying color at this index
                # For chr003: only key out pure green (0,255,0), green variants, and pure magenta (255,0,255)
                is_keying = False
                if base_color == (255, 0, 255):  # Pure magenta
                    is_keying = True
                elif base_color == (0, 255, 0):  # Pure green  
                    is_keying = True
                elif self.is_universal_keying_color(base_color):  # Green variants
                    is_keying = True
                
                if not is_keying:
                    # Map base palette index to custom palette color
                    base_to_custom_mapping[vanilla_idx] = vanilla_color
                    matched_base_indices.add(vanilla_idx)
                    del unmatched_candidates[vanilla_idx]
        
        # Pass 2+: Match remaining colors by color similarity
        max_passes = 5
        for pass_num in range(max_passes):
            if not unmatched_candidates:
                break
            
            matched_this_pass = []
            
            for vanilla_idx, vanilla_color in unmatched_candidates.items():
                # Find nearest non-keying, non-matched base color
                best_match_idx = None
                best_distance = float('inf')
                
                for base_idx, base_color in enumerate(base_pal_colors):
                    # Skip if already matched
                    if base_idx in matched_base_indices:
                        continue
                    # Skip keying colors in base palette (same logic as Pass 1)
                    is_keying = (base_color == (255, 0, 255) or  # Pure magenta
                                base_color == (0, 255, 0) or     # Pure green
                                self.is_universal_keying_color(base_color))  # Green variants
                    if is_keying:
                        continue
                    
                    # Calculate color distance
                    distance = sum((a - b) ** 2 for a, b in zip(vanilla_color, base_color))
                    
                    if distance < best_distance:
                        best_distance = distance
                        best_match_idx = base_idx
                
                if best_match_idx is not None:
                    base_to_custom_mapping[best_match_idx] = vanilla_color
                    matched_base_indices.add(best_match_idx)
                    matched_this_pass.append(vanilla_idx)
            
            # Remove matched candidates
            for vanilla_idx in matched_this_pass:
                del unmatched_candidates[vanilla_idx]
            
            # If no progress, stop
            if not matched_this_pass:
                break
        
        return base_to_custom_mapping

    def _is_keyed_color(self, rgb_color, palette_index=None):
        """Check if an RGB color is a keyed/transparency color that should be avoided"""
        r, g, b = rgb_color
        
        # Universal keying colors (same logic as main app)
        if self.is_universal_keying_color(rgb_color):
            return True
        
        # Magenta (chroma key)
        if rgb_color == (255, 0, 255):
            return True
        
        # Character-specific keying rules
        if hasattr(self, 'char_id') and self.char_id:
            char_num = self.char_id[3:]  # Extract number from chr###
            
            # chr004 specific rules
            if char_num == "004":
                if rgb_color == (0, 0, 0):  # Black
                    return True
                if palette_index == 255:  # Last color in palette
                    return True
            
            # chr003 (Sheep) - uses universal keying colors
            elif char_num == "003":
                return self.is_chr003_keying_color(rgb_color)
            
            # chr008 (Raccoon) - uses universal keying colors  
            elif char_num == "008":
                return self.is_chr008_keying_color(rgb_color)
            
            # chr011 (Sheep 2nd Job) - uses same as chr003
            elif char_num == "011":
                return self.is_chr011_keying_color(rgb_color)
            
            # chr014 (Lion 2nd Job) - uses selective keying
            elif char_num == "014":
                return self.is_chr014_keying_color(rgb_color)
        
        return False

    def is_universal_keying_color(self, color):
        """Check if a color is a universal keying color for ALL characters"""
        r, g, b = color
        
        # Pure green (0, 255, 0) - used by ALL characters including chr010
        if color == (0, 255, 0):
            return True
        
        # (0~25, 255, 0) pattern - used by chr002, chr008, chr024, and others
        if g == 255 and b == 0 and 0 <= r <= 25:
            return True
        
        # (0, 255, 0~21) pattern - used by chr003, chr011, chr019, and others
        if g == 255 and r == 0 and 0 <= b <= 21:
            return True
        
        return False

    def is_chr003_keying_color(self, color):
        """Check if a color is a keying color for chr003 (Sheep)"""
        # chr003 uses universal keying colors
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr008_keying_color(self, color):
        """Check if a color is a keying color for chr008 (Raccoon)"""
        # chr008 uses universal keying colors
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr011_keying_color(self, color):
        """Check if a color is a keying color for chr011 (Sheep 2nd Job)"""
        # chr011 uses the same keying patterns as chr003
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr014_keying_color(self, color):
        """Check if a color is a keying color for chr014 (Lion 2nd Job)"""
        # chr014 uses more selective keying to avoid over-transparency
        # Only key out pure green and magenta, not green variants
        if color == (0, 255, 0) or color == (255, 0, 255):  # Pure green and magenta
            return True
        return False


class IconPaletteEditor:
    """A mini palette editor specifically for editing icon palettes with live preview."""
    
    def __init__(self, char_id: str, fashion_type: str, custom_palette: list, palette_path: str, palette_layers=None, live_editor_window=None, is_quicksave_mode=False, icon_handler=None):
        self.char_id = char_id
        self.fashion_type = fashion_type
        self.custom_palette = custom_palette
        self.palette_path = palette_path
        self.palette_layers = palette_layers or []
        self.live_editor_window = live_editor_window
        self.is_quicksave_mode = is_quicksave_mode
        self.icon_handler = icon_handler
        
        # Initialize UI variables first
        self.multi_select_var = tk.BooleanVar(value=False)
        self.index_var = tk.StringVar(value="0")
        self.hex_var = tk.StringVar(value="#000000")
        self.hue_var = tk.IntVar(value=0)
        self.sat_var = tk.IntVar(value=0)
        self.val_var = tk.IntVar(value=0)
        self.selection_count_var = tk.StringVar(value="(0 selected)")
        self.selected_index = 0
        self.selected_indices = set()
        self.saved_colors = [(0, 0, 0)] * 20
        self.saved_mode = "R"  # "R" for right-click save (default), "L" for left-click save
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
        self.inverse_order_var = tk.BooleanVar(value=False)  # For inverse palette order (if UI supports it)
        
        # HSV adjustment settings with defaults (same as fashionpreviewer.py)
        self._gradient_adjust_hue = True
        self._gradient_adjust_saturation = False
        self._gradient_adjust_value = False
        
        # Temporary palette cache to preserve changes during editor session
        self._temp_palette_cache = {}  # Cache for temporary changes during session
        self._original_palettes = {}  # Store original colors for cleanup when editor closes
        
        # Get paths to reference files
        self.icon_handler = IconHandler()
        item_name = self.icon_handler._get_fashion_name(char_id, fashion_type)
        self.image_path, self.ref_pal_path = self.icon_handler._get_icon_paths(char_id, item_name)
        
        
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
        
        # Current edited colors (convert dict to full palette for compatibility)
        self.current_colors = self.custom_palette.copy()  # Start with full palette
        # Update only the editable positions with extracted colors
        for idx, color in self.editable_colors.items():
            if idx < len(self.current_colors):
                self.current_colors[idx] = color
        
        # Create UI
        self._create_ui()
        
        # Load preview
        self._update_preview()
        
        # Initialize the last palette key
        self._last_palette_key = f"{self.char_id}_{self.fashion_type}"
        
        # Initialize temporary cache with current colors
        current_palette_key = f"{self.char_id}_{self.fashion_type}"
        self._temp_palette_cache[current_palette_key] = self.current_colors.copy()
        self._original_palettes[current_palette_key] = self.current_colors.copy()
        
        # Center the icon editor window after content is created
        self.window.update_idletasks()
        self._center_window_on_parent()
        
        # Prompt user to save excess colors after window is shown
        self.window.after(100, self._prompt_save_excess_colors)
    
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

    
    def _find_nearest_non_keyed_color(self, target_rgb, adjustment_direction='both'):
        """Find the nearest non-keyed color by adjusting RGB values with precise increments"""
        r, g, b = target_rgb
        
        # If the color is not keyed, return it as-is
        if not self._is_keyed_color(target_rgb):
            return target_rgb
        
        # Try precise adjustment strategies - start with small increments, then larger
        distance_steps = [1, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50]  # Precise increments first
        
        for offset in distance_steps:
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
            pass
    
    def _extract_editable_colors(self):
        """Extract ONLY the editable colors with multi-pass matching to reference PAL.
        
        Uses a smart matching algorithm:
        1. First pass: Match custom colors to reference PAL colors
        2. Detect collisions (multiple customs mapping to same reference)
        3. Second+ passes: Match unmatched colors to nearest available neighbors
        """
        # Validate custom_palette
        if not self.custom_palette or not isinstance(self.custom_palette, list):
            return {0: (128, 128, 128)}  # Return dict with single default color
        
        # Get the valid ranges for this fashion type
        char_num = self.char_id[3:] if self.char_id.startswith('chr') else self.char_id
        translator = IndexTranslator()
        ranges = translator.original_ranges.get(char_num, {}).get(self.fashion_type, [])
        
        # First, collect all candidate colors from custom palette (excluding keying colors)
        candidates = {}  # idx -> color
        
        for r in ranges:
            for idx in range(r.start, r.stop):
                if idx < len(self.custom_palette) and idx != 0 and idx != 255:
                    color = self.custom_palette[idx]
                    
                    # Validate and convert color tuple
                    if not isinstance(color, (list, tuple)) or len(color) != 3:
                        continue
                    
                    try:
                        r_val, g_val, b_val = int(color[0]), int(color[1]), int(color[2])
                        if not (0 <= r_val <= 255 and 0 <= g_val <= 255 and 0 <= b_val <= 255):
                            continue
                        color = (r_val, g_val, b_val)
                    except (ValueError, TypeError):
                        continue
                    
                    # Filter out keying colors
                    if color == (255, 0, 255) or color == (0, 255, 0):
                        continue
                    if self._is_keyed_color(color, idx):
                        continue
                    
                    candidates[idx] = color
        
        if not candidates:
            return {111: (128, 128, 128)}
        
        # If no reference palette, return all candidates
        if not hasattr(self, 'ref_colors') or not self.ref_colors:
            return candidates
        
        # Use the same mapping logic as preview/save for consistency
        # Create a mapping from base palette indices to custom palette colors
        base_to_custom_mapping = self.icon_handler._create_base_to_custom_mapping(
            self.ref_colors, self.custom_palette, self.char_id, self.fashion_type
        )
        
        
        
        # The key insight: if a vanilla color is used in the base_to_custom_mapping,
        # then that vanilla index should be editable, regardless of other filtering
        editable_colors = {}
        
        # Include ALL vanilla indices that produce colors used by the icon
        for vanilla_idx in candidates.keys():
            vanilla_color = candidates[vanilla_idx]
            
            # Check if this vanilla color is actually used by the base palette mapping
            is_used = False
            for base_idx, mapped_color in base_to_custom_mapping.items():
                if mapped_color == vanilla_color:
                    is_used = True
                    break
            
            if is_used:
                editable_colors[vanilla_idx] = vanilla_color
        
        # Count non-keying base palette colors
        non_keying_base_count = 0
        for base_idx, base_color in enumerate(self.ref_colors):
            if (base_color != (255, 0, 255) and base_color != (0, 255, 0) and
                not self.is_universal_keying_color(base_color) and
                not self._is_keyed_color(base_color, base_idx)):
                non_keying_base_count += 1
        
        # IMPROVED LOGIC: Include additional candidates even if there are fewer base colors
        # This handles cases where vanilla palette has more useful colors than the base palette
        expected_editable_count = max(non_keying_base_count, 4)  # At least 4 colors for bow
        
        if len(editable_colors) < expected_editable_count:
            # Sort candidates by index to get the most relevant ones first
            sorted_candidates = sorted(candidates.items(), key=lambda x: x[0])
            
            # Add candidates until we have a reasonable number for editing
            for vanilla_idx, vanilla_color in sorted_candidates:
                if vanilla_idx not in editable_colors:
                    editable_colors[vanilla_idx] = vanilla_color
                    
                    # Stop when we have enough colors
                    if len(editable_colors) >= expected_editable_count:
                        break
        
        # Fallback: if still no colors, include all candidates
        if not editable_colors:
            editable_colors = candidates
        
        # If still no matches, provide default
        if not editable_colors:
            editable_colors = {111: (128, 128, 128)}
        
        # Store unmatched candidates for later extraction to JSON
        # Calculate unmatched candidates as those not included in editable_colors
        unmatched_candidates = {}
        for vanilla_idx, vanilla_color in candidates.items():
            if vanilla_idx not in editable_colors:
                unmatched_candidates[vanilla_idx] = vanilla_color
        self._unmatched_candidates = unmatched_candidates
        
        
        return editable_colors
    
    def _extract_unused_colors(self):
        """Extract colors from palette indexes that are NOT used by the icon (excess colors).
        This includes:
        1. Unmatched colors from multi-pass matching algorithm
        2. Colors at indexes where reference PAL has keying colors (icon doesn't use them)
        3. Colors outside the valid fashion ranges (but NOT keying colors)
        4. Non-keying colors within valid ranges that are unused by the icon
        
        All extracted colors exclude keying colors (magenta, green, character-specific) for JSON export.
        """
        # Validate custom_palette
        if not self.custom_palette or not isinstance(self.custom_palette, list):
            return []
        
        # Get the valid ranges for this fashion type
        char_num = self.char_id[3:] if self.char_id.startswith('chr') else self.char_id
        translator = IndexTranslator()
        ranges = translator.original_ranges.get(char_num, {}).get(self.fashion_type, [])
        
        # Create a set of all indexes in valid ranges
        valid_range_indexes = set()
        for r in ranges:
            for idx in range(r.start, r.stop):
                valid_range_indexes.add(idx)
        
        # Extract unused colors from multiple sources:
        unused_colors = []
        processed_indices = set()  # Track which indices we've already processed
        
        # IMPORTANT: Exclude all editable/active colors from excess colors
        # Get the editable colors indices to avoid including them in excess
        editable_indices = set()
        if hasattr(self, 'editable_colors') and self.editable_colors:
            editable_indices = set(self.editable_colors.keys())
            processed_indices.update(editable_indices)  # Mark all editable indices as processed
            
        
        # Source 0: Unmatched colors from multi-pass matching (highest priority)
        if hasattr(self, '_unmatched_candidates') and self._unmatched_candidates:
            for idx, color in self._unmatched_candidates.items():
                if isinstance(color, (list, tuple)) and len(color) == 3:
                    # Already validated and filtered in _extract_editable_colors
                    color_list = [int(color[0]), int(color[1]), int(color[2])]
                    if color_list not in unused_colors:
                        unused_colors.append(color_list)
                        processed_indices.add(idx)
        
        # Source 1: Colors where REFERENCE PAL has keying colors (icon doesn't use these indexes)
        if hasattr(self, 'ref_colors') and self.ref_colors:
            for idx in valid_range_indexes:
                # Skip if already processed
                if idx in processed_indices:
                    continue
                    
                if idx < len(self.custom_palette) and idx < len(self.ref_colors) and idx != 0 and idx != 255:
                    ref_color = self.ref_colors[idx]
                    custom_color = self.custom_palette[idx]
                    
                    # Check if reference PAL has a keying color at this index
                    ref_is_keyed = (ref_color == (255, 0, 255) or 
                                   ref_color == (0, 255, 0) or 
                                   self.is_universal_keying_color(ref_color) or
                                   self._is_keyed_color(ref_color, idx))
                    
                    if ref_is_keyed:
                        # Reference has keying color, so icon doesn't use this index
                        # But only save if custom palette has a valid, non-keying color
                        if isinstance(custom_color, (list, tuple)) and len(custom_color) == 3:
                            try:
                                r_val, g_val, b_val = int(custom_color[0]), int(custom_color[1]), int(custom_color[2])
                                if 0 <= r_val <= 255 and 0 <= g_val <= 255 and 0 <= b_val <= 255:
                                    # Don't save magenta/green from custom palette
                                    if (r_val, g_val, b_val) not in [(255, 0, 255), (0, 255, 0)]:
                                        # Also skip if custom color is a keying color
                                        if not self.is_universal_keying_color((r_val, g_val, b_val)):
                                            color_list = [r_val, g_val, b_val]
                                            if color_list not in unused_colors:
                                                unused_colors.append(color_list)
                                                processed_indices.add(idx)
                            except (ValueError, TypeError):
                                pass
        
        # Source 2: Non-keying colors in custom palette WITHIN valid ranges that are unused
        for idx in valid_range_indexes:
            # Skip if already processed
            if idx in processed_indices:
                continue
                
            if idx < len(self.custom_palette) and idx != 0 and idx != 255:
                color = self.custom_palette[idx]
                
                # Validate color tuple
                if isinstance(color, (list, tuple)) and len(color) == 3:
                    try:
                        r_val, g_val, b_val = int(color[0]), int(color[1]), int(color[2])
                        if 0 <= r_val <= 255 and 0 <= g_val <= 255 and 0 <= b_val <= 255:
                            # Only save NON-keying colors that are in valid ranges but unused by icon
                            if not self._is_keyed_color((r_val, g_val, b_val), idx):
                                # Additional check: skip magenta/green even if not detected as keyed
                                if (r_val, g_val, b_val) not in [(255, 0, 255), (0, 255, 0)]:
                                    # Skip universal keying colors as extra safety
                                    if not self.is_universal_keying_color((r_val, g_val, b_val)):
                                        color_list = [r_val, g_val, b_val]
                                        if color_list not in unused_colors:
                                            unused_colors.append(color_list)
                                            processed_indices.add(idx)
                    except (ValueError, TypeError):
                        pass
        
        # Source 3: Colors OUTSIDE valid ranges (truly unused indexes)
        for idx in range(len(self.custom_palette)):
            # Skip if in valid ranges or already processed
            if idx in valid_range_indexes or idx in processed_indices:
                continue
                
            if idx != 0 and idx != 255:
                color = self.custom_palette[idx]
                
                # Validate color tuple
                if isinstance(color, (list, tuple)) and len(color) == 3:
                    try:
                        r_val, g_val, b_val = int(color[0]), int(color[1]), int(color[2])
                        if 0 <= r_val <= 255 and 0 <= g_val <= 255 and 0 <= b_val <= 255:
                            # Use comprehensive keying detection to exclude ALL keying colors
                            if not self._is_keyed_color((r_val, g_val, b_val), idx):
                                # Additional safety checks: skip magenta/green explicitly
                                if (r_val, g_val, b_val) not in [(255, 0, 255), (0, 255, 0)]:
                                    # Skip universal keying colors as extra safety
                                    if not self.is_universal_keying_color((r_val, g_val, b_val)):
                                        color_list = [r_val, g_val, b_val]
                                        if color_list not in unused_colors:
                                            unused_colors.append(color_list)
                                            processed_indices.add(idx)
                    except (ValueError, TypeError):
                        pass
        
        return unused_colors
    
    def _prompt_save_excess_colors(self):
        """Prompt user to save excess/unused colors from the palette as JSON."""
        import json
        
        # Extract unused colors
        unused_colors = self._extract_unused_colors()
        
        if not unused_colors:
            return  # No excess colors to save
        
        # Check if user has opted to not show this dialog again
        if self._get_excess_colors_preference():
            return  # User chose "don't show again"
        
        # Create custom dialog with options
        response, dont_show_option = self._show_excess_colors_dialog(len(unused_colors))
        
        # Handle the different "don't show" options
        if dont_show_option == "forever":
            # Save permanently to settings.json
            self._save_excess_colors_preference(True)
        elif dont_show_option == "session":
            # Set session-only flag (will be cleared when program closes)
            self._set_session_excess_colors_preference(True)
        
        if not response:
            return
        
        # Prepare colors for saved colors format (limit to 20 slots, matching saved_colors capacity)
        colors_to_save = unused_colors[:20]
        
        # Pad with black if less than 20
        while len(colors_to_save) < 20:
            colors_to_save.append([0, 0, 0])
        
        # Default to exports/colors/json directory
        default_dir = os.path.join(self.icon_handler.root_dir, "exports", "colors", "json")
        os.makedirs(default_dir, exist_ok=True)
        
        # Generate a default filename based on the ACTUAL palette being edited
        # Extract base name from palette_path (e.g., "chr001_w17.pal" -> "chr001_w17")
        palette_basename = os.path.splitext(os.path.basename(self.palette_path))[0]
        # Replace "temp_" prefix if present (from main UI opening)
        if palette_basename.startswith('temp_'):
            palette_basename = palette_basename[5:]  # Remove "temp_" prefix
        
        # Get fashion type name and clean it (remove spaces and special chars)
        fashion_name = self.icon_handler._get_fashion_name(self.char_id, self.fashion_type)
        clean_fashion_name = ''.join(c for c in fashion_name if c.isalnum())
        
        # Format: chr###_w##########_excess_FashionTypeName.json
        default_filename = f"{palette_basename}_excess_{clean_fashion_name}.json"
        
        # Open save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            title="Save Excess Colors",
            initialdir=default_dir,
            initialfile=default_filename,
            parent=self.window
        )
        
        # Bring the icon editor window back to front after file dialog closes
        self._bring_to_front()
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(colors_to_save, f)
            messagebox.showinfo(
                "Success", 
                f"Saved {len(unused_colors)} excess colors to:\n{os.path.basename(file_path)}",
                parent=self.window
            )
            self._bring_to_front()
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Failed to save excess colors: {e}",
                parent=self.window
            )
            self._bring_to_front()
    
    def _show_excess_colors_dialog(self, num_colors):
        """Show custom dialog with 'don't show again' options.
        
        Args:
            num_colors: Number of excess colors found
            
        Returns:
            tuple: (user_response, dont_show_option) where user_response is True/False for Yes/No,
                   and dont_show_option is "show"/"session"/"forever"
        """
        # Create custom dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Save Excess Colors")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = 450
        height = 280  # Increased from 200 to 280 to accommodate all content and buttons
        x = (dialog.winfo_screenwidth() - width) // 2
        y = (dialog.winfo_screenheight() - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Message
        message = (f"Found {num_colors} unused color indexes in the palette.\n\n"
                  "Would you like to save these excess colors as JSON for reference?\n"
                  "(Can be loaded into the saved colors box)")
        tk.Label(dialog, text=message, wraplength=400, justify="center").pack(pady=20)
        
        # Button frame (create first, pack later)
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        # Options for "don't show again" (create variable first)
        dont_show_option = tk.StringVar(value="show")  # Default to showing
        
        result = {"response": False, "dont_show_option": "show"}
        
        def on_yes():
            result["response"] = True
            result["dont_show_option"] = dont_show_option.get()
            dialog.destroy()
        
        def on_no():
            result["response"] = False
            result["dont_show_option"] = dont_show_option.get()
            dialog.destroy()
        
        # Yes/No buttons
        tk.Button(button_frame, text="Yes", command=on_yes, width=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="No", command=on_no, width=10).pack(side="left", padx=5)

        # Options frame (packed after buttons, so appears below)
        options_frame = tk.Frame(dialog)
        options_frame.pack(pady=5)
        
        tk.Radiobutton(options_frame, text="Keep showing this dialog", 
                      variable=dont_show_option, value="show").pack(anchor="w")
        tk.Radiobutton(options_frame, text="Don't show again this session", 
                      variable=dont_show_option, value="session").pack(anchor="w")
        tk.Radiobutton(options_frame, text="Don't show again forever", 
                      variable=dont_show_option, value="forever").pack(anchor="w")

        # Wait for dialog to close
        dialog.wait_window()
        
        return result["response"], result["dont_show_option"]
    
    def _get_excess_colors_preference(self):
        """Load the 'don't show excess colors prompt' preference.
        
        Returns:
            bool: True if user chose to not show the dialog again, False otherwise
        """
        import json
        
        # Check session-only setting first (has priority)
        if hasattr(self, '_session_dont_show_excess') and self._session_dont_show_excess:
            return True
        
        try:
            # Check permanent setting in src/settings.json
            settings_path = os.path.join(self.icon_handler.root_dir, "src", "settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    # Check in global settings
                    return settings.get('global', {}).get('dont_show_excess_colors_prompt', False)
        except Exception:
            pass
        
        return False
    
    def _set_session_excess_colors_preference(self, dont_show):
        """Set the session-only 'don't show excess colors prompt' preference.
        This setting is cleared when the icon editor is closed.
        
        Args:
            dont_show: True to suppress the dialog for this session only
        """
        self._session_dont_show_excess = dont_show
    
    def _save_excess_colors_preference(self, dont_show):
        """Save the 'don't show excess colors prompt' preference.
        
        Args:
            dont_show: True to suppress the dialog in the future, False otherwise
        """
        import json
        
        try:
            # Use src/settings.json
            settings_path = os.path.join(self.icon_handler.root_dir, "src", "settings.json")
            settings = {'global': {}, 'per_character': {}}
            
            # Load existing settings if file exists
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
            
            # Ensure global key exists
            if 'global' not in settings:
                settings['global'] = {}
            
            # Update the preference in global settings
            settings['global']['dont_show_excess_colors_prompt'] = dont_show
            
            # Save settings
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Failed to save excess colors preference: {e}")
    
    def _prompt_save_loaded_excess_colors(self, excess_colors, source_pal_path):
        """Prompt user to save excess colors found when loading a PAL file.
        
        Args:
            excess_colors: List of RGB tuples that are excess colors (already filtered for keying colors)
            source_pal_path: Path to the PAL file that was loaded
        """
        import json
        
        if not excess_colors:
            return  # No excess colors to save
        
        # Ask user if they want to save excess colors
        response = messagebox.askyesno(
            "Save Excess Colors",
            f"Found {len(excess_colors)} excess colors in the loaded palette\n"
            f"(colors beyond what the icon uses).\n\n"
            "Would you like to save these excess colors as JSON for reference?\n"
            "(Can be loaded into the saved colors box)",
            parent=self.window
        )
        
        if not response:
            return
        
        # Convert tuples to lists for JSON compatibility
        colors_to_save = [[r, g, b] for r, g, b in excess_colors[:20]]
        
        # Pad with black if less than 20
        while len(colors_to_save) < 20:
            colors_to_save.append([0, 0, 0])
        
        # Default to exports/colors/json directory
        default_dir = os.path.join(self.icon_handler.root_dir, "exports", "colors", "json")
        os.makedirs(default_dir, exist_ok=True)
        
        # Generate a default filename based on source palette name
        palette_basename = os.path.splitext(os.path.basename(source_pal_path))[0]
        default_filename = f"{palette_basename}_excess_colors.json"
        
        # Open save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            title="Save Excess Colors",
            initialdir=default_dir,
            initialfile=default_filename,
            parent=self.window
        )
        
        # Bring the icon editor window back to front after file dialog closes
        self._bring_to_front()
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(colors_to_save, f)
            messagebox.showinfo(
                "Success", 
                f"Saved {len(excess_colors)} excess colors to:\n{os.path.basename(file_path)}",
                parent=self.window
            )
            self._bring_to_front()
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Failed to save excess colors: {e}",
                parent=self.window
            )
            self._bring_to_front()
    
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
        
        select_all_btn = ttk.Button(multi_frame, text="Select All", command=self._select_all)
        select_all_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        clear_sel_btn = ttk.Button(multi_frame, text="Clear Sel", command=self._clear_selection)
        clear_sel_btn.pack(side=tk.LEFT, padx=(5, 0))
        
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
                    # Skip hair and third job layers - don't include them in the dropdown
                    if layer.palette_type in ('hair', '3rd_job_base'):
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
        self.saved_mode_button = ttk.Button(saved_btn_frame, text="R", command=self._toggle_saved_mode, width=3)
        self.saved_mode_button.pack(side=tk.RIGHT)
        
        # Saved colors instructions on one line (dynamic based on mode)
        self.saved_instructions_label = ttk.Label(right_frame, text="Right click below to save color / Left click above to apply color", font=("Arial", 8))
        self.saved_instructions_label.pack(anchor=tk.W, pady=(0, 1))
        
        # Saved colors grid
        self.saved_colors_frame = ttk.Frame(right_frame)
        self.saved_colors_frame.pack(fill=tk.X, pady=(0, 1))
        self._create_saved_colors_grid()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Quick export button
        ttk.Button(button_frame, text="Quick Export Icon", command=lambda: self._quick_export("icon")).pack(side=tk.LEFT, padx=(0, 10))
        
        # Regular buttons
        ttk.Button(button_frame, text="Export as Icon", command=self._export_icon).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Reset to Original", command=self._reset_colors).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Close", command=self._close_editor).pack(side=tk.RIGHT)
        
        # Initialize UI
        self._update_color_picker()
        self._update_preview()
    
    def _create_palette_grid(self):
        """Create the palette grid showing only the editable colors with their original indexes."""
        # Clear existing squares
        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        self.palette_squares = []
        
        # Use the already-filtered editable_colors dictionary which has keying colors removed
        # This ensures consistency with the extraction logic
        all_editable_indexes = sorted(self.editable_colors.keys())
        
        # Build list of (index, color) pairs for editable colors only - in EXACT index order
        editable_index_colors = []
        for idx in all_editable_indexes:
            if idx < len(self.current_colors):
                editable_index_colors.append((idx, self.current_colors[idx]))
        
        
        # Create mapping from display position to original index for selection logic
        self.display_to_original_index = {}
        self.original_to_display_index = {}
        for display_idx, (original_idx, color) in enumerate(editable_index_colors):
            self.display_to_original_index[display_idx] = original_idx
            self.original_to_display_index[original_idx] = display_idx
        
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
        for i, (original_idx, color) in enumerate(editable_index_colors):
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
                hex_color = "#808080"  # Default gray
            
            square.create_rectangle(0, 0, square_size, square_size, fill=hex_color, outline="black")
            
            # Bind click events using the ORIGINAL index, not the display index
            square.bind("<Button-1>", lambda e, idx=original_idx: self._on_palette_square_click(idx, "left", e.state))
            square.bind("<Button-3>", lambda e, idx=original_idx: self._on_palette_square_click(idx, "right", e.state))
            
            # Store reference
            self.palette_squares.append(square)
        
        # Update canvas scroll region
        self.palette_frame.update_idletasks()
        self.palette_canvas.configure(scrollregion=self.palette_canvas.bbox("all"))
        
        # Select first color by default (using the original index of the first displayed square)
        if self.palette_squares and self.display_to_original_index:
            first_original_idx = self.display_to_original_index.get(0, 0)
            self._select_color(first_original_idx, "left", 0)
    
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
                    if hasattr(self, 'original_to_display_index') and index in self.original_to_display_index:
                        display_idx = self.original_to_display_index[index]
                        if display_idx < len(self.palette_squares):
                            square = self.palette_squares[display_idx]
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
            # Convert display index to original index
            original_idx = self.display_to_original_index.get(i, i)
            if original_idx in self.selected_indices:
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
            # Convert display index to original index
            original_idx = self.display_to_original_index.get(i, i)
            if original_idx in self.selected_indices:
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
            
            # Set flag to prevent callbacks during slider updates
            old_flag = getattr(self, '_updating_selection', False)
            self._updating_selection = True
            try:
                # Update sliders (without triggering change event)
                self.hue_var.set(int(h * 360))
                self.sat_var.set(int(s * 100))
                self.val_var.set(int(v * 100))
            finally:
                # Restore the flag to its previous state
                self._updating_selection = old_flag
            
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
            # Clamp additive deltas to prevent extreme changes when base color is near black/gray
            dS = max(-50, min(50, S_new - bs)) if not use_scaleS else 0
            dV = max(-50, min(50, V_new - bv)) if not use_scaleV else 0
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
                        # Additional safety: don't apply extreme negative dV to colors that aren't already dark
                        if dV < -20 and v > 20:  # If trying to apply large negative change to bright color
                            v = max(20, min(100, int(round(v + max(dV, -20)))))  # Limit the darkening
                        else:
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
                if hasattr(self, 'original_to_display_index') and idx in self.original_to_display_index:
                    display_idx = self.original_to_display_index[idx]
                    if display_idx < len(self.palette_squares):
                        square = self.palette_squares[display_idx]
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
    
    def _bring_to_front(self):
        """Bring the icon editor window to front."""
        self.window.lift()
        self.window.focus_force()
        
    def _close_editor(self):
        """Close the editor and clean up the instance."""
        # Clean up temporary cache
        if hasattr(self, '_temp_palette_cache'):
            delattr(self, '_temp_palette_cache')
        if hasattr(self, '_original_palettes'):
            delattr(self, '_original_palettes')
        
        # Clear session-only excess colors preference
        if hasattr(self, '_session_dont_show_excess'):
            delattr(self, '_session_dont_show_excess')
        
        # Restore focus to main UI window if it exists
        try:
            if hasattr(self, 'icon_handler') and self.icon_handler and hasattr(self.icon_handler, 'main_window'):
                main_window = self.icon_handler.main_window
                if main_window and hasattr(main_window, 'master') and main_window.master.winfo_exists():
                    # Restore focus to main window
                    main_window.master.focus_force()
                    main_window.master.lift()
                    
                    # Update navigation button states to ensure they work properly
                    if hasattr(main_window, 'update_navigation_buttons'):
                        main_window.update_navigation_buttons()
        except Exception as e:
            # Silent fallback - don't show error dialog during cleanup
            pass
        
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
                self._original_palettes[old_palette_key] = self.current_colors.copy()
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
                            # COMPLETE REINITIALIZATION - as if opening editor fresh with this palette
                            
                            # Update to NEW character and fashion type
                            self.char_id = char_id
                            self.fashion_type = layer.palette_type
                            
                            # Update palette_path to the NEW palette name
                            self.palette_path = layer.name if hasattr(layer, 'name') else f"{char_id}_{layer.palette_type}.pal"
                            
                            # Get NEW icon paths for the selected character/fashion type
                            item_name = self.icon_handler._get_fashion_name(char_id, layer.palette_type)
                            self.image_path, self.ref_pal_path = self.icon_handler._get_icon_paths(char_id, item_name)
                            
                            # Clear all cached state to force fresh extraction
                            self.ref_colors = []
                            self.keying_color = (255, 0, 255)
                            self._unmatched_candidates = {}
                            
                            # Load the NEW reference palette
                            self._load_reference_palette()
                            
                            # ALWAYS initialize custom_palette with NEW layer colors first
                            self.custom_palette = layer.colors if hasattr(layer, 'colors') else []
                            
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
                                        # Override with saved palette colors
                                        try:
                                            with open(saved_palette_path, 'rb') as f:
                                                pal_data = f.read()
                                            
                                            # Parse the saved palette
                                            saved_palette = []
                                            for i in range(0, len(pal_data), 3):
                                                if i + 2 < len(pal_data):
                                                    r, g, b = pal_data[i], pal_data[i+1], pal_data[i+2]
                                                    saved_palette.append((r, g, b))
                                            
                                            # Override the default layer colors with saved palette
                                            self.custom_palette = saved_palette
                                        except Exception as e:
                                            # Keep layer colors (already set above)
                                            pass
                                else:
                                    # No saved palette found, try to load vanilla palette
                                    vanilla_palette = self._load_vanilla_palette_for_item(char_id, layer.palette_type, layer.name)
                                    if vanilla_palette:
                                        # Override with vanilla palette
                                        self.custom_palette = vanilla_palette
                                    # else: keep layer colors (already set above)
                            
                            # Extract editable colors - this will generate fresh _unmatched_candidates
                            self.editable_colors = self._extract_editable_colors()
                            
                            # Create a FRESH full palette with all indices (from scratch)
                            full_palette = [(0, 0, 0)] * 256  # Initialize with black
                            
                            # Fill in the editable colors at their correct indices
                            for idx, color in self.editable_colors.items():
                                if idx < 256:  # Safety check
                                    full_palette[idx] = color
                            
                            # Check if we have cached temporary changes for this palette
                            new_palette_key = f"{char_id}_{layer.palette_type}"
                            if hasattr(self, '_temp_palette_cache') and new_palette_key in self._temp_palette_cache:
                                # Restore from temp cache to preserve temporary changes
                                cached_colors = self._temp_palette_cache[new_palette_key]
                                # Update only the editable indices from cache
                                for idx in self.editable_colors.keys():
                                    if idx < len(cached_colors):
                                        full_palette[idx] = cached_colors[idx]
                            
                            # Set current_colors to the full palette (after cache restoration)
                            self.current_colors = full_palette
                            
                            # Update cache
                            if hasattr(self, '_temp_palette_cache'):
                                self._temp_palette_cache[new_palette_key] = self.current_colors.copy()
                                self._original_palettes[new_palette_key] = self.current_colors.copy()
                            
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
                            
                            # Prompt to save excess colors from the NEW palette after extraction
                            self._prompt_save_excess_colors()
                            
                            # Clear protection flags after successful switch with delay
                            self._clear_protection_flags()
                            return  # Exit after successful switch
                            
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
                        return False
        
        # For other palette types, do a more general match
        else:
            # Check if the layer name (without extension) is contained in the saved filename
            base_layer_name = os.path.splitext(layer_name)[0].lower()
            base_saved_name = os.path.splitext(saved_filename)[0].lower()
            
            if base_layer_name == base_saved_name:
                return True
            else:
                return False
        
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
                    # Skip hair and third job layers - don't include them in the dropdown
                    if layer.palette_type in ('hair', '3rd_job_base'):
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
        root_dir = getattr(self, "root_dir", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
                            continue
        
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
    
    def _select_all(self):
        """Select all editable colors."""
        # Prevent color changes during selection update
        self._updating_selection = True
        try:
            # Enable multi-select mode to allow relative HSV adjustments
            self.multi_select_var.set(True)
            
            # Select all indices from editable_colors
            self.selected_indices = set(self.editable_colors.keys())
            if self.selected_indices:
                self.selected_index = min(self.selected_indices)
            self._update_selection_highlights()
            self._update_color_picker()
            # Force pending events to process before clearing flag
            if hasattr(self, 'window') and self.window:
                self.window.update_idletasks()
        finally:
            self._updating_selection = False
    
    def _clear_selection(self):
        """Clear all selected colors."""
        self.selected_indices = set()
        self.selected_index = 0
        self._update_selection_highlights()
        self._update_color_picker()
    
    def _update_selection_highlights(self):
        """Update the selection highlights in the grid."""
        # Keep highlightthickness consistent to prevent grid movement
        for display_idx, square in enumerate(self.palette_squares):
            # Get the original index for this display position
            if hasattr(self, 'display_to_original_index') and display_idx in self.display_to_original_index:
                original_idx = self.display_to_original_index[display_idx]
                if original_idx in self.selected_indices:
                    square.configure(highlightbackground="red", highlightthickness=1)
                else:
                    square.configure(highlightbackground="black", highlightthickness=1)
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
        """Save current color to a saved color slot."""
        if self.selected_index < len(self.current_colors):
            self.saved_colors[slot_index] = self.current_colors[self.selected_index]
            # Update only the specific square instead of recreating the entire grid
            self._update_saved_color_square(slot_index)
    
    def _load_from_slot(self, slot_index):
        """Load color from a saved color slot to selected color(s)."""
        if self.saved_colors[slot_index] != (0, 0, 0):  # Only load if slot is not empty
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
                if hasattr(self, 'original_to_display_index') and idx in self.original_to_display_index:
                    display_idx = self.original_to_display_index[idx]
                    if display_idx < len(self.palette_squares):
                        square = self.palette_squares[display_idx]
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
        """Toggle between R (right-click save, default) and L (left-click save) mode."""
        if self.saved_mode == "R":
            self.saved_mode = "L"
            # Update button text to show current mode
            self.saved_mode_button.configure(text="L")
            # Update instructions text
            self.saved_instructions_label.configure(text="Left click below to save color / Right click above to apply color")
        else:
            self.saved_mode = "R"
            # Update button text to show current mode
            self.saved_mode_button.configure(text="R")
            # Update instructions text
            self.saved_instructions_label.configure(text="Right click below to save color / Left click above to apply color")
    
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
            if hasattr(self, 'original_to_display_index') and index in self.original_to_display_index:
                display_idx = self.original_to_display_index[index]
                if display_idx < len(self.palette_squares):
                    square = self.palette_squares[display_idx]
                    hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                    square.delete("all")
                    square.create_rectangle(0, 0, 80, 80, fill=hex_color, outline="black")
            
            # Update preview
            self._update_preview()
    
    def _update_preview(self):
        """Update the live preview of the icon with proper palette translation."""
        try:
            # Use only BMP files for consistency
            bmp_path = self.image_path
            if not os.path.exists(bmp_path):
                return
            
            # Load the BMP file for both image data and palette
            bmp_img = Image.open(bmp_path)
            if bmp_img.mode != 'P':
                bmp_img = bmp_img.convert('P')
            
            # For transparency, we'll treat the keying color (magenta) as transparent
            # Convert to RGBA to create alpha channel from keying color
            img = bmp_img.convert("RGBA")
            alpha_data = []
            
            # Create alpha channel: transparent where keying color exists
            for pixel in img.getdata():
                if pixel[:3] == self.keying_color:  # Keying color (usually magenta)
                    alpha_data.append(0)  # Transparent
                else:
                    alpha_data.append(255)  # Opaque
            
            # Create alpha channel
            alpha = Image.new('L', img.size)
            alpha.putdata(alpha_data)
            
            # Get BMP palette and pixel data
            bmp_palette_data = bmp_img.getpalette()
            if not bmp_palette_data:
                return
            
            # Convert palette to RGB tuples
            bmp_palette = []
            for i in range(0, len(bmp_palette_data), 3):
                if i + 2 < len(bmp_palette_data):
                    bmp_palette.append((bmp_palette_data[i], bmp_palette_data[i+1], bmp_palette_data[i+2]))
            
            # Get BMP pixel indices
            bmp_pixels = list(bmp_img.getdata())
            
            # Load the base palette (_base.pal)
            base_pal_colors = []
            if self.ref_pal_path and os.path.exists(self.ref_pal_path):
                with open(self.ref_pal_path, 'rb') as f:
                    base_pal_data = f.read()
                    for i in range(0, len(base_pal_data), 3):
                        if i + 2 < len(base_pal_data):
                            base_pal_colors.append((base_pal_data[i], base_pal_data[i+1], base_pal_data[i+2]))
            
            if not base_pal_colors:
                return
            
            # Check if the base palette is mostly keying colors (invalid reference palette)
            non_keying_count = 0
            for color in base_pal_colors:
                if (color != (255, 0, 255) and color != (0, 255, 0) and 
                    not self.is_universal_keying_color(color)):
                    non_keying_count += 1
            
            
            # Create base palette to current_colors mapping using multi-pass matching
            base_to_custom_mapping = self.icon_handler._create_base_to_custom_mapping(
                base_pal_colors, self.current_colors, self.char_id, self.fashion_type
            )
            
            # Create BMP index to custom_palette index mapping
            # Match BMP colors to base palette colors, then use mapped custom colors

            bmp_to_custom_map = {}
            
            for bmp_idx, bmp_color in enumerate(bmp_palette):
                if (bmp_color == (255, 0, 255) or 
                    bmp_color == (0, 255, 0) or 
                    self.is_universal_keying_color(bmp_color)):
                    bmp_to_custom_map[bmp_idx] = (255, 0, 255)  # Map to magenta
                    continue
                
                # Find matching color in base palette
                base_pal_idx = None
                for base_idx, base_color in enumerate(base_pal_colors):
                    if base_color == bmp_color:
                        base_pal_idx = base_idx
                        break
                
                if base_pal_idx is not None:
                    # Use the mapped custom color if available
                    if base_pal_idx in base_to_custom_mapping:
                        custom_color = base_to_custom_mapping[base_pal_idx]
                        # Only use the custom color if it's not a keying color
                        if (custom_color != (255, 0, 255) and
                            not self.is_universal_keying_color(custom_color)):
                            bmp_to_custom_map[bmp_idx] = custom_color
                        else:
                            # Custom color is keying, but BMP color is valid - use BMP color
                            bmp_to_custom_map[bmp_idx] = bmp_color
                    else:
                        # No mapping found - use BMP color
                        bmp_to_custom_map[bmp_idx] = bmp_color
                else:
                    # If not found in base palette, use the BMP's original color
                    # (don't default to magenta - that would key out valid pixels)
                    bmp_to_custom_map[bmp_idx] = bmp_color
            
            # Create new RGB image with palette-translated colors
            new_img = Image.new("RGB", img.size)
            
            transparent_count = 0
            opaque_count = 0
            
            # Create color mapping for colorpicker (map BMP RGBA pixels to palette indices)
            self.color_mapping = {}
            
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if alpha.getpixel((x, y)) > 0:  # Not transparent
                        # Get the BMP palette index for this pixel
                        pixel_idx = y * img.size[0] + x
                        if pixel_idx < len(bmp_pixels):
                            bmp_idx = bmp_pixels[pixel_idx]
                            
                            # Get the mapped color
                            final_color = bmp_to_custom_map.get(bmp_idx, (255, 0, 255))
                            new_img.putpixel((x, y), final_color)
                            
                            # Store mapping for colorpicker (BMP pixel -> custom_palette index)
                            bmp_pixel = img.getpixel((x, y))
                            if bmp_pixel not in self.color_mapping and bmp_idx in bmp_to_custom_map:
                                # Find which index in current_colors this color is
                                for idx, color in enumerate(self.current_colors):
                                    if color == final_color:
                                        self.color_mapping[bmp_pixel] = idx
                                        break
                            
                            opaque_count += 1
                    else:
                        # Use keying color for transparent areas
                        new_img.putpixel((x, y), self.keying_color)
                        transparent_count += 1
            
            # Save the base preview image (before resizing) for click detection
            self.preview_base_img = new_img
            
            # Resize for preview using current zoom level
            max_allowed_width = 230
            max_allowed_height = 230
            
            max_zoom_x = max_allowed_width / new_img.size[0] if new_img.size[0] > 0 else self.zoom_level
            max_zoom_y = max_allowed_height / new_img.size[1] if new_img.size[1] > 0 else self.zoom_level
            max_allowed_zoom = min(max_zoom_x, max_zoom_y, self.zoom_level)
            
            effective_zoom = min(self.zoom_level, max_allowed_zoom)
            
            preview_size = (int(new_img.size[0] * effective_zoom), int(new_img.size[1] * effective_zoom))
            preview_img = new_img.resize(preview_size, Image.NEAREST)
            
            # Convert to PhotoImage for tkinter
            self.preview_photo = ImageTk.PhotoImage(preview_img)
            if self.preview_label is not None:
                self.preview_label.configure(image=self.preview_photo)
            
        except Exception as e:
            pass
    
    
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
            # Use the preview base image (already has correct palette applied)
            if not hasattr(self, 'preview_base_img') or self.preview_base_img is None:
                return
            
            # Get the click coordinates relative to the preview label
            click_x = event.x
            click_y = event.y
            
            # The preview is scaled up by effective zoom, so we need to scale down the coordinates
            # Calculate the same effective zoom as in _update_preview
            max_allowed_width = 230  # Same as in _update_preview
            max_allowed_height = 230  # Same as in _update_preview
            
            max_zoom_x = max_allowed_width / self.preview_base_img.size[0] if self.preview_base_img.size[0] > 0 else self.zoom_level
            max_zoom_y = max_allowed_height / self.preview_base_img.size[1] if self.preview_base_img.size[1] > 0 else self.zoom_level
            max_allowed_zoom = min(max_zoom_x, max_zoom_y, self.zoom_level)
            
            effective_zoom = min(self.zoom_level, max_allowed_zoom)
            
            original_x = int(click_x / effective_zoom)
            original_y = int(click_y / effective_zoom)
            
            # Check if the click is within the image bounds
            if 0 <= original_x < self.preview_base_img.size[0] and 0 <= original_y < self.preview_base_img.size[1]:
                # Get the original BMP pixel to use for mapping
                original_img = Image.open(self.image_path)
                if original_img.mode != 'P':
                    original_img = original_img.convert('P')
                
                # Get the palette index at this position
                pixel_idx = original_img.getpixel((original_x, original_y))
                palette_data = original_img.getpalette()
                
                # Check if the pixel is transparent (keying color)
                if palette_data and pixel_idx < len(palette_data)//3:
                    r = palette_data[pixel_idx*3]
                    g = palette_data[pixel_idx*3+1] 
                    b = palette_data[pixel_idx*3+2]
                    pixel_color = (r, g, b)
                    is_transparent = (pixel_color == self.keying_color)
                    pixel = (r, g, b, 255 if not is_transparent else 0)  # Create RGBA-like tuple
                else:
                    is_transparent = True
                    pixel = (0, 0, 0, 0)
                
                if is_transparent:
                    # Clicked on transparent area - pick the keying/background color
                    picked_color = self.keying_color
                else:
                    # Get the actual color being displayed (after color mapping)
                    if pixel in self.color_mapping:
                        # Get the mapped color from current_colors
                        color_index = self.color_mapping[pixel]
                        
                        # If inverse order is enabled, translate the index
                        if self.inverse_order_var.get():
                            color_index = len(self.current_colors) - 1 - color_index
                        
                        if 0 <= color_index < len(self.current_colors):
                            picked_color = self.current_colors[color_index]
                        else:
                            picked_color = (0, 0, 0)
                    else:
                        # Fallback to black if mapping not found
                        picked_color = (0, 0, 0)
                
                # Check if picked color is a keying color and find alternative if needed
                if self._is_keyed_color(picked_color):
                    picked_color = self._find_nearest_non_keyed_color(picked_color)
                
                # Apply the picked color to selected palette indices
                self._apply_colorpicked_color(picked_color)
                
        except Exception as e:
            pass
    
    def _colorpick_from_palette(self, index):
        """Pick color from palette square."""
        if 0 <= index < len(self.current_colors):
            picked_color = self.current_colors[index]
            
            # Check if picked color is a keying color and find alternative if needed
            if self._is_keyed_color(picked_color):
                picked_color = self._find_nearest_non_keyed_color(picked_color)
            
            self._apply_colorpicked_color(picked_color)
    
    def _colorpick_from_saved(self, slot_index):
        """Pick color from saved color slot."""
        if 0 <= slot_index < len(self.saved_colors):
            picked_color = self.saved_colors[slot_index]
            if picked_color != (0, 0, 0):  # Only pick non-empty slots
                # Check if picked color is a keying color and find alternative if needed
                if self._is_keyed_color(picked_color):
                    picked_color = self._find_nearest_non_keyed_color(picked_color)
                
                self._apply_colorpicked_color(picked_color)
    
    def _apply_colorpicked_color(self, picked_color):
        """Apply a picked color to the selected palette indices."""
        # Double-check that picked color is not a keying color before applying
        if self._is_keyed_color(picked_color):
            picked_color = self._find_nearest_non_keyed_color(picked_color)
        
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
            if hasattr(self, 'original_to_display_index') and idx in self.original_to_display_index:
                display_idx = self.original_to_display_index[idx]
                if display_idx < len(self.palette_squares):
                    square = self.palette_squares[display_idx]
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
            # Route based on saved_mode
            if self.saved_mode == "L":
                # L mode: Left-click saves, Right-click applies
                if button == "left":
                    self._save_to_slot(slot_index)
                elif button == "right":
                    self._load_from_slot(slot_index)
            else:  # R mode
                # R mode: Right-click saves, Left-click applies
                if button == "right":
                    self._save_to_slot(slot_index)
                elif button == "left":
                    self._load_from_slot(slot_index)
    
    def _on_preview_click(self, event):
        """Handle click on preview image to select corresponding color index or pick color."""
        if self.colorpicker_active:
            self._colorpick_from_preview(event)
            return
        
        # Original preview click behavior for color selection
        try:
            # Use the preview base image (already has correct palette applied)
            if not hasattr(self, 'preview_base_img') or self.preview_base_img is None:
                return
            
            # Get the click coordinates relative to the preview label
            click_x = event.x
            click_y = event.y
            
            # The preview is scaled up by effective zoom, so we need to scale down the coordinates
            # Calculate the same effective zoom as in _update_preview
            max_allowed_width = 230  # Same as in _update_preview (10px more stretch)
            max_allowed_height = 230  # Same as in _update_preview
            
            max_zoom_x = max_allowed_width / self.preview_base_img.size[0] if self.preview_base_img.size[0] > 0 else self.zoom_level
            max_zoom_y = max_allowed_height / self.preview_base_img.size[1] if self.preview_base_img.size[1] > 0 else self.zoom_level
            max_allowed_zoom = min(max_zoom_x, max_zoom_y, self.zoom_level)
            
            effective_zoom = min(self.zoom_level, max_allowed_zoom)
            
            original_x = int(click_x / effective_zoom)
            original_y = int(click_y / effective_zoom)
            
            # Check if the click is within the image bounds
            if 0 <= original_x < self.preview_base_img.size[0] and 0 <= original_y < self.preview_base_img.size[1]:
                # Get the original BMP pixel to use for mapping
                original_img = Image.open(self.image_path)
                if original_img.mode != 'P':
                    original_img = original_img.convert('P')
                
                # Get the palette index and color
                pixel_idx = original_img.getpixel((original_x, original_y))
                palette_data = original_img.getpalette()
                
                # Check if the pixel is transparent (keying color)
                if palette_data and pixel_idx < len(palette_data)//3:
                    r = palette_data[pixel_idx*3]
                    g = palette_data[pixel_idx*3+1] 
                    b = palette_data[pixel_idx*3+2]
                    pixel_color = (r, g, b)
                    is_transparent = (pixel_color == self.keying_color)
                    pixel = (r, g, b, 255 if not is_transparent else 0)  # Create RGBA-like tuple for mapping
                else:
                    is_transparent = True
                    pixel = (0, 0, 0, 0)
                
                if not is_transparent:
                    # Look up the color index from our mapping (maps RGBA-like pixel to display index)
                    if pixel in self.color_mapping:
                        color_index = self.color_mapping[pixel]
                        
                        # If inverse order is enabled, translate the index
                        if self.inverse_order_var.get():
                            color_index = len(self.current_colors) - 1 - color_index
                        
                        # Convert display index to original index for selection
                        if hasattr(self, 'display_to_original_index'):
                            original_idx = self.display_to_original_index.get(color_index, color_index)
                        else:
                            original_idx = color_index
                        
                        # Select the corresponding color in the palette
                        if 0 <= original_idx < len(self.current_colors):
                            self._select_color(original_idx, "left", 0)
                
        except Exception as e:
            pass
    
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
            pass
    
    def _reset_colors(self):
        """Reset colors to original extracted colors."""
        current_palette_key = f"{self.char_id}_{self.fashion_type}"
        
        # Reset to original colors (full palette list)
        if hasattr(self, '_original_palettes') and current_palette_key in self._original_palettes:
            self.current_colors = self._original_palettes[current_palette_key].copy()
        else:
            # Fallback: rebuild from custom_palette and editable_colors (same as initialization)
            self.current_colors = self.custom_palette.copy()  # Start with full palette
            # Update only the editable positions with extracted colors
            for idx, color in self.editable_colors.items():
                if idx < len(self.current_colors):
                    self.current_colors[idx] = color
        
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
                
                # Filter out ALL keying colors:
                # - Magenta (255, 0, 255)
                # - Universal keying colors (green variants)
                # - Character-specific keying colors based on character rules
                valid_colors = []
                for idx, color in enumerate(saved_colors):
                    # Skip magenta explicitly
                    if color == (255, 0, 255):
                        continue
                    # Skip universal green keying colors
                    if color == (0, 255, 0):
                        continue
                    # Skip any color that matches character-specific keying rules
                    if self._is_keyed_color(color, idx):
                        continue
                    # This is a valid, non-keyed color
                    valid_colors.append(color)
                
                # Identify excess colors (colors beyond what we need for the icon palette)
                # These excess colors are already filtered to exclude all keying colors
                if len(valid_colors) > expected_count:
                    excess_colors = valid_colors[expected_count:]
                    # Offer to save excess colors to JSON (they're already filtered)
                    if excess_colors:
                        self._prompt_save_loaded_excess_colors(excess_colors, file_path)
                
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
        tk.Label(main_frame, text="Adjust all colors to match:", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        
        # HSL adjustment checkboxes
        checkbox_frame = tk.Frame(main_frame)
        checkbox_frame.pack(pady=(0, 10))
        
        # Hue checkbox
        hue_var = tk.BooleanVar(value=self._gradient_adjust_hue)
        hue_cb = tk.Checkbutton(checkbox_frame, text="Hue", variable=hue_var,
                               command=lambda: self._update_gradient_settings('hue', hue_var.get()))
        hue_cb.pack(side="left", padx=5)
        
        # Saturation checkbox
        sat_var = tk.BooleanVar(value=self._gradient_adjust_saturation)
        sat_cb = tk.Checkbutton(checkbox_frame, text="Saturation", variable=sat_var,
                               command=lambda: self._update_gradient_settings('saturation', sat_var.get()))
        sat_cb.pack(side="left", padx=5)
        
        # Value checkbox
        value_var = tk.BooleanVar(value=self._gradient_adjust_value)
        value_cb = tk.Checkbutton(checkbox_frame, text="Value", variable=value_var,
                               command=lambda: self._update_gradient_settings('value', value_var.get()))
        value_cb.pack(side="left", padx=5)
        
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
    
    def _update_gradient_settings(self, setting, value):
        """Update the HSL adjustment settings."""
        if setting == 'hue':
            self._gradient_adjust_hue = value
        elif setting == 'saturation':
            self._gradient_adjust_saturation = value
        elif setting == 'value':
            self._gradient_adjust_value = value

    def _apply_gradient_hue(self, target_hue, color_name, variant=None):
        """Apply hue adjustment to colors in the current icon palette."""
        import colorsys
        
        # Determine which indices to modify based on multiselect state
        if self.multi_select_var.get() and self.selected_indices:
            indices_to_modify = self.selected_indices
        else:
            indices_to_modify = range(len(self.current_colors))
        
        # Special handling for neutral colors and variants
        if target_hue is None or variant in ["grey", "light_grey", "dark_grey", "black", "white"]:
            if variant == "light_grey" or color_name == "Light Grey":
                # Convert to light greyscale
                for i in indices_to_modify:
                    if i < len(self.current_colors):  # Ensure index is valid
                        r, g, b = self.current_colors[i]
                        grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                        # Make it lighter
                        light_grey = min(255, int(grey * 1.5))
                        self.current_colors[i] = (light_grey, light_grey, light_grey)
            elif variant == "dark_grey" or color_name == "Dark Grey":
                # Convert to dark greyscale
                for i in indices_to_modify:
                    if i < len(self.current_colors):  # Ensure index is valid
                        r, g, b = self.current_colors[i]
                        grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                        # Make it darker
                        dark_grey = int(grey * 0.5)
                        self.current_colors[i] = (dark_grey, dark_grey, dark_grey)
            elif variant == "grey" or color_name == "Grey":
                # Convert all colors to greyscale
                for i in indices_to_modify:
                    if i < len(self.current_colors):  # Ensure index is valid
                        r, g, b = self.current_colors[i]
                        grey = int(0.299 * r + 0.587 * g + 0.114 * b)
                        self.current_colors[i] = (grey, grey, grey)
            elif variant == "black" or color_name == "Black":
                # Make all colors darker (reduce value significantly)
                for i in indices_to_modify:
                    if i < len(self.current_colors):  # Ensure index is valid
                        r, g, b = self.current_colors[i]
                        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                        v = v * 0.2  # Reduce brightness to 20%
                        rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
                        self.current_colors[i] = (int(rr*255), int(gg*255), int(bb*255))
            elif variant == "white" or color_name == "White":
                # Make all colors lighter (increase value significantly)
                for i in indices_to_modify:
                    if i < len(self.current_colors):  # Ensure index is valid
                        r, g, b = self.current_colors[i]
                        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                        v = min(1.0, v + (1.0 - v) * 0.8)  # Increase brightness towards white
                        rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
                        self.current_colors[i] = (int(rr*255), int(gg*255), int(bb*255))
        else:
            # Apply hue adjustment with optional value variants
            for i in indices_to_modify:
                if i >= len(self.current_colors):  # Skip invalid indices
                    continue
                r, g, b = self.current_colors[i]
                h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                
                # Store original HSV values
                orig_h, orig_s, orig_v = h, s, v
                
                # Only adjust hue if enabled and color has some saturation
                if self._gradient_adjust_hue and s > 0.1:  # Threshold to avoid adjusting near-grey colors
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
                
                # Adjust saturation if enabled
                if self._gradient_adjust_saturation:
                    s = orig_s  # Use original saturation as target
                    
                # Adjust value if enabled
                if self._gradient_adjust_value:
                    v = orig_v  # Use original value as target
                
                # Apply value variants
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
        """Reset colors to original extracted colors before gradient changes and reset HSL settings."""
        # Reset HSL settings to defaults
        self._gradient_adjust_hue = True
        self._gradient_adjust_saturation = False
        self._gradient_adjust_value = False
        
        current_palette_key = f"{self.char_id}_{self.fashion_type}"
        
        # Reset to original colors (full palette list)
        if hasattr(self, '_original_palettes') and current_palette_key in self._original_palettes:
            self.current_colors = self._original_palettes[current_palette_key].copy()
        else:
            # Fallback: rebuild from custom_palette and editable_colors (same as initialization)
            self.current_colors = self.custom_palette.copy()  # Start with full palette
            # Update only the editable positions with extracted colors
            for idx, color in self.editable_colors.items():
                if idx < len(self.current_colors):
                    self.current_colors[idx] = color
        
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
        
        # Use the same comprehensive keying logic as the IconHandler
        # Universal keying colors
        if self.is_universal_keying_color(color):
            return True
        
        # Magenta (chroma key)
        if color == (255, 0, 255):
            return True
        
        # Character-specific keying rules
        char_num = self.char_id[3:] if self.char_id.startswith('chr') else self.char_id
        
        # chr004 specific rules
        if char_num == "004":
            # Black is now treated as a valid color for icon editor
            # Only filter out the last palette index
            if index == 255:  # Last color in palette
                return True
        
        # chr003 (Sheep) - uses universal keying colors
        elif char_num == "003":
            return self.is_chr003_keying_color(color)
        
        # chr008 (Raccoon) - uses universal keying colors  
        elif char_num == "008":
            return self.is_chr008_keying_color(color)
        
        # chr011 (Sheep 2nd Job) - uses same as chr003
        elif char_num == "011":
            return self.is_chr011_keying_color(color)
        
        # chr014 (Lion 2nd Job) - uses selective keying
        elif char_num == "014":
            return self.is_chr014_keying_color(color)
        
        return False

    def is_universal_keying_color(self, color):
        """Check if a color is a universal keying color for ALL characters"""
        r, g, b = color
        
        # Pure green (0, 255, 0) - used by ALL characters including chr010
        if color == (0, 255, 0):
            return True
        
        # (0~25, 255, 0) pattern - used by chr002, chr008, chr024, and others
        if g == 255 and b == 0 and 0 <= r <= 25:
            return True
        
        # (0, 255, 0~21) pattern - used by chr003, chr011, chr019, and others
        if g == 255 and r == 0 and 0 <= b <= 21:
            return True
        
        return False

    def is_chr003_keying_color(self, color):
        """Check if a color is a keying color for chr003 (Sheep)"""
        # chr003 uses universal keying colors
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr008_keying_color(self, color):
        """Check if a color is a keying color for chr008 (Raccoon)"""
        # chr008 uses universal keying colors
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr011_keying_color(self, color):
        """Check if a color is a keying color for chr011 (Sheep 2nd Job)"""
        # chr011 uses the same keying patterns as chr003
        return self.is_universal_keying_color(color) or color == (255, 0, 255)  # Magenta

    def is_chr014_keying_color(self, color):
        """Check if a color is a keying color for chr014 (Lion 2nd Job)"""
        # chr014 uses more selective keying to avoid over-transparency
        # Only key out pure green and magenta, not green variants
        if color == (0, 255, 0) or color == (255, 0, 255):  # Pure green and magenta
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
    
    def _quick_export(self, export_type):
        """Quick export either icon or portrait using current settings."""
        try:
            if export_type == "icon":
                # Use current settings to export icon
                success = self.icon_handler.save_as_icon(
                    self.char_id,
                    self.fashion_type,
                    self.current_colors,
                    self.palette_path
                )
                if success:
                    messagebox.showinfo("Success", "Icon exported successfully!")
                else:
                    messagebox.showerror("Error", "Failed to export icon.")
            else:  # portrait
                # Get the live editor window
                if (self.live_editor_window and self.live_editor_window.winfo_exists() and 
                    not getattr(self.live_editor_window, 'advanced_mode', False)):
                    # Get the current frame from the live editor's preview
                    frame = self.live_editor_window.get_current_displayed_frame()
                    if frame is not None:
                        # Export the frame as portrait
                        self.live_editor_window.export_background_bmp(frame, force_portrait=True)
                    else:
                        messagebox.showerror("Error", "No frame available in live preview.")
                else:
                    # Fall back to main UI preview if live preview is not available or in advanced mode
                    if self.icon_handler and self.icon_handler.main_window:
                        frame = self.icon_handler.main_window.get_current_displayed_frame()
                        if frame is not None:
                            self.icon_handler.main_window.export_background_bmp(frame, force_portrait=True)
                        else:
                            messagebox.showerror("Error", "No frame available in main preview.")
                    else:
                        messagebox.showerror("Error", "No preview window available.")
            
            # Bring the icon editor window back to front
            self._bring_to_front()
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
            self._bring_to_front()

    def _export_icon(self):
        """Export the edited icon."""
        try:
            # Get exports directory path
            export_dir = os.path.join(self.icon_handler.root_dir, "exports", "icons")
            
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
                self.keying_color, self.image_path, export_path
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

