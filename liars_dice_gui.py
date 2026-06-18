"""
liars_dice_gui.py
=================

A graphical (point-and-click) version of Liar's Dice that uses the pixel-art
sprites in the ``assets/`` folder. The original terminal game in
``liars_dice.py`` still works exactly as before -- this is just a second,
prettier way to play the same game.

How to run it::

    python generate_assets.py     # once, to create the artwork (assets/)
    python liars_dice_gui.py      # play!

You need two libraries: ``pygame`` and ``pillow`` (Pillow is only needed by
generate_assets.py). Install them with::

    pip install pygame pillow

The game:
  * You and three bots each start with five dice.
  * On your turn, RAISE the bid (more dice, or the same many of a higher
    value) or CHALLENGE the last bid if you think it's a lie.
  * On a challenge everyone's dice are revealed and counted. Whoever was
    wrong loses a die. Lose all your dice and you're out. Last one standing
    wins!
"""

import os
import sys
import random

import pygame

# ---------------------------------------------------------------------------
# Basic settings
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1000, 720
FPS = 60
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Colours (R, G, B)
INK = (33, 27, 21)
PARCHMENT = (238, 230, 206)
GOLD = (242, 193, 78)
GOLD_DK = (201, 138, 43)
RED = (181, 52, 31)
GREEN = (74, 120, 64)
TEAL = (47, 107, 107)
PANEL = (60, 42, 28)
PANEL_LT = (84, 60, 40)
SHADOW = (26, 18, 12, 120)

# Display sizes for the dice sprites (the PNGs are 128x128).
HAND_DIE = 56     # dice shown in the human's hand
BOT_DIE = 40      # smaller dice for the three bots (they hold 5 in a row)
PICK_DIE = 52     # dice in the value picker
ICON = 44         # small avatar / coin icons

BOT_NAMES = ["Bot 1", "Bot 2", "Bot 3"]


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------
def load_image(name, size=None):
    path = os.path.join(ASSETS_DIR, name + ".png")
    img = pygame.image.load(path).convert_alpha()
    if size is not None:
        img = pygame.transform.scale(img, (size, size))
    return img


def load_assets():
    """Load every sprite at the sizes we need and return them in a dict."""
    if not os.path.isdir(ASSETS_DIR) or not os.path.exists(
        os.path.join(ASSETS_DIR, "die_1.png")
    ):
        raise SystemExit(
            "Could not find the artwork. Run 'python generate_assets.py' first!"
        )

    art = {}
    # Dice faces in a player's hand and in the picker. Bots get smaller dice
    # so all five fit neatly in their narrower panels.
    art["hand"] = {v: load_image("die_%d" % v, HAND_DIE) for v in range(1, 7)}
    art["hand_sm"] = {v: load_image("die_%d" % v, BOT_DIE) for v in range(1, 7)}
    art["pick"] = {v: load_image("die_%d" % v, PICK_DIE) for v in range(1, 7)}
    art["hidden"] = load_image("die_hidden", HAND_DIE)
    art["hidden_sm"] = load_image("die_hidden", BOT_DIE)
    # Decorative sprites.
    art["skull"] = load_image("skull", ICON)
    art["skull_big"] = load_image("skull", 120)
    art["coin"] = load_image("coin", 32)
    art["cup"] = load_image("cup", ICON)
    art["chest"] = load_image("chest", 160)
    # A tiling wood plank for the table background.
    art["plank"] = load_image("plank")  # full 128x128 tile
    return art


# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------
class Player:
    def __init__(self, name, is_bot):
        self.name = name
        self.is_bot = is_bot
        self.num_dice = 5
        self.dice = []           # current rolled values

    def roll(self):
        self.dice = [random.randint(1, 6) for _ in range(self.num_dice)]


class Game:
    """Holds all the rules and the current state of a match."""

    def __init__(self, player_name="You"):
        self.players = [Player(player_name, False)] + [
            Player(n, True) for n in BOT_NAMES
        ]
        self.human = self.players[0]
        self.current = self.players[0]      # whose turn it is
        self.bidder = None                  # who made the standing bid
        self.bid_q = 0
        self.bid_v = 0
        self.dice_in_play = 0
        self.phase = "intro"                # see the main loop for phases
        self.message = "Roll to see who goes first!"
        self.reveal_loser = None
        self.last_total = 0
        self.winner = None
        # Human's in-progress bid choices.
        self.pick_v = 1
        self.pick_q = 1

    # --- helpers -----------------------------------------------------------
    def alive(self):
        return [p for p in self.players if p.num_dice > 0]

    def loses_die_phrase(self, p):
        """Grammatically correct 'X loses a die' that handles 'You'."""
        return "You lose a die." if p is self.human else "%s loses a die." % p.name

    def next_player(self, player):
        order = self.players
        i = order.index(player)
        for step in range(1, len(order) + 1):
            nxt = order[(i + step) % len(order)]
            if nxt.num_dice > 0:
                return nxt
        return player

    def count_value(self, value):
        return sum(p.dice.count(value) for p in self.players if p.num_dice > 0)

    def higher_bid(self, q, v):
        return q > self.bid_q or (q == self.bid_q and v > self.bid_v)

    # --- flow --------------------------------------------------------------
    def start_round(self, starting_player):
        for p in self.players:
            if p.num_dice > 0:
                p.roll()
            else:
                p.dice = []
        self.dice_in_play = sum(p.num_dice for p in self.players)
        self.bidder = None
        self.bid_q = 0
        self.bid_v = 0
        self.current = starting_player
        self.reveal_loser = None
        self.pick_v = 1
        self.pick_q = 1
        if self.current.is_bot:
            self.phase = "bot_think"
            self.bot_timer = 0
            self.message = self.current.name + " opens the bidding..."
        else:
            self.phase = "human"
            self.message = "Your turn! Make the opening bid."

    def opening_bid_for_bot(self, bot):
        value = random.randint(1, 6)
        quantity = bot.dice.count(value) + random.randint(0, 1)
        quantity = max(1, min(quantity, self.dice_in_play))
        return quantity, value

    def bot_decide(self, bot):
        """Return ('challenge', None, None) or ('raise', q, v)."""
        # Opening bid -- nothing to challenge yet.
        if self.bidder is None:
            q, v = self.opening_bid_for_bot(bot)
            return ("raise", q, v)

        own = bot.dice.count(self.bid_v)
        others = self.dice_in_play - bot.num_dice
        expected = own + others / 6.0
        can_raise_q = self.bid_q < self.dice_in_play
        can_raise_v = self.bid_v < 6

        if not can_raise_q and not can_raise_v:
            challenge = True
        elif self.bid_q > expected + 1:
            challenge = random.randint(1, 10) <= 8
        elif self.bid_q > expected:
            challenge = random.randint(1, 10) <= 3
        else:
            challenge = random.randint(1, 10) <= 1

        if challenge:
            return ("challenge", None, None)
        if can_raise_v and random.randint(1, 2) == 1:
            return ("raise", self.bid_q, self.bid_v + 1)
        if can_raise_q:
            return ("raise", self.bid_q + 1, self.bid_v)
        return ("raise", self.bid_q, self.bid_v + 1)

    def apply_raise(self, player, q, v):
        self.bid_q = q
        self.bid_v = v
        self.bidder = player
        if player is self.human:
            self.message = "You bid %s." % bid_text(q, v)
        else:
            self.message = "%s bids %s." % (player.name, bid_text(q, v))
        self.current = self.next_player(player)
        if self.current.is_bot:
            self.phase = "bot_think"
            self.bot_timer = 0
        else:
            self.phase = "human"
            self.pick_q = max(1, q)
            self.pick_v = v

    def apply_challenge(self, challenger):
        self.last_total = self.count_value(self.bid_v)
        if self.last_total >= self.bid_q:
            # Bid was good -> the challenger was wrong.
            self.reveal_loser = challenger
            if self.bidder is self.human:
                truth = "You were telling the truth!"
            else:
                truth = "%s was telling the truth!" % self.bidder.name
            verdict = "%s %s" % (truth, self.loses_die_phrase(challenger))
        else:
            self.reveal_loser = self.bidder
            verdict = "It was a lie! %s" % self.loses_die_phrase(self.bidder)
        if challenger is self.human:
            head = "You challenge %s!" % self.bidder.name
        else:
            head = "%s challenges %s!" % (challenger.name, self.bidder.name)
        self.message = "%s %s" % (head, verdict)
        self.phase = "reveal"

    def resolve_round(self):
        """After the reveal, take a die from the loser and set up the next
        round (or end the game)."""
        loser = self.reveal_loser
        loser.num_dice -= 1
        if loser.num_dice <= 0:
            loser.dice = []
            if loser is self.human:
                self.phase = "game_over"
                self.winner = None
                self.message = "You lost your last die! Walk the plank..."
                return
            self.message = "%s is out of the game!" % loser.name

        survivors = self.alive()
        if len(survivors) == 1:
            self.winner = survivors[0]
            self.phase = "game_over"
            if self.winner is self.human:
                self.message = "You are the last pirate standing -- YOU WIN!"
            else:
                self.message = "%s wins the game!" % self.winner.name
            return

        # Loser starts the next round (or the next player if they're out).
        starter = loser if loser.num_dice > 0 else self.next_player(loser)
        self.start_round(starter)


def bid_text(q, v):
    word = "die" if q == 1 else "dice"
    return "%d %s showing %d" % (q, word, v)


# ---------------------------------------------------------------------------
# A tiny clickable button
# ---------------------------------------------------------------------------
class Button:
    def __init__(self, rect, label, colour=PANEL_LT, enabled=True):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.colour = colour
        self.enabled = enabled

    def draw(self, surf, font):
        col = self.colour if self.enabled else (70, 70, 70)
        pygame.draw.rect(surf, INK, self.rect.inflate(6, 6), border_radius=8)
        pygame.draw.rect(surf, col, self.rect, border_radius=8)
        # top highlight
        hi = self.rect.copy()
        hi.height = hi.height // 2
        pygame.draw.rect(
            surf, lighten(col, 25), hi, border_top_left_radius=8,
            border_top_right_radius=8,
        )
        txt = font.render(self.label, True, PARCHMENT if self.enabled else (160, 160, 160))
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def hit(self, pos):
        return self.enabled and self.rect.collidepoint(pos)


def lighten(c, amt):
    return tuple(min(255, x + amt) for x in c[:3])


def darken(c, amt):
    return tuple(max(0, x - amt) for x in c[:3])


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
class UI:
    def __init__(self, surface, art):
        self.surf = surface
        self.art = art
        self.font_big = pygame.font.SysFont("georgia,serif", 40, bold=True)
        self.font = pygame.font.SysFont("georgia,serif", 26, bold=True)
        self.font_sm = pygame.font.SysFont("georgia,serif", 20)
        self.buttons = {}

    # background of tiled wood planks, slightly darkened
    def draw_table(self):
        plank = self.art["plank"]
        pw, ph = plank.get_size()
        for y in range(0, HEIGHT, ph):
            for x in range(0, WIDTH, pw):
                self.surf.blit(plank, (x, y))
        # darken with a translucent overlay for contrast
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((20, 12, 6, 90))
        self.surf.blit(veil, (0, 0))

    def panel(self, rect, highlight=False):
        rect = pygame.Rect(rect)
        pygame.draw.rect(self.surf, INK, rect.inflate(8, 8), border_radius=12)
        pygame.draw.rect(self.surf, PANEL, rect, border_radius=12)
        edge = GOLD if highlight else PANEL_LT
        pygame.draw.rect(self.surf, edge, rect, width=3, border_radius=12)

    def text(self, s, pos, font=None, colour=PARCHMENT, center=False):
        font = font or self.font
        img = font.render(s, True, colour)
        r = img.get_rect()
        if center:
            r.center = pos
        else:
            r.topleft = pos
        self.surf.blit(img, r)
        return r

    def draw_player(self, game, player, rect, reveal):
        rect = pygame.Rect(rect)
        self.panel(rect, highlight=(player is game.current and game.phase in ("human", "bot_think")))
        # avatar + name
        avatar = self.art["cup"] if not player.is_bot else self.art["skull"]
        self.surf.blit(avatar, (rect.x + 12, rect.y + 10))
        name_col = GOLD if player is game.current else PARCHMENT
        self.text(player.name, (rect.x + 64, rect.y + 16), self.font, name_col)
        # dice-left counter with a coin
        self.surf.blit(self.art["coin"], (rect.right - 78, rect.y + 12))
        self.text("x%d" % player.num_dice, (rect.right - 44, rect.y + 14), self.font, GOLD)

        # the dice themselves (smaller for bots so 5 fit in the panel)
        dsize = BOT_DIE if player.is_bot else HAND_DIE
        faces = self.art["hand_sm"] if player.is_bot else self.art["hand"]
        hidden = self.art["hidden_sm"] if player.is_bot else self.art["hidden"]
        dx = rect.x + 16
        dy = rect.y + 64
        show_faces = (not player.is_bot) or reveal
        if player.num_dice == 0:
            self.text("- knocked out -", (dx, dy + 6), self.font_sm, (150, 140, 120))
            return
        for i in range(player.num_dice):
            if show_faces and i < len(player.dice):
                sprite = faces[player.dice[i]]
            else:
                sprite = hidden
            self.surf.blit(sprite, (dx + i * (dsize + 6), dy))

    def draw_bid_banner(self, game):
        rect = pygame.Rect(WIDTH // 2 - 230, 250, 460, 96)
        self.panel(rect, highlight=True)
        if game.bidder is None:
            self.text("No bid yet", (rect.centerx, rect.y + 26),
                      self.font, GOLD, center=True)
        else:
            self.text("Current bid", (rect.centerx, rect.y + 20),
                      self.font_sm, PARCHMENT, center=True)
            self.text("%d" % game.bid_q, (rect.centerx - 70, rect.centery + 8),
                      self.font_big, GOLD, center=True)
            self.text("x", (rect.centerx - 24, rect.centery + 8),
                      self.font, PARCHMENT, center=True)
            self.surf.blit(self.art["hand"][game.bid_v],
                           (rect.centerx + 4, rect.centery - 18))
            self.text("by %s" % game.bidder.name, (rect.centerx + 110, rect.centery + 8),
                      self.font_sm, PARCHMENT, center=True)
        self.text("%d dice in play" % game.dice_in_play, (rect.centerx, rect.bottom + 18),
                  self.font_sm, PARCHMENT, center=True)

    def draw_message(self, game):
        rect = pygame.Rect(40, HEIGHT - 168, WIDTH - 80, 44)
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        self.surf.blit(s, rect.topleft)
        self.text(game.message, (rect.centerx, rect.centery),
                  self.font, PARCHMENT, center=True)

    def draw_controls(self, game):
        """The human's RAISE / CHALLENGE controls along the bottom."""
        self.buttons = {}
        base_y = HEIGHT - 110

        if game.phase == "human":
            # value picker (six dice)
            px = 40
            py = base_y + 6
            self.text("Value:", (px, py - 26), self.font_sm, PARCHMENT)
            for v in range(1, 7):
                r = pygame.Rect(px + (v - 1) * (PICK_DIE + 8), py, PICK_DIE, PICK_DIE)
                if v == game.pick_v:
                    pygame.draw.rect(self.surf, GOLD, r.inflate(10, 10), border_radius=8)
                self.surf.blit(self.art["pick"][v], r.topleft)
                self.buttons["v%d" % v] = Button(r, "")
            # quantity stepper
            qx = px + 6 * (PICK_DIE + 8) + 30
            self.text("How many:", (qx, py - 26), self.font_sm, PARCHMENT)
            minus = Button((qx, py, 48, PICK_DIE), "-")
            self.buttons["q-"] = minus
            minus.draw(self.surf, self.font_big)
            self.text(str(game.pick_q), (qx + 86, py + PICK_DIE // 2),
                      self.font_big, GOLD, center=True)
            plus = Button((qx + 120, py, 48, PICK_DIE), "+")
            self.buttons["q+"] = plus
            plus.draw(self.surf, self.font_big)

            # action buttons
            ax = qx + 200
            higher = game.higher_bid(game.pick_q, game.pick_v)
            bid_btn = Button((ax, py, 150, PICK_DIE), "RAISE", GREEN, enabled=higher)
            self.buttons["raise"] = bid_btn
            bid_btn.draw(self.surf, self.font)
            can_challenge = game.bidder is not None
            ch_btn = Button((ax + 166, py, 150, PICK_DIE), "CHALLENGE", RED,
                            enabled=can_challenge)
            self.buttons["challenge"] = ch_btn
            ch_btn.draw(self.surf, self.font)

        elif game.phase in ("reveal", "round_over"):
            cont = Button((WIDTH // 2 - 110, base_y + 6, 220, PICK_DIE),
                          "CONTINUE", GOLD_DK)
            self.buttons["continue"] = cont
            cont.draw(self.surf, self.font)

        elif game.phase == "intro":
            roll = Button((WIDTH // 2 - 110, base_y + 6, 220, PICK_DIE),
                          "ROLL!", GREEN)
            self.buttons["roll"] = roll
            roll.draw(self.surf, self.font)

        elif game.phase == "game_over":
            again = Button((WIDTH // 2 - 110, base_y + 6, 220, PICK_DIE),
                           "PLAY AGAIN", GREEN)
            self.buttons["again"] = again
            again.draw(self.surf, self.font)

    def draw(self, game, reveal=False):
        self.draw_table()
        # title
        self.surf.blit(self.art["skull"], (WIDTH // 2 - 150, 12))
        self.text("LIAR'S DICE", (WIDTH // 2, 34), self.font_big, GOLD, center=True)
        self.surf.blit(self.art["coin"], (WIDTH // 2 + 110, 16))

        # bots across the top, human along the bottom
        bot_rects = [
            (40, 90, 280, 150),
            (WIDTH // 2 - 140, 90, 280, 150),
            (WIDTH - 320, 90, 280, 150),
        ]
        bots = [p for p in game.players if p.is_bot]
        for p, r in zip(bots, bot_rects):
            self.draw_player(game, p, r, reveal or game.phase in ("reveal", "game_over"))

        self.draw_player(game, game.human,
                         (WIDTH // 2 - 200, 382, 400, 150),
                         reveal or game.phase in ("reveal", "game_over"))

        self.draw_bid_banner(game)

        if game.phase == "game_over":
            self.draw_game_over(game)
        else:
            self.draw_message(game)
            self.draw_controls(game)

    def draw_game_over(self, game):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.surf.blit(overlay, (0, 0))
        won = game.winner is game.human
        self.surf.blit(self.art["chest"] if won else self.art["skull_big"],
                       (WIDTH // 2 - 80, 230))
        msg = "YOU WIN!" if won else "GAME OVER"
        self.text(msg, (WIDTH // 2, 200), self.font_big,
                  GOLD if won else RED, center=True)
        self.text(game.message, (WIDTH // 2, 420), self.font, PARCHMENT, center=True)
        self.draw_controls(game)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def handle_click(game, ui, pos):
    for key, btn in ui.buttons.items():
        if not btn.hit(pos):
            continue
        if key == "roll":
            starter = random.choice(game.alive())
            game.start_round(starter)
            if starter is game.human:
                game.message = "You go first! Make the opening bid."
        elif key.startswith("v"):
            game.pick_v = int(key[1:])
        elif key == "q+":
            game.pick_q = min(game.dice_in_play, game.pick_q + 1)
        elif key == "q-":
            game.pick_q = max(1, game.pick_q - 1)
        elif key == "raise":
            if game.higher_bid(game.pick_q, game.pick_v):
                game.apply_raise(game.human, game.pick_q, game.pick_v)
        elif key == "challenge":
            if game.bidder is not None:
                game.apply_challenge(game.human)
        elif key == "continue":
            game.resolve_round()
        elif key == "again":
            game.__init__(game.human.name)
        return


def update_bots(game, dt):
    """Give the bots a short 'thinking' pause, then let them act."""
    if game.phase != "bot_think":
        return
    game.bot_timer = getattr(game, "bot_timer", 0) + dt
    if game.bot_timer < 850:
        return
    game.bot_timer = 0
    bot = game.current
    action, q, v = game.bot_decide(bot)
    if action == "challenge":
        game.apply_challenge(bot)
    else:
        game.apply_raise(bot, q, v)


def render_once(player_name="You"):
    """Build a representative mid-game frame and save it to a PNG. Used for
    headless previews/screenshots (set LIARS_DICE_SHOT=path)."""
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    surf = pygame.display.set_mode((WIDTH, HEIGHT))
    art = load_assets()
    ui = UI(surf, art)
    game = Game(player_name)
    game.start_round(game.human)
    # Pretend a bot already made a standing bid and it's now the human's turn,
    # so the preview shows the full RAISE / CHALLENGE control panel.
    game.bid_q, game.bid_v, game.bidder = 3, 4, game.players[1]
    game.current, game.phase = game.human, "human"
    game.pick_v, game.pick_q = 5, 4
    game.message = "Your turn! RAISE the bid or CHALLENGE Bot 1."
    ui.draw(game)
    out = os.environ.get("LIARS_DICE_SHOT", "preview.png")
    pygame.image.save(surf, out)
    print("Saved preview to", out)


def main():
    if os.environ.get("LIARS_DICE_SHOT"):
        render_once()
        return

    pygame.init()
    pygame.display.set_caption("Liar's Dice")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    art = load_assets()
    ui = UI(screen, art)
    game = Game("You")

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_click(game, ui, event.pos)
        update_bots(game, dt)
        ui.draw(game)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
