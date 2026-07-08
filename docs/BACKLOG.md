# Product backlog — Liar's Dice

A prioritized backlog of features and user stories on the road to (and past) an
App Store launch. Stories use the form **"As a … I want … so that …"** with
acceptance criteria where it helps.

**Priority:** `P0` = required for a credible launch · `P1` = strong first update ·
`P2` = growth / nice-to-have · `P3` = icebox.

**Status:** ✅ done · 🔶 partial · ⬜ not started.

---

## Milestone 1.0 — App Store launch (MVP)

### Epic A — Core gameplay ✅ (foundation complete)
- ✅ `P0` As a player, I want to play full rounds of Liar's Dice vs. bots so that
  I can enjoy the game solo. *(engine + loop done)*
- ✅ `P0` As a player, I want to raise or challenge on my turn so that I can bluff
  and call bluffs. *(done)*
- ✅ `P0` As a player, I want a reveal that counts all dice so that outcomes are
  clear and fair. *(done)*
- ✅ `P0` As a player, I want bots with adjustable difficulty so that the game
  scales to my skill. *(Cabin Boy / Buccaneer / Sea Devil)*
- 🔶 `P0` As a player, I want the game to feel alive (sound, haptics, dice
  animation) so that it's satisfying to play. *(audio + haptics + tumble done;
  more animation polish in 1.1)*

### Epic B — First-run & onboarding
- ⬜ `P0` As a new player, I want a short interactive tutorial (or a clear rules
  card on first launch) so that I can learn without reading a wall of text.
  - **AC:** First launch shows a 3–4 step walkthrough or a dismissible rules
    overlay; never blocks returning players; reachable later from the menu.
- ✅ `P0` As a player, I want to set my name so that the game feels personal.
- ⬜ `P1` As a player, I want a "how to play" entry in-game (not just the menu) so
  that I can review rules mid-session.

### Epic C — Visual identity & art
- ✅ `P0` As a user browsing the App Store, I want a distinctive app icon so that
  the game looks legit. *(pixel-art bone-die icon shipped)*
- ✅ `P0` As a player, I want a consistent retro look so that the game feels
  designed. *(Theme + ART_DIRECTION.md)*
- ⬜ `P1` As a player, I want characterful opponents (pirate avatars) so that the
  table feels populated.
- ⬜ `P2` As a player, I want a real pixel font so that text matches the art.

### Epic D — Settings & accessibility
- ✅ `P0` As a player, I want to toggle sound and haptics so that I can play
  quietly. *(done)*
- ⬜ `P0` As a player using VoiceOver, I want dice, bids, and buttons labelled so
  that the game is accessible.
  - **AC:** All interactive controls have accessibility labels; the current bid
    and your dice are announced; passes an Accessibility Inspector audit.
- ⬜ `P1` As a player, I want Dynamic Type / larger text support so that I can
  read comfortably.
- ⬜ `P1` As a player who prefers calm UI, I want a "reduce motion" path so that
  dice don't tumble if I disable animation.

### Epic E — App Store readiness
- ⬜ `P0` Replace the placeholder bundle id and set the signing team.
- ⬜ `P0` Capture screenshots for required device sizes (6.7" + 6.5").
- ⬜ `P0` Write App Store metadata (name, subtitle, description, keywords).
- ⬜ `P0` Complete the App Privacy questionnaire ("Data Not Collected") and host a
  one-page privacy policy.
- ⬜ `P0` Answer the age-rating questionnaire (expected 12+, simulated gambling:
  none).
- ⬜ `P0` TestFlight build verified on a real device, then submit for review.

---

## Milestone 1.1 — First update (retention & polish)

### Epic F — Juice & animation 🔶
- ⬜ `P1` As a player, I want dice to tumble through random faces before settling
  so that rolls feel real.
- ⬜ `P1` As a player, I want the cups to lift and dice to pop on the reveal so
  that the climax lands.
- ⬜ `P2` As a player, I want coins/confetti on a win so that victory feels
  rewarding.
- ⬜ `P1` As a player, I want a quick roll-off animation to decide who starts so
  that the opener feels earned (a nod to the original).

### Epic G — Progression & stats
- ⬜ `P1` As a returning player, I want my stats (games, wins, bluffs caught) saved
  so that I can track improvement.
  - **AC:** Stats persist across launches (SwiftData/`@AppStorage`); a simple
    stats screen shows totals and a win streak.
- ⬜ `P2` As a player, I want achievements so that I have goals to chase.

### Epic H — AI depth
- ⬜ `P1` As a skilled player, I want a smarter "Sea Devil" that tracks bid history
  and models opponents so that hard mode is genuinely hard.
- ⬜ `P2` As a player, I want bots with distinct personalities (cautious, reckless,
  bluffer) so that opponents feel individual.

---

## Milestone 1.2+ — Growth

### Epic I — Game modes
- ⬜ `P1` As a player, I want a **Daily Challenge** (seeded dice, same for
  everyone, shareable result) so that I have a reason to return daily.
  - **AC:** Uses `SeededRandomNumberGenerator` keyed to the date; result is
    shareable as text/image.
- ⬜ `P2` As friends in a room, I want **pass-and-play** local multiplayer so that
  we can play on one device.
- ⬜ `P3` As a player, I want **online multiplayer** (Game Center) so that I can
  play remotely. *(large effort; validate demand first)*

### Epic J — Monetization
- ⬜ `P1` As a maker, I want a single tip-jar IAP (StoreKit 2) or a $1.99 price so
  that the game can earn while keeping the privacy story clean.
- ⬜ `P2` As a player, I want cosmetic dice skins / table themes (IAP) so that I
  can customize; as a maker this is the best long-term revenue.
- ⬜ `P3` As a maker, I want rewarded ads as an alternative to IAP. *(adds privacy
  + review overhead; only if pursuing free-with-ads.)*

### Epic K — Reach & quality
- ⬜ `P2` As a non-English player, I want localization so that I can play in my
  language. *(strings are already centralized in Flavor.swift.)*
- ⬜ `P2` As a maker, I want lightweight, privacy-respecting analytics + crash
  reporting so that I can fix issues. *(weigh against "Data Not Collected".)*
- ⬜ `P2` As an iPad player, I want a tuned landscape/iPad layout so that the game
  looks great on a larger screen.

---

## Notes
- Keep **"Data Not Collected"** true as long as possible — it makes review and the
  privacy label trivial. Adding ads or analytics changes that; decide deliberately.
- Bluffing ≠ real-money gambling. Avoid casino chrome (slot reels, real currency)
  to keep the age rating low and review smooth.
