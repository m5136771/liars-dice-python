# liars-dice-python

A simple, silly, pirate-themed game of **Liar's Dice** (a.k.a. Pirate's Dice),
written in Python to help high school students learn to code. The code is
heavily commented so you can follow exactly what every section does.

You play against three bots aboard a pirate ship. Lie well, call out the liars,
and don't be the last scallywag holding no dice... or you'll be stuck listening
to Crazy Pete for all eternity.

## How to run it

You need Python 3 installed. Then, from this folder:

```
python liars_dice.py
```

(On some computers the command is `python3` instead of `python`.)

## How to play

1. Everyone secretly rolls their dice. You can see yours; the bots hide theirs.
2. On your turn you either:
   - **RAISE** the bid — claim there are *more* dice of a value, **or** the same
     number of a *higher* value, across everyone's cups, or
   - **CHALLENGE** the last bid if you think it's a lie.
3. When a bid is challenged, everyone reveals their dice and we count them up:
   - If there really are at least that many, the bid was good and the
     **challenger** loses a die.
   - If there aren't enough, the bid was a lie and the **bidder** loses a die.
4. Lose all your dice and you're out. The last pirate standing wins!

## Files

- `liars_dice.py` — the complete, playable game.
- `learning_liars_dice.py` — the original "thinking out loud" notes showing how
  the project was figured out, step by step. Great for learners to read!
- `init.py` — a tiny package file with a version number and a greeting.
