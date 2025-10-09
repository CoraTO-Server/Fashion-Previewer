#!/usr/bin/env python3
print("Loading script...")
"""
make_palettes_v2.py - Intelligent Palette Generator

Recursively processes BMP directories to create optimized palette files that:
1. Place background/key color at index 0
2. Group similar colors together
3. Align indices with fashion_base.pal reference
4. Fill unused indices with background color

The script:
- Renames existing .pal files to *_base.pal before analysis
- Creates new .pal files matching BMP names
- Uses VGA 24-bit format for output
- Intelligently places colors near similar colors from fashion_base.pal
"""

import os
import sys
from PIL import Image
import numpy as np
from collections import defaultdict
import shutil

def rgb_to_bytes(rgb_array):
    """Convert RGB array to bytes for .pal file."""
    return bytes([int(x) for x in rgb_array.flatten()])

def get_background_color(img, palette):
    """
    Detect background color:
    - If a color occupies >=30% of pixels OR
    - Is close to magenta (255,0,255) or black (0,0,0)
    - Otherwise use most frequent color
    """
    # Count color frequencies
    width, height = img.size
    pixel_count = width * height
    color_freq = {}
    
    # Convert palette to list of RGB tuples
    pal_colors = []
    for i in range(0, len(palette), 3):
        pal_colors.append((palette[i], palette[i+1], palette[i+2]))
    
    # Count pixels
    for y in range(height):
        for x in range(width):
            idx = img.getpixel((x, y))
            color_freq[idx] = color_freq.get(idx, 0) + 1
    
    for idx, count in color_freq.items():
        rgb = pal_colors[idx]
        
        # Check if color is dominant (>=30%)
        if count / pixel_count >= 0.3:
            return idx, rgb
            
        # Check if color is close to magenta or black
        r, g, b = rgb
        is_magenta = (abs(r - 255) <= 10 and 
                     abs(g - 0) <= 10 and 
                     abs(b - 255) <= 10)
        is_black = r <= 10 and g <= 10 and b <= 10
        
        if is_magenta or is_black:
            return idx, rgb
    
    # Fallback to most frequent color
    most_freq_idx = max(color_freq.items(), key=lambda x: x[1])[0]
    return most_freq_idx, pal_colors[most_freq_idx]

def color_distance(c1, c2):
    """Calculate Euclidean distance between colors."""
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    dr = r1 - r2
    dg = g1 - g2
    db = b1 - b2
    return (dr * dr + dg * dg + db * db) ** 0.5

def find_nearest_color_index(target_color, palette, exclude_indices=None):
    """Find index of nearest color in palette, optionally excluding certain indices."""
    if exclude_indices is None:
        exclude_indices = set()
    
    # Convert palette to list of RGB tuples
    pal_colors = []
    for i in range(0, len(palette), 3):
        pal_colors.append((palette[i], palette[i+1], palette[i+2]))
    
    best_distance = float('inf')
    best_index = None
    
    for i, color in enumerate(pal_colors):
        if i in exclude_indices:
            continue
        distance = color_distance(target_color, color)
        if distance < best_distance:
            best_distance = distance
            best_index = i
    
    return best_index if best_index is not None else 0

def group_similar_colors(colors):
    """Group colors by similarity using a simple clustering approach."""
    groups = []
    remaining = colors[:]  # Make a copy
    
    while remaining:
        current = remaining.pop(0)
        group = [current]
        
        i = 0
        while i < len(remaining):
            if color_distance(current, remaining[i]) < 100:  # Threshold
                group.append(remaining.pop(i))
            else:
                i += 1
                
        groups.append(group)
    
    return groups

def is_neon_green(color, threshold=10):
    """Check if a color is neon green (approximately 0,255,0)."""
    r, g, b = color
    return (abs(r - 0) <= threshold and 
            abs(g - 255) <= threshold and 
            abs(b - 0) <= threshold)

def is_pure_magenta(color, threshold=5):
    """Check if a color is pure magenta (255,0,255)."""
    r, g, b = color
    return (abs(r - 255) <= threshold and 
            abs(g - 0) <= threshold and 
            abs(b - 255) <= threshold)

def process_bmp_file(bmp_path, fashion_base_path=None):
    """
    Process a single BMP file to create an optimized palette file.
    
    Args:
        bmp_path: Path to the BMP file
        fashion_base_path: Optional path to fashion_base.pal reference
    """
    try:
        # Load and process the BMP
        img = Image.open(bmp_path)
        if img.mode != 'P':
            print(f"Warning: {bmp_path} is not an 8-bit palette image")
            return
            
        # Get the original palette
        orig_palette = img.getpalette()
        if not orig_palette:
            print(f"Warning: {bmp_path} has no palette")
            return
            
        # Convert original palette to RGB tuples
        orig_colors = []
        for i in range(0, len(orig_palette), 3):
            orig_colors.append((orig_palette[i], orig_palette[i+1], orig_palette[i+2]))
        
        # Step 1: Detect background color for index 0
        bg_idx, bg_color = get_background_color(img, orig_palette)
        
        # Step 2 & 3: Load and analyze _base.pal
        base_colors = {}  # index -> color mapping
        base_start_index = None
        
        if fashion_base_path and os.path.exists(fashion_base_path):
            with open(fashion_base_path, 'rb') as f:
                base_data = f.read()
                
            # Convert base palette to RGB tuples
            for i in range(0, len(base_data), 3):
                idx = i // 3
                color = (base_data[i], base_data[i+1], base_data[i+2])
                
                # Skip neon green, index 1 and 255
                if not is_neon_green(color) and idx != 1 and idx != 255:
                    if base_start_index is None:
                        base_start_index = idx
                        print(f"Base palette colors start at index {base_start_index}")
                    base_colors[idx] = color
            
            print(f"Found {len(base_colors)} valid colors in base palette")
        
        # Step 4: Analyze BMP palette and filter out pure magenta
        cached_palette = []
        for i, color in enumerate(orig_colors):
            if i != bg_idx and not is_pure_magenta(color):
                cached_palette.append(color)
        
        # Step 5: Create new palette with magenta
        magenta = (255, 0, 255)
        new_palette = [magenta] * 256
        new_palette[0] = bg_color
        used_indices = {0}
        
        # Step 6: Place BMP colors with progressive matching
        if base_start_index is not None and base_colors:
            # Get sorted list of available base indices
            available_indices = sorted([idx for idx in base_colors.keys() if idx not in used_indices])
            print(f"Available base indices: {available_indices}")
            
            remaining_colors = cached_palette[:]
            thresholds = [5, 15, 30, 50, 100, 200]
            
            for threshold in thresholds:
                if not remaining_colors or not available_indices:
                    break
                    
                print(f"\nTrying threshold {threshold}:")
                colors_to_remove = []
                
                for color in remaining_colors:
                    best_match_idx = None
                    best_distance = float('inf')
                    
                    for base_idx in available_indices:
                        base_color = base_colors[base_idx]
                        distance = color_distance(color, base_color)
                        
                        if distance < threshold and distance < best_distance:
                            best_distance = distance
                            best_match_idx = base_idx
                    
                    if best_match_idx is not None:
                        new_palette[best_match_idx] = color
                        used_indices.add(best_match_idx)
                        available_indices.remove(best_match_idx)
                        colors_to_remove.append(color)
                        print(f"  Color {color} -> Index {best_match_idx} (distance: {best_distance:.2f})")
                
                for color in colors_to_remove:
                    remaining_colors.remove(color)
            
            if remaining_colors:
                print(f"\nUnplaced colors: {len(remaining_colors)}")
        
        # Step 7: Convert palette to bytes
        palette_bytes = []
        for color in new_palette:
            palette_bytes.extend(color)
        
        # Step 8: Output the .pal file
        pal_path = os.path.splitext(bmp_path)[0] + '.pal'
        with open(pal_path, 'wb') as f:
            f.write(bytes(palette_bytes))
            
        print(f"Created palette: {pal_path}")
        
    except Exception as e:
        print(f"Error processing {bmp_path}: {e}")
        import traceback
        traceback.print_exc()

def find_base_palette(root, bmp_name):
    """Find matching base palette for a BMP file."""
    # Convert "something.bmp" to "something_base.pal"
    base_name = os.path.splitext(bmp_name)[0] + '_base.pal'
    
    # First check current directory
    base_path = os.path.join(root, base_name)
    if os.path.exists(base_path):
        print(f"Found base palette: {base_path}")
        return base_path
        
    # Check parent directory
    parent_dir = os.path.dirname(root)
    if os.path.exists(parent_dir):
        parent_base_path = os.path.join(parent_dir, base_name)
        if os.path.exists(parent_base_path):
            print(f"Found base palette in parent: {parent_base_path}")
            return parent_base_path
    
    print(f"No base palette found for {bmp_name}")
    return None

def process_directory(directory):
    """
    Recursively process all BMP directories.
    """
    try:
        print(f"Starting to process directory: {directory}")
        for root, dirs, files in os.walk(directory):
            try:
                # Only process directories ending with BMP
                if not root.upper().endswith('BMP'):
                    continue
                
                print(f"\nProcessing directory: {root}")
                print(f"Files found: {files}")
                
                # Process each BMP file with its matching base palette
                for file in files:
                    try:
                        if file.lower().endswith('.bmp'):
                            print(f"\nProcessing BMP file: {file}")
                            bmp_path = os.path.join(root, file)
                            print(f"Full BMP path: {bmp_path}")
                            base_pal = find_base_palette(root, file)
                            print(f"Found base palette: {base_pal}")
                            if base_pal:
                                process_bmp_file(bmp_path, base_pal)
                            else:
                                print(f"Skipping {file} - no matching base palette")
                    except Exception as e:
                        print(f"Error processing file {file}: {str(e)}")
                        import traceback
                        traceback.print_exc()
            except Exception as e:
                print(f"Error processing directory {root}: {str(e)}")
                import traceback
                traceback.print_exc()
    except Exception as e:
        print(f"Error in process_directory: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]
    else:
        start_dir = os.getcwd()
        
    if not os.path.isdir(start_dir):
        print(f"Error: {start_dir} is not a directory")
        sys.exit(1)
        
    print(f"Starting palette generation from: {start_dir}")
    process_directory(start_dir)
    
if __name__ == '__main__':
    print("Script starting...")
    try:
        main()
    except Exception as e:
        print(f"Fatal error, as Claude is retarded: {str(e)}")
        import traceback
        traceback.print_exc()
