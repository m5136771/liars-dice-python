"""
generate_assets.py
===================

Builds all of the pixel-art image assets for the graphical version of
Liar's Dice (see ``liars_dice_gui.py``). Run it once and it fills the
``assets/`` folder with PNG sprites:

    python generate_assets.py

Why generate the art with code instead of drawing it by hand?
  * Pixel art is literally a grid of coloured squares, so a little Python
    can describe each sprite exactly, pixel for pixel.
  * The sprites come out perfectly crisp, with a see-through (transparent)
    background, ready to drop straight into the game.
  * It is reproducible -- delete the folder, run this again, get the same art.
  * It is a fun thing for a learner to read: every sprite below is just a
    little picture spelled out with letters!

The art is authored at a tiny native size (e.g. 16x16 "pixels") and then
blown up with "nearest-neighbour" scaling so each little pixel becomes a
nice chunky block -- that is what gives it the retro, pixelated look.
"""

import os
from PIL import Image

# Where the finished PNGs go.
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# How many real screen-pixels each "art pixel" becomes when we blow the
# sprite up. Bigger number = chunkier blocks.
SCALE = 8

# ---------------------------------------------------------------------------
# The palette: every sprite is painted using only these colours. Keeping the
# list short is part of what makes it feel like cohesive pixel art. Each key
# is a single character we use in the little ASCII pictures further down.
# A value of None means "leave this pixel see-through".
# ---------------------------------------------------------------------------
PALETTE = {
    ".": None,             # transparent

    # Bone / ivory dice
    "o": (47, 37, 28),     # outline (dark brown)
    "b": (238, 230, 206),  # bone body
    "h": (255, 247, 230),  # bone highlight
    "s": (213, 197, 162),  # bone shadow
    "p": (47, 37, 28),      # dark pip (same as outline for a carved look)

    # Gold / treasure
    "g": (242, 193, 78),   # gold
    "G": (255, 224, 138),  # gold highlight
    "y": (201, 138, 43),   # gold shadow

    # Wood
    "w": (107, 74, 43),    # wood
    "W": (138, 94, 56),    # wood highlight
    "d": (74, 49, 25),     # wood dark

    # Leather (dice cup)
    "l": (122, 59, 31),    # leather
    "L": (156, 82, 48),    # leather highlight
    "k": (83, 38, 19),     # leather dark

    # Skull / bone white
    "f": (244, 239, 226),  # skull face
    "c": (204, 195, 173),  # skull shadow

    # Accents
    "r": (181, 52, 31),    # red
    "t": (47, 107, 107),   # teal
    "m": (40, 33, 26),     # near-black metal / iron
}


def render(rows, scale=SCALE, name="sprite"):
    """Turn a list of text rows into a scaled-up PNG and save it.

    Every character in ``rows`` is looked up in ``PALETTE`` to get its colour.
    Spaces are treated the same as '.' (transparent) for convenience.
    """
    height = len(rows)
    width = max(len(row) for row in rows)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == " ":
                ch = "."
            colour = PALETTE.get(ch)
            if colour is not None:
                px[x, y] = (colour[0], colour[1], colour[2], 255)
    # Blow it up with NEAREST so the pixels stay sharp little squares.
    img = img.resize((width * scale, height * scale), Image.NEAREST)
    path = os.path.join(ASSETS_DIR, name + ".png")
    img.save(path)
    return path


# ---------------------------------------------------------------------------
# Dice faces. Rather than hand-spell all six, we build them from one blank
# die plus the standard pip positions, so they are guaranteed to match.
# ---------------------------------------------------------------------------
# A blank 16x16 bone die: 'h' highlight top/left, 's' shadow bottom/right,
# 'b' body, 'o' outline, with a 1px drop shadow ('s') bottom-right.
DIE_BLANK = [
    "................",
    ".oooooooooooo...",
    ".ohhhhhhhhhhbo..",
    ".ohbbbbbbbbbbos.",
    ".ohbbbbbbbbbbos.",
    ".ohbbbbbbbbbbos.",
    ".ohbbbbbbbbbbos.",
    ".ohbbbbbbbbbbos.",
    ".ohbbbbbbbbbbos.",
    ".ohbbbbbbbbbbos.",
    ".ohbbbbbbbbbbos.",
    ".ohbbbbbbbbbbos.",
    ".obbbbbbbbbbsos.",
    ".oooooooooooos..",
    "..ssssssssssss..",
    "................",
]

# The nine possible pip slots, as (col, row) top-left corners on the grid.
# The bone face spans columns/rows 3..12, so pips at 3, 7 and 11 sit neatly
# symmetric (each pip is a 2x2 block).
PIP_SLOTS = {
    "tl": (3, 3),  "tc": (7, 3),  "tr": (11, 3),
    "ml": (3, 7),  "mc": (7, 7),  "mr": (11, 7),
    "bl": (3, 11), "bc": (7, 11), "br": (11, 11),
}

# Which slots are filled for each die value (classic dice layout).
DIE_PIPS = {
    1: ["mc"],
    2: ["tl", "br"],
    3: ["tl", "mc", "br"],
    4: ["tl", "tr", "bl", "br"],
    5: ["tl", "tr", "mc", "bl", "br"],
    6: ["tl", "tr", "ml", "mr", "bl", "br"],
}


def make_die(value):
    """Stamp the pips for ``value`` onto a copy of the blank die."""
    grid = [list(row) for row in DIE_BLANK]
    for slot in DIE_PIPS[value]:
        cx, cy = PIP_SLOTS[slot]
        # A 2x2 pip block makes a clean, readable dot at this size.
        for dx in (0, 1):
            for dy in (0, 1):
                grid[cy + dy][cx + dx] = "p"
    return ["".join(row) for row in grid]


# A face-down / hidden die: same body, with a carved skull-ish "?" so you
# know a bot is keeping it secret.
DIE_HIDDEN = [
    "................",
    ".oooooooooooo...",
    ".ohhhhhhhhhhbo..",
    ".ohbbbboobbbbos.",
    ".ohbbboppobbbos.",
    ".ohbbbbboppbbos.",
    ".ohbbbbbboobbos.",
    ".ohbbbbboobbbos.",
    ".ohbbbbbobbbbos.",
    ".ohbbbbbobbbbos.",
    ".ohbbbbboobbbos.",
    ".ohbbbbbbbbbbos.",
    ".obbbbbbbbbbsos.",
    ".oooooooooooos..",
    "..ssssssssssss..",
    "................",
]


# ---------------------------------------------------------------------------
# Decorative sprites, hand-authored pixel by pixel.
# ---------------------------------------------------------------------------
SKULL = [
    "................",
    "....oooooo......",
    "...offffffo.....",
    "..offffffffo....",
    ".offffffffffo...",
    ".offooffooffo...",
    ".offooffooffo...",
    ".offffffffffo...",
    ".offffooffffo...",
    "..offfooffffo...",
    "...offffffo.....",
    "....ofofofo.....",
    "...offffffo.....",
    "..o.o.o.o.o.o...",
    "...o.o.o.o.o....",
    "................",
]

CHEST = [
    "................",
    "................",
    "..gggggggggg....",
    ".gyGGGGGGGGyg...",
    ".gGggggggggGg...",
    ".gGgwwwwwwgGg...",
    "oooooooooooooo..",
    "owwwwwgwwwwwwo..",
    "owWWWggGwWWWwo..",
    "owwwwwgwwwwwwo..",
    "owWWWwgwWWWWwo..",
    "owwwwwgwwwwwwo..",
    "oooooooooooooo..",
    ".dddddddddddd...",
    "................",
    "................",
]

COIN = [
    "................",
    ".....oooo.......",
    "...ooyyyyoo.....",
    "..oyGGGGGGyo....",
    ".oyGGgggGGgyo...",
    ".oyGgG GgGGyo...",
    ".oyGgG GgGGyo...",
    ".oyGgG GgGGyo...",
    ".oyGgGgGGGGyo...",
    ".oyGGGGGGGGyo...",
    "..oyGGGGGGyo....",
    "...ooyyyyoo.....",
    ".....oooo.......",
    "................",
    "................",
    "................",
]

CUP = [
    "................",
    "..kkkkkkkkkk....",
    ".oLLLLLLLLLLo...",
    ".oLllllllllko...",
    "..klllllllk.....",
    "..kLlllllLk.....",
    "..klllllllk.....",
    "..kLlllllLk.....",
    "...klllllk......",
    "...kLlllLk......",
    "...klllllk......",
    "....klllk.......",
    "....kLLLk.......",
    "...okkkkko......",
    "..oLLLLLLLo.....",
    "...ooooooo......",
]

# A single wooden plank tile we repeat to make the table-top background.
PLANK = [
    "wwwwwwwwwwwwwwww",
    "wWwwwwdwwwwwWwww",
    "wwwwwwwwwwwwwwdw",
    "dwwwwWwwwwdwwwww",
    "wwwwwwwwwwwwwwww",
    "wwdwwwwwwWwwwwww",
    "wWwwwwwwwwwwwdww",
    "wwwwwdwwwwwwwwww",
    "wwwwwwwwwwwwwwww",
    "wwwWwwwdwwwwwwWw",
    "dwwwwwwwwwwdwwww",
    "wwwwwwwWwwwwwwww",
    "wwwwdwwwwwwwwwdw",
    "wWwwwwwwwdwwwwww",
    "wwwwwwwwwwwwWwww",
    "oooooooooooooooo",
]


def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    made = []

    # The six dice faces.
    for value in range(1, 7):
        made.append(render(make_die(value), name="die_%d" % value))

    # The hidden die and the decorative sprites.
    made.append(render(DIE_HIDDEN, name="die_hidden"))
    made.append(render(SKULL, name="skull"))
    made.append(render(CHEST, name="chest"))
    made.append(render(COIN, name="coin"))
    made.append(render(CUP, name="cup"))
    made.append(render(PLANK, name="plank"))

    print("Created %d sprites in %s :" % (len(made), ASSETS_DIR))
    for path in made:
        print("  " + os.path.basename(path))


if __name__ == "__main__":
    main()
