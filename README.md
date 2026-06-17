# Liar's Dice ☠︎

A pirate-themed game of **Liar's Dice** (a.k.a. Pirate's Dice) for **iOS**,
written in **Swift / SwiftUI**. Bluff your way past a crew of bots, call out
their lies, and don't be the last scallywag holding nothing — or you'll be
sentenced to the Flying Dutchman to listen to Crazy Pete for eternity.

> This project began life as a heavily-commented Python CLI used to teach high
> school students to code. It is now being rebuilt as a native iOS game for the
> App Store. The original teaching code is preserved under
> [`python-legacy/`](python-legacy/).

## Project layout

```
LiarsDice.xcodeproj      The iOS app project — open this in Xcode
LiarsDice/
  App/                   App entry point and root navigation
  Engine/                Pure game logic (no UI) — the rules live here
  ViewModels/            GameViewModel: drives the engine, paces bot turns
  Views/                 SwiftUI screens (menu, table, dice, reveal, game over)
  Theme/                 Retro "pirate tavern" colors, fonts, components
  Resources/             Flavor text (pirate narration, the Crazy Pete ending)
  Assets.xcassets/       App icon + accent color
Package.swift            Builds/tests the Engine from the command line
Tests/                   Engine unit tests (swift test, or run in Xcode)
project.yml              XcodeGen spec (recovery path; see Makefile)
python-legacy/           The original Python teaching game, kept for posterity
docs/ROADMAP.md          The plan to ship this on the App Store
```

The engine is deliberately separated from the UI: `LiarsDice/Engine` is pure
value-type Swift with no SwiftUI imports. It compiles into the app **and** into
a standalone Swift package so the rules can be unit-tested in seconds without a
simulator.

## Getting started (on a Mac with Xcode 16+)

```bash
# 1. Run the engine tests — no Xcode UI required
swift test            # or: make test

# 2. Open and run the app
open LiarsDice.xcodeproj   # or: make open
#   then pick an iPhone simulator and press ⌘R
```

Before building to a device or submitting, set your signing team and a real
bundle identifier in Xcode (**Target ▸ Signing & Capabilities**). The project
ships with a placeholder bundle id `com.example.liarsdice`.

If the committed Xcode project ever drifts, regenerate it from `project.yml`:

```bash
brew install xcodegen && xcodegen generate   # or: make project
```

## How to play

1. Everyone secretly rolls their dice. You see yours; the crew hides theirs.
2. On your turn you either:
   - **RAISE** the bid — claim there are *more* dice of a value, **or** the same
     number of a *higher* value, across everyone's cups; or
   - **CHALLENGE** the last bid if you think it's a lie.
3. On a challenge, all dice are counted. Guess wrong and you lose a die.
4. Lose all your dice and you're out. Last pirate standing wins the gold.

House rules (set on the main menu): crew size, bot difficulty, and an optional
"ones are wild" variant.

## Status & roadmap

This is an early, fully-playable foundation: complete rules engine, single-player
vs. bots, full game loop, and a styled UI. See
[`docs/ROADMAP.md`](docs/ROADMAP.md) for what's next on the way to the App Store
(app icon & art, sound, polish, App Store Connect setup, TestFlight, and review).
