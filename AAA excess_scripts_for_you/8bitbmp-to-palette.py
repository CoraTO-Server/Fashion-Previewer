#!/usr/bin/env python3
from __future__ import annotations
import struct
from pathlib import Path
from typing import List, Tuple, Iterable
from colorsys import rgb_to_hsv
import argparse
import sys
from PIL import Image

Color = Tuple[int, int, int]
MAGENTA: Color = (255, 0, 255)
BLACK: Color = (0, 0, 0)

# -------------------- RIFF PAL I/O --------------------

def read_riff_pal(path: Path) -> List[Color]:
    data = path.read_bytes()
    if data[:4] != b"RIFF":
        raise ValueError(f"{path} is not a RIFF file")
    if data[8:12] != b"PAL ":
        raise ValueError(f"{path} does not contain 'PAL ' chunk")
    idx = data.find(b"data", 12)
    if idx == -1:
        raise ValueError(f"{path} has no 'data' chunk")
    size = struct.unpack_from("<I", data, idx + 4)[0]
    payload = data[idx + 8 : idx + 8 + size]
    palVersion, palNumEntries = struct.unpack_from("<HH", payload, 0)
    entries: List[Color] = []
    off = 4
    for i in range(palNumEntries):
        r, g, b, _ = struct.unpack_from("4B", payload, off + i*4)
        entries.append((r, g, b))
    return entries

def write_riff_pal(entries: List[Color], out_path: Path, palVersion: int = 0x0300) -> None:
    palNumEntries = len(entries)
    payload = bytearray(struct.pack("<HH", palVersion, palNumEntries))
    for (r,g,b) in entries:
        payload += struct.pack("4B", r, g, b, 0)
    riff_size = 4 + (4 + 4) + len(payload)  # 'PAL ' + 'data' + size + payload
    out = bytearray()
    out += b"RIFF"
    out += struct.pack("<I", riff_size)
    out += b"PAL "
    out += b"data"
    out += struct.pack("<I", len(payload))
    out += payload
    out_path.write_bytes(bytes(out))

# -------------------- Sorting --------------------

def perceived_luminance(c: Color) -> float:
    r,g,b = c
    return 0.2126*r + 0.7152*g + 0.0722*b

def sort_darkest_last(colors: List[Color]) -> List[Color]:
    def key(c: Color):
        r,g,b = [x/255.0 for x in c]
        h,s,v = rgb_to_hsv(r,g,b)
        lum = perceived_luminance(c)
        return (-lum, -s)  # brightest first, darkest last; saturated first on ties
    return sorted(colors, key=key)

# -------------------- Image-based pad detection --------------------

IMG_EXTS = {".png", ".bmp", ".gif", ".jpg", ".jpeg", ".tif", ".tiff"}

def find_matching_images_for_palette(pal_path: Path) -> List[Path]:
    """Prefer images in the same folder whose stem starts with the palette stem
    (e.g., hero.pal -> hero.png, hero_idle_0.png)."""
    base = pal_path.stem.lower()
    results: List[Path] = []
    for p in pal_path.parent.iterdir():
        if p.is_file() and p.suffix.lower() in IMG_EXTS and p.stem.lower().startswith(base):
            results.append(p)
    return results

def count_special_pixels(img_path: Path) -> Tuple[int, int]:
    """Return (#magenta_pixels, #black_pixels) using exact matches."""
    try:
        im = Image.open(img_path).convert("RGBA")
    except Exception:
        return (0, 0)
    pix = im.getdata()
    mag = 0
    blk = 0
    for r,g,b,a in pix:
        if a == 0:
            # treat fully transparent as background-neutral; ignore
            continue
        if r == 255 and g == 0 and b == 255:
            mag += 1
        elif r == 0 and g == 0 and b == 0:
            blk += 1
    return (mag, blk)

def decide_pad_color_for_palette(pal_entries: List[Color], pal_path: Path, detect_from: List[Path]) -> Color:
    """Decide between MAGENTA and BLACK. Priority:
       1) Images alongside the .pal with matching stem.
       2) If none, fall back to provided --detect-from images.
       3) If still none, heuristics based on palette content.
    """
    local_imgs = find_matching_images_for_palette(pal_path)
    img_list: List[Path] = local_imgs if local_imgs else detect_from

    mag_count = 0
    blk_count = 0
    for img in img_list:
        m,b = count_special_pixels(img)
        mag_count += m
        blk_count += b

    has_mag = MAGENTA in pal_entries
    has_blk = BLACK in pal_entries

    if mag_count > blk_count and has_mag:
        return MAGENTA
    if blk_count > mag_count and has_blk:
        return BLACK

    # Tie or no images: prefer MAGENTA if present; else BLACK if present; else MAGENTA fallback
    if has_mag:
        return MAGENTA
    if has_blk:
        return BLACK
    return MAGENTA

# -------------------- Magenta/Black padding rule --------------------

def apply_padding_rule(entries: List[Color], pad_color: Color) -> List[Color]:
    """Place exactly one pad_color at the start, rest of that color at the end."""
    pads = [c for c in entries if c == pad_color]
    non_pads = [c for c in entries if c != pad_color]
    sorted_non = sort_darkest_last(non_pads)

    out: List[Color] = []
    if pads:
        out.append(pad_color)   # one at beginning
        pads = pads[1:]
    out.extend(sorted_non)
    out.extend(pads)            # remaining at end
    return out

# -------------------- CLI --------------------

def main():
    ap = argparse.ArgumentParser(description="Recursively reorder .pal files with auto padding (magenta/black) decided from image composition.")
    ap.add_argument("root", nargs="?", default=".", help="Root folder to scan recursively (default: current)")
    ap.add_argument("--outdir", type=str, default="", help="Optional output folder; if omitted, overwrites in place.")
    ap.add_argument("--detect-from", nargs="*", default=[], help="Optional list of image files or folders to sample for background detection.")
    args = ap.parse_args()

    root = Path(args.root)
    outdir = Path(args.outdir) if args.outdir else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)

    # Expand detect-from into a flat list of image files
    detect_sources: List[Path] = []
    for item in args.detect_from:
        p = Path(item)
        if p.is_dir():
            detect_sources.extend([f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in IMG_EXTS])
        elif p.is_file() and p.suffix.lower() in IMG_EXTS:
            detect_sources.append(p)
    # Process palettes
    for pal_path in root.rglob("*.pal"):
        try:
            entries = read_riff_pal(pal_path)
            pad_color = decide_pad_color_for_palette(entries, pal_path, detect_sources)
            new_entries = apply_padding_rule(entries, pad_color)
            out_path = (outdir / pal_path.relative_to(root)) if outdir else pal_path
            if outdir:
                out_path.parent.mkdir(parents=True, exist_ok=True)
            write_riff_pal(new_entries, out_path)
            pc = "#FF00FF" if pad_color == MAGENTA else "#000000"
            print(f"✔ {pal_path} → {out_path} (pad={pc}, darkest last)")
        except Exception as e:
            print(f"✘ Error processing {pal_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
