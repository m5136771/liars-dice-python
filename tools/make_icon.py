#!/usr/bin/env python3
"""
Generate the Liar's Dice app icon as crisp pixel art, using only the Python
standard library (zlib for PNG encoding). No Pillow / external deps required.

The icon is composed on a small logical grid (64x64) and nearest-neighbor
upscaled to 1024x1024, which keeps the pixels sharp and on-brand with the
in-app pixel-art aesthetic.

Usage:
    python3 tools/make_icon.py

Outputs (1024x1024, opaque RGB — App Store compliant, no alpha):
    LiarsDice/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png   (primary)
    docs/icon-concepts/concept-bones.png
    docs/icon-concepts/concept-skull.png
    docs/icon-concepts/concept-gold.png
"""

import os
import zlib
import struct

N = 64           # logical grid size
SCALE = 16       # 64 * 16 = 1024

# ---- Palette (matches LiarsDice/Theme/Theme.swift) -------------------------
NAVY      = (0x14, 0x15, 0x1F)
NAVY_DK   = (0x0C, 0x0D, 0x14)
TEAL      = (0x2A, 0x6F, 0x5A)
TEAL_HI   = (0x37, 0x86, 0x6E)
GOLD      = (0xF2, 0xC1, 0x4E)
GOLD_DK   = (0xB8, 0x88, 0x2A)
BONE      = (0xF6, 0xF0, 0xE2)
BONE_HI   = (0xFF, 0xFC, 0xF2)
BONE_SH   = (0xCE, 0xC4, 0xB0)
PIP       = (0x23, 0x20, 0x1A)
PARCH     = (0xD6, 0xC4, 0x96)
PARCH_DK  = (0x8A, 0x73, 0x44)
INK       = (0x24, 0x1B, 0x12)


def new_canvas():
    return [[list(NAVY) for _ in range(N)] for _ in range(N)]


def put(c, x, y, color, a=1.0):
    xi, yi = int(x), int(y)
    if 0 <= xi < N and 0 <= yi < N:
        if a >= 1.0:
            c[yi][xi] = list(color)
        else:
            bg = c[yi][xi]
            c[yi][xi] = [int(bg[i] * (1 - a) + color[i] * a) for i in range(3)]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def background(c, center, edge):
    cx, cy = (N - 1) / 2, (N - 1) / 2
    maxd = (cx ** 2 + cy ** 2) ** 0.5
    for y in range(N):
        for x in range(N):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / maxd
            c[y][x] = list(lerp(center, edge, min(1.0, d ** 1.1)))


def disc(c, cx, cy, r, color, a=1.0):
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                put(c, x, y, color, a)


def round_rect(c, x0, y0, x1, y1, rad, color, a=1.0):
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1):
            inside = True
            # round the four corners
            for (cx, cy) in ((x0 + rad, y0 + rad), (x1 - rad, y0 + rad),
                             (x0 + rad, y1 - rad), (x1 - rad, y1 - rad)):
                if ((x < x0 + rad and y < y0 + rad and (cx, cy) == (x0 + rad, y0 + rad)) or
                    (x > x1 - rad and y < y0 + rad and (cx, cy) == (x1 - rad, y0 + rad)) or
                    (x < x0 + rad and y > y1 - rad and (cx, cy) == (x0 + rad, y1 - rad)) or
                    (x > x1 - rad and y > y1 - rad and (cx, cy) == (x1 - rad, y1 - rad))):
                    if (x - cx) ** 2 + (y - cy) ** 2 > rad * rad:
                        inside = False
            if inside:
                put(c, x, y, color, a)


def round_rect_outline(c, x0, y0, x1, y1, rad, color, thick=1):
    for t in range(thick):
        # draw a slightly smaller filled ring by overlaying outline color on edge
        pass
    # simple approach: draw filled rect of outline color, then we redraw inner fill later
    round_rect(c, x0, y0, x1, y1, rad, color)


def thick_line(c, x0, y0, x1, y1, r, color):
    steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        disc(c, x, y, r, color)


def crossed_bones(c):
    # two bones forming an X behind the die
    bones = (((15, 15), (49, 49)), ((49, 15), (15, 49)))
    for (a, b) in bones:
        # shaft
        thick_line(c, a[0], a[1], b[0], b[1], 2.2, PARCH_DK)
        thick_line(c, a[0], a[1], b[0], b[1], 1.4, PARCH)
        # knuckle knobs at each end
        for (kx, ky) in (a, b):
            dx = 2.4 if kx < 32 else -2.4
            disc(c, kx, ky - 2, 2.1, PARCH_DK); disc(c, kx, ky - 2, 1.3, PARCH)
            disc(c, kx, ky + 2, 2.1, PARCH_DK); disc(c, kx, ky + 2, 1.3, PARCH)


def die(c, cx, cy, half, face="five", body=BONE):
    x0, y0, x1, y1 = cx - half, cy - half, cx + half, cy + half
    rad = max(2, half * 0.32)
    # drop shadow
    round_rect(c, x0 + 2, y0 + 3, x1 + 2, y1 + 3, rad, (0, 0, 0), a=0.30)
    # outline then body
    round_rect(c, x0 - 1, y0 - 1, x1 + 1, y1 + 1, rad + 1, INK)
    round_rect(c, x0, y0, x1, y1, rad, body)
    # soft top highlight for a carved look
    round_rect(c, x0 + 2, y0 + 2, x1 - 2, y0 + 4, rad * 0.5, BONE_HI, a=0.6)

    inset = half * 0.42
    lo_x, hi_x = x0 + inset, x1 - inset
    lo_y, hi_y = y0 + inset, y1 - inset
    mx, my = cx, cy
    pr = max(2.0, half * 0.16)

    if face == "five":
        spots = [(lo_x, lo_y), (hi_x, lo_y), (mx, my), (lo_x, hi_y), (hi_x, hi_y)]
        for (px, py) in spots:
            disc(c, px, py, pr + 0.6, INK)
            disc(c, px, py, pr, PIP)
    elif face == "skull":
        skull(c, cx, cy, half)


SKULL = [
    "..######..",
    ".########.",
    "##########",
    "##.####.##",
    "##.####.##",
    "##########",
    ".##.##.##.",
    "..######..",
    ".#.####.#.",
    "..#.##.#..",
]


def skull(c, cx, cy, half):
    rows = SKULL
    h = len(rows)
    w = len(rows[0])
    px = max(1, (2 * half * 0.62) / w)
    ox = cx - (w * px) / 2
    oy = cy - (h * px) / 2
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '#':
                x = ox + i * px
                y = oy + j * px
                round_rect(c, x, y, x + px - 0.5, y + px - 0.5, 0, PIP)


def frame(c):
    # gold rounded border
    round_rect(c, 3, 3, N - 4, N - 4, 7, GOLD_DK)
    round_rect(c, 4, 4, N - 5, N - 5, 6, GOLD)
    # cut the interior back to the background by re-blitting bg inside — instead,
    # we draw the frame FIRST then content over it, so just inset-clear:
    # (handled by drawing order in compose())


def compose(face="five", bg=(TEAL_HI, NAVY_DK), die_body=BONE, with_bones=True):
    c = new_canvas()
    background(c, bg[0], bg[1])
    # gold frame ring
    round_rect(c, 3, 3, N - 4, N - 4, 7, GOLD_DK)
    round_rect(c, 4, 4, N - 5, N - 5, 6, GOLD)
    # clear interior back to gradient (so frame is a ring, not a filled plate)
    inner = new_canvas()
    background(inner, bg[0], bg[1])
    for y in range(7, N - 7):
        for x in range(7, N - 7):
            c[y][x] = list(inner[y][x])
    if with_bones:
        crossed_bones(c)
    die(c, 32, 33, 16, face=face, body=die_body)
    # a small gold glint, top-left of die
    disc(c, 24, 25, 1.4, BONE_HI, a=0.9)
    return c


def write_png(path, canvas):
    w = N * SCALE
    h = N * SCALE
    raw = bytearray()
    for row in canvas:
        line = bytearray()
        for (r, g, b) in row:
            line += bytes((r, g, b)) * SCALE
        for _ in range(SCALE):
            raw += b'\x00' + line

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(png)
    print("wrote", path, f"({w}x{h})")


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    appicon = os.path.join(here, "LiarsDice/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png")
    concepts = os.path.join(here, "docs/icon-concepts")

    # Primary: bone die (5) with crossed bones on teal->navy.
    write_png(appicon, compose(face="five"))

    write_png(os.path.join(concepts, "concept-bones.png"),
              compose(face="five"))
    write_png(os.path.join(concepts, "concept-clean.png"),
              compose(face="five", with_bones=False))
    write_png(os.path.join(concepts, "concept-gold.png"),
              compose(face="five", bg=(NAVY, NAVY_DK), die_body=GOLD, with_bones=True))


if __name__ == "__main__":
    main()
