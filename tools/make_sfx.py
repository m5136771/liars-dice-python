#!/usr/bin/env python3
"""
Generate the game's chiptune sound effects as small 8-bit-style WAV files,
using only the Python standard library (`wave`). No samples to license, fully
reproducible, and on-brand with the retro pixel-art look.

Usage:
    python3 tools/make_sfx.py

Outputs (16-bit mono, 22.05 kHz) into LiarsDice/Resources/Audio/:
    roll, bid, challenge, reveal_good, reveal_lie, lose_die, win, lose
"""

import os
import wave
import struct
import math
import random

SR = 22050
random.seed(7)


def envelope(i, n, attack, release):
    t = i / SR
    dur = n / SR
    a = min(1.0, t / attack) if attack > 0 else 1.0
    rem = max(0.0, dur - t)
    r = min(1.0, rem / release) if release > 0 else 1.0
    return a * r


def wave_sample(kind, freq, t, duty=0.5):
    if kind == "square":
        return 1.0 if (t * freq) % 1.0 < duty else -1.0
    if kind == "triangle":
        return 4.0 * abs(((t * freq) % 1.0) - 0.5) - 1.0
    if kind == "noise":
        return random.uniform(-1.0, 1.0)
    return math.sin(2 * math.pi * freq * t)


def note(buf, start, dur, freq, kind="square", vol=0.4,
         glide=None, attack=0.005, release=None, duty=0.5):
    n = int(dur * SR)
    if release is None:
        release = dur * 0.6
    for i in range(n):
        t = i / SR
        f = freq if glide is None else freq + (glide - freq) * (i / n)
        s = wave_sample(kind, f, t, duty)
        idx = start + i
        if 0 <= idx < len(buf):
            buf[idx] += s * vol * envelope(i, n, attack, release)


def buffer(dur):
    return [0.0] * int(dur * SR)


def write_wav(path, buf):
    frames = bytearray()
    for s in buf:
        v = max(-1.0, min(1.0, s))
        frames += struct.pack("<h", int(v * 32767))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(bytes(frames))
    print("wrote", path, f"({len(buf)/SR:.2f}s)")


def fx_roll():
    b = buffer(0.5)
    for k in range(4):
        start = int((0.02 + k * 0.095) * SR)
        note(b, start, 0.07, 0, "noise", vol=0.30, attack=0.002, release=0.06)
    note(b, 0, 0.12, 90, "triangle", vol=0.12, release=0.1)  # low body
    return b


def fx_bid():
    b = buffer(0.12)
    note(b, 0, 0.08, 880, "square", vol=0.33, attack=0.003, release=0.06, duty=0.4)
    return b


def fx_challenge():
    b = buffer(0.42)
    note(b, 0, 0.30, 440, "square", vol=0.38, glide=120, release=0.26)
    note(b, 0, 0.18, 0, "noise", vol=0.16, release=0.16)
    return b


def fx_reveal_good():
    b = buffer(0.42)
    for k, f in enumerate((523.25, 659.25, 783.99)):
        note(b, int(k * 0.08 * SR), 0.13, f, "square", vol=0.30, release=0.11)
    return b


def fx_reveal_lie():
    b = buffer(0.46)
    note(b, 0, 0.40, 415.30, "triangle", vol=0.40, glide=246.94, release=0.30)
    return b


def fx_lose_die():
    b = buffer(0.22)
    note(b, 0, 0.18, 600, "square", vol=0.30, glide=200, release=0.14)
    return b


def fx_win():
    b = buffer(0.8)
    for f, start in ((523.25, 0.0), (659.25, 0.12), (783.99, 0.24), (1046.50, 0.36)):
        note(b, int(start * SR), 0.18, f, "square", vol=0.30, release=0.16)
    note(b, int(0.36 * SR), 0.34, 1046.50, "triangle", vol=0.16, release=0.30)
    return b


def fx_lose():
    b = buffer(0.85)
    for f, start in ((440, 0.0), (349.23, 0.18), (293.66, 0.36), (220, 0.54)):
        note(b, int(start * SR), 0.24, f, "triangle", vol=0.34, release=0.20)
    return b


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, "LiarsDice/Resources/Audio")
    effects = {
        "roll": fx_roll,
        "bid": fx_bid,
        "challenge": fx_challenge,
        "reveal_good": fx_reveal_good,
        "reveal_lie": fx_reveal_lie,
        "lose_die": fx_lose_die,
        "win": fx_win,
        "lose": fx_lose,
    }
    for name, fn in effects.items():
        write_wav(os.path.join(out, name + ".wav"), fn())


if __name__ == "__main__":
    main()
