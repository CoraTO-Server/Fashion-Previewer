#!/usr/bin/env python3
"""
Reorder RIFF .pal palettes with options for sorting and the "magenta padding" rule.

Default behavior:
  - Sort so the darkest colors are LAST (brightest -> darkest).
  - Keep exactly ONE magenta (#FF00FF) swatch at the beginning.
  - Put any remaining magentas at the end.

Other modes are available via --mode.
"""
from __future__ import annotations
import struct
from pathlib import Path
from typing import List, Tuple
from colorsys import rgb_to_hsv
import argparse
import sys

Color = Tuple[int, int, int]

# ---------- RIFF PAL I/O ----------

def read_riff_pal(path: Path) -> List[Color]:
    data = path.read_bytes()
    if data[:4] != b"RIFF":
        raise ValueError(f"{path} is not a RIFF file")
    # Find 'PAL ' fourcc
    if data[8:12] != b"PAL ":
        raise ValueError(f"{path} does not contain 'PAL ' chunk")
    # Find 'data' chunk start
    idx = data.find(b"data", 12)
    if idx == -1:
        raise ValueError(f"{path} has no 'data' chunk")
    size = struct.unpack_from("<I", data, idx + 4)[0]
    payload = data[idx + 8 : idx + 8 + size]
    if len(payload) < 4:
        raise ValueError(f"{path} has truncated LOGPALETTE")
    palVersion, palNumEntries = struct.unpack_from("<HH", payload, 0)
    entries: List[Color] = []
    off = 4
    for i in range(palNumEntries):
        r, g, b, _ = struct.unpack_from("4B", payload, off + i*4)
        entries.append((r, g, b))
    return entries

def write_riff_pal_simple(entries: List[Color], out_path: Path, palVersion: int = 0x0300) -> None:
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

# ---------- Sorting helpers ----------

def perceived_luminance(c: Color) -> float:
    r, g, b = c
    # ITU-R BT.709 coefficients
    return 0.2126*r + 0.7152*g + 0.0722*b

def sort_darkest_last(colors: List[Color]) -> List[Color]:
    # Brightest first, darkest last
    def key(c: Color):
        r,g,b = [x/255.0 for x in c]
        h,s,v = rgb_to_hsv(r,g,b)
        lum = perceived_luminance(c)
        return (-lum, -s)  # luminance descending, then more saturated first
    return sorted(colors, key=key)

def sort_lightest_last(colors: List[Color]) -> List[Color]:
    # Darkest first, lightest last
    def key(c: Color):
        r,g,b = [x/255.0 for x in c]
        h,s,v = rgb_to_hsv(r,g,b)
        lum = perceived_luminance(c)
        return (lum, -s)  # luminance ascending, then more saturated first
    return sorted(colors, key=key)

def sort_hue_dark_sat(colors: List[Color]) -> List[Color]:
    # Hue asc -> luminance asc (darker first) -> saturation desc
    def key(c: Color):
        r,g,b = [x/255.0 for x in c]
        h,s,v = rgb_to_hsv(r,g,b)  # h in [0,1)
        hue = round(h*360.0, 6)
        lum = perceived_luminance(c)
        return (hue, lum, -s)
    return sorted(colors, key=key)

# ---------- Magenta-padding rule ----------

def apply_magenta_rule(sorted_nonmag: List[Color], magentas: List[Color], pad_first: bool) -> List[Color]:
    out: List[Color] = []
    if pad_first and magentas:
        out.append((255,0,255))
        magentas = magentas[1:]
    out.extend(sorted_nonmag)
    out.extend(magentas)
    return out

def reorder_palette(entries: List[Color], mode: str, pad_color: Color = (255,0,255), pad_first: bool = True) -> List[Color]:
    magentas = [c for c in entries if c == pad_color]
    nonmag = [c for c in entries if c != pad_color]

    if mode == "darkest_last":
        sorted_non = sort_darkest_last(nonmag)
    elif mode == "lightest_last":
        sorted_non = sort_lightest_last(nonmag)
    elif mode == "hue_darkness_saturation":
        sorted_non = sort_hue_dark_sat(nonmag)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    return apply_magenta_rule(sorted_non, magentas, pad_first=pad_first)

# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(description="Reorder RIFF .pal palettes with magenta padding rule.")
    ap.add_argument("paths", nargs="+", help="One or more .pal files (globs allowed by your shell).")
    ap.add_argument("--mode", choices=["darkest_last", "lightest_last", "hue_darkness_saturation"],
                    default="darkest_last", help="Sorting mode (default: darkest_last)")
    ap.add_argument("--no-pad-first", action="store_true",
                    help="Do NOT place a magenta at the very start (all magentas go at the end).")
    ap.add_argument("--pad-color", default="FF00FF",
                    help="Hex RGB for padding color (default FF00FF).")
    ap.add_argument("--outdir", type=str, default="",
                    help="Optional output directory. If omitted, overwrites in place.")
    args = ap.parse_args()

    # Parse pad color
    pad_hex = args.pad_color.strip().lstrip("#")
    if len(pad_hex) != 6:
        print("pad-color must be 6 hex digits like FF00FF", file=sys.stderr)
        sys.exit(2)
    pad = tuple(int(pad_hex[i:i+2], 16) for i in (0,2,4))  # type: ignore

    outdir = Path(args.outdir) if args.outdir else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)

    # Process files
    for pstr in args.paths:
        p = Path(pstr)
        if not p.exists():
            print(f"Skipping {p}: not found", file=sys.stderr)
            continue
        try:
            entries = read_riff_pal(p)
            new_entries = reorder_palette(entries, mode=args.mode, pad_color=pad, pad_first=(not args.no_pad_first))
            # write
            out_path = (outdir / p.name) if outdir else p
            write_riff_pal_simple(new_entries, out_path)
            print(f"Wrote {out_path}")
        except Exception as e:
            print(f"Error processing {p}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
