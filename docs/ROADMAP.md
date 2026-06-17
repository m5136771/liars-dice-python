# Roadmap: from teaching script to App Store game

This is the honest, end-to-end plan for turning Liar's Dice into a shippable
iOS game. It's split into what's **done**, what's **next**, and the **store
mechanics** that only you (with the Mac + Apple Developer account) can do.

---

## ✅ Phase 0 — Foundation (this commit)

- [x] Pivot the repo from a Python CLI to a native **Swift / SwiftUI** app.
- [x] **Pure rules engine** (`LiarsDice/Engine`): bids, raises, challenges,
      reveal/tally, dice loss, elimination, win/lose — all deterministic and
      unit-tested via `swift test`.
- [x] **Bot AI** with three difficulty levels, ported and tightened from the
      original Python bots.
- [x] **Game loop UI**: main menu with settings, the table with opponents and
      your cup, bidding controls, the dramatic reveal, and win/lose screens.
- [x] Preserved the game's personality — pirate narration and the legendary
      **Crazy Pete** defeat sequence.
- [x] A buildable `LiarsDice.xcodeproj` (plus an XcodeGen recovery spec).

## 🎨 Phase 1 — Make it look and feel finished

- [ ] **App icon** (1024×1024). The asset slot is wired up but empty — this is
      the single most visible missing piece. Options: commission pixel art, or
      generate one and drop the PNG into
      `LiarsDice/Assets.xcassets/AppIcon.appiconset`.
- [ ] **Pixel-art dice & table sprites** (optional upgrade). The dice are
      currently drawn with SwiftUI shapes, which looks clean and scales
      perfectly; swapping in hand-drawn sprites is a localized change in
      `DieView`/`OpponentView`.
- [ ] **A real pixel font** (e.g. *Press Start 2P*). Bundle the `.ttf`, register
      it, and update `RetroFont` — one place, the whole app changes.
- [ ] **Sound & haptics**: dice rattle, a thud on challenge, a sting on a lie,
      victory jingle. Use `AVAudioPlayer` + `UIImpactFeedbackGenerator`.
- [ ] **Animation polish**: dice actually tumbling through random faces, cups
      lifting on the reveal, coins on a win.

## 🕹️ Phase 2 — Depth & retention

- [ ] Roll-off animation to decide who starts (a nod to the original).
- [ ] Stats & streaks (games won, bluffs caught) via `@AppStorage`/SwiftData.
- [ ] **Daily challenge** using the existing `SeededRandomNumberGenerator` — same
      dice for everyone, shareable result.
- [ ] Difficulty tuning and a smarter "Sea Devil" AI (track bid history, model
      opponents).
- [ ] Accessibility: VoiceOver labels for dice/bids, Dynamic Type, reduce-motion.
- [ ] Optional: local **pass-and-play** multiplayer, then Game Center online.

## 🚀 Phase 3 — Ship it (your turn — needs the Mac + Apple Developer account)

These steps require your Apple Developer account ($99/yr) and signing identity.

1. **Bundle identifier & signing**
   - In Xcode ▸ target **LiarsDice** ▸ *Signing & Capabilities*: pick your Team,
     set a unique bundle id (replace `com.example.liarsdice`, e.g.
     `com.<you>.liarsdice`).
2. **App Store Connect**
   - Create the app record at <https://appstoreconnect.apple.com> with that
     bundle id, a name (check availability), and primary category **Games →
     Board** (or **Casino/Card**).
3. **Privacy**
   - This app collects **no data** and has no network calls or third-party SDKs,
     so the *App Privacy* questionnaire is "Data Not Collected" and a Privacy
     Manifest is trivial. (Keep it that way for the easiest review.)
   - Liar's Dice involves bluffing, not real-money gambling → expect a **12+**
     age rating ("Simulated Gambling: None"; "Infrequent/Mild" only if you add
     casino theming). Answer the rating questionnaire honestly.
4. **Marketing assets**
   - Screenshots for required device sizes (6.7" and 6.5" iPhone at minimum) —
     capture from the simulator.
   - App description, keywords, support URL, and a privacy-policy URL (a simple
     hosted page stating "no data collected" suffices).
5. **Monetization** (decide early; see below)
   - Set price (free or paid) or add In-App Purchases / ads.
6. **TestFlight**
   - Archive (*Product ▸ Archive*), upload, and test on real devices / invite
     friends before submitting.
7. **Submit for review**
   - Submit the build, respond to any reviewer questions, then release.

## 💰 Monetization options (pick one to aim for)

| Model | Effort | Notes |
|---|---|---|
| **Paid up front** (e.g. $1.99) | Lowest | Simplest; no SDKs, cleanest privacy. |
| **Free + "Remove distractions / tip jar" IAP** | Low | One non-consumable via StoreKit 2. |
| **Free + rewarded/banner ads** | Medium | Adds an ad SDK → privacy + review overhead. |
| **Free + cosmetic IAP** (dice skins, themes) | Higher | Best long-term if the game has legs. |

Recommendation: launch **free with a single optional "tip jar" IAP**, or paid at
$1.99 — both keep the privacy story clean and review fast. Add cosmetic IAPs in
a later update once you see retention.

## ⚠️ Things to know

- A 1024×1024 **app icon is required** to submit — the build runs without one,
  but App Store Connect will reject a submission that lacks it.
- Replace the **placeholder bundle id** before archiving.
- Apple review for a simple, offline game is usually quick, but budget a few
  days and be ready to answer the gambling/age-rating questions.
- **Continuous integration** isn't set up: GitHub-hosted runners (macOS *and*
  Linux) failed to provision for this repo — every job died at startup with no
  runner assigned, which points to Actions being disabled or limited on the
  account, not a code problem. To enable CI later, turn on GitHub-hosted runners
  (or add a self-hosted one) under the repo/owner **Settings → Actions**, then a
  workflow can run `swift test` (engine) and `xcodebuild` (the app). Until then,
  verify locally with `swift test` and an Xcode build.
