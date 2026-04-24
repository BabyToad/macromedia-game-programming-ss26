"""
Mario Jump Playground — procedural PyGame-CE reference.

A tunable 2D platformer sandbox where every 'game feel' trick can be
toggled independently. Companion to the web playground shown in class.

The teaching point:
    Real physics feels terrible.
    Modern platformers stack half a dozen cheats to feel good.
    Each cheat is a boolean flag plus a few lines of code.

Run it:
    uv sync
    uv run main.py

Controls (in-game):
    A / D or ← / →        move
    Space / W / ↑         jump  (variable height if toggle on)
    S / ↓                 fast fall
    R                     reset
    1 … 7                 toggle each trick (see overlay, press H)
    H                     toggle the help overlay
    G                     toggle the velocity/accel graph strip
    [  /  ]               decrease / increase gravity
    -  /  =               decrease / increase jump strength

Everything below is ONE FILE, in the procedural style you already know
from Unit 02. No classes. No magic. Read top-to-bottom.
"""

import pygame
from collections import deque


# ============================================================================
# Window + world
# ============================================================================
SCREEN_W, SCREEN_H = 1200, 680         # window size
WORLD_H = 540                           # world occupies the top chunk
GRAPH_H = SCREEN_H - WORLD_H            # graph strip at the bottom
FPS = 60

# Level layout. Each tuple is (x, y, width, height) in pixels.
# These match the web playground exactly so the feel transfers.
PLATFORMS = [
    (0,    470, 340, 70),    # start
    (420,  470, 200, 70),    # after a gap (tests jump distance)
    (680,  420, 160, 120),   # step up
    (880,  350, 100, 190),   # tall step
    (1040, 470, 160, 70),    # end plateau (ledge on left tests coyote)
    (920,  280,  80,  16),   # floating — only reachable with hangtime
]

PLAYER_W, PLAYER_H = 42, 54

# ============================================================================
# Trick-tuning constants
# ============================================================================
# Frame counts at 60 FPS. 1 frame ≈ 16.7 ms.
COYOTE_FRAMES   = 7     # ~120 ms after leaving a ledge
BUFFER_FRAMES   = 8     # ~130 ms before landing

# How aggressively variable-jump-height cuts an interrupted rise.
# 0.0 = tap becomes an instant stop (too sharp)
# 0.35 = responsive, Celeste-ish
# 1.0 = no effect, fully committed jump
VAR_JUMP_CUTOFF = 0.35

# Apex hangtime: if |vy| is below this threshold, apply a reduced gravity.
APEX_THRESHOLD  = 2.2
APEX_FACTOR     = 0.5

# Asymmetric gravity: falling multiplies gravity.
FALL_MULT       = 1.55

# Fast-fall: hold down while airborne and falling.
FAST_FALL_MULT  = 1.9

MAX_FALL_SPEED  = 18    # clamp so the character can't tunnel through walls

# ============================================================================
# Config — mutable at runtime, driven by keyboard toggles + sliders
# ============================================================================
config = {
    # Base physics (change with [ ] - = keys)
    "gravity":       0.65,
    "jump_strength": 13.5,
    "move_speed":    5.0,
    "air_control":   1.0,

    # Toggles (keys 1-7 flip these)
    "realistic":          False,  # flip ON to disable ALL tricks
    "variable_jump":      True,
    "coyote_time":        True,
    "jump_buffer":        True,
    "apex_hang":          True,
    "asymmetric_gravity": True,
    "fast_fall":          True,
}

TRICK_KEYS = [
    "variable_jump", "coyote_time", "jump_buffer",
    "apex_hang", "asymmetric_gravity", "fast_fall",
]

# ============================================================================
# State
# ============================================================================
# Using dicts instead of classes keeps us inside what you know so far.
# By Unit 6 you'll learn why a class makes this cleaner.
player = {
    "x":      80.0,
    "y":      470.0 - PLAYER_H,
    "vx":     0.0,
    "vy":     0.0,
    "facing": 1,       # 1 right, -1 left
    "squash": 1.0,     # 1 = normal, <1 flat, >1 stretched
}

state = {
    "on_ground":              False,
    "coyote":                 0,       # frames remaining in the coyote window
    "buffer":                 0,       # frames remaining in the jump buffer
    "current_gravity":        0.65,    # effective gravity this frame
    "jump_pressed_this_tick": False,   # set once on keydown
    "released_during_rise":   False,   # set once on keyup while vy < 0
}

# History buffers for the graph strip — 4 seconds at 60 FPS.
HIST_LEN = 240
hist = {
    "y":  deque([player["y"]] * HIST_LEN, maxlen=HIST_LEN),
    "vy": deque([0.0]         * HIST_LEN, maxlen=HIST_LEN),
    "ay": deque([config["gravity"]] * HIST_LEN, maxlen=HIST_LEN),
}


def reset():
    """Return player to the start, zero all state, clear history."""
    player["x"], player["y"] = 80.0, 470.0 - PLAYER_H
    player["vx"] = player["vy"] = 0.0
    player["facing"] = 1
    player["squash"] = 1.0
    state["on_ground"] = False
    state["coyote"]    = 0
    state["buffer"]    = 0
    state["released_during_rise"] = False
    hist["y"].clear();  hist["y"] .extend([player["y"]] * HIST_LEN)
    hist["vy"].clear(); hist["vy"].extend([0.0]        * HIST_LEN)
    hist["ay"].clear(); hist["ay"].extend([config["gravity"]] * HIST_LEN)


# ============================================================================
# Helpers
# ============================================================================
def rect_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    """AABB overlap test. Two rectangles intersect if they overlap on both axes."""
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def lerp(a, b, t):
    """Linear interpolation. t=0 → a, t=1 → b."""
    return a + (b - a) * t


def sign(v):
    return 1 if v > 0 else (-1 if v < 0 else 0)


# ============================================================================
# Update — one physics step
# This is where every trick lives. Read top to bottom.
# ============================================================================
def update(keys, jump_pressed, jump_released):
    # ---- 1) Horizontal input ----
    want_vx = 0.0
    if keys[pygame.K_LEFT]  or keys[pygame.K_a]:  want_vx -= config["move_speed"]
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  want_vx += config["move_speed"]

    # Air control fraction: 1.0 on ground, config value airborne.
    ctl = 1.0 if state["on_ground"] else config["air_control"]
    player["vx"] = lerp(player["vx"], want_vx, min(1.0, 0.3 * ctl))
    if abs(want_vx) > 0.2:
        player["facing"] = sign(want_vx)

    # ---- 2) Jump buffer ----
    # When you press jump, we 'arm' the buffer for BUFFER_FRAMES frames.
    # If you land or enter the coyote window while it's armed, we jump.
    if jump_pressed:
        state["buffer"] = BUFFER_FRAMES if config["jump_buffer"] else 1
    state["buffer"] = max(0, state["buffer"] - 1)

    # ---- 3) Fire jump if buffered AND (on ground OR in coyote window) ----
    can_jump = state["on_ground"] or (config["coyote_time"] and state["coyote"] > 0)
    if state["buffer"] > 0 and can_jump:
        player["vy"]   = -config["jump_strength"]
        state["buffer"] = 0
        state["coyote"] = 0
        state["on_ground"] = False
        state["released_during_rise"] = False
        player["squash"] = 1.2   # launch stretch

    # ---- 4) Variable jump height ----
    # Release the jump key while still rising → clip the upward velocity.
    if config["variable_jump"] and state["released_during_rise"] and player["vy"] < 0:
        player["vy"] *= VAR_JUMP_CUTOFF
        state["released_during_rise"] = False
    if not keys[pygame.K_SPACE] and not keys[pygame.K_w] and not keys[pygame.K_UP]:
        state["released_during_rise"] = False

    # ---- 5) Gravity with modifiers ----
    g = config["gravity"]
    tricks_on = not config["realistic"]
    if tricks_on and config["apex_hang"] and abs(player["vy"]) < APEX_THRESHOLD:
        g *= APEX_FACTOR                    # floaty peak
    if tricks_on and config["asymmetric_gravity"] and player["vy"] > 0:
        g *= FALL_MULT                       # fall faster than rise
    if tricks_on and config["fast_fall"] and (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player["vy"] > 0:
        g *= FAST_FALL_MULT                  # hold down to slam
    state["current_gravity"] = g
    player["vy"] += g
    if player["vy"] > MAX_FALL_SPEED:
        player["vy"] = MAX_FALL_SPEED

    # ---- 6) X movement + collision ----
    # Move, then check overlap for every platform, then push out.
    # One axis at a time is what gives clean corner behavior.
    player["x"] += player["vx"]
    for (px, py, pw, ph) in PLATFORMS:
        if rect_overlap(player["x"], player["y"], PLAYER_W, PLAYER_H, px, py, pw, ph):
            if player["vx"] > 0:    player["x"] = px - PLAYER_W
            elif player["vx"] < 0:  player["x"] = px + pw
            player["vx"] = 0

    # ---- 7) Y movement + collision ----
    was_on_ground = state["on_ground"]
    state["on_ground"] = False
    player["y"] += player["vy"]
    for (px, py, pw, ph) in PLATFORMS:
        if rect_overlap(player["x"], player["y"], PLAYER_W, PLAYER_H, px, py, pw, ph):
            if player["vy"] > 0:
                player["y"] = py - PLAYER_H
                state["on_ground"] = True
                # Landing squash — flatter when impact is harder.
                if not was_on_ground:
                    impact = min(1.0, player["vy"] / 16.0)
                    player["squash"] = lerp(1.0, 0.7, impact)
            elif player["vy"] < 0:
                player["y"] = py + ph
            player["vy"] = 0

    # ---- 8) Coyote timer ----
    # Arms the moment you walk off a ledge — only if you didn't jump.
    if was_on_ground and not state["on_ground"] and player["vy"] >= 0:
        state["coyote"] = COYOTE_FRAMES
    elif state["coyote"] > 0 and not state["on_ground"]:
        state["coyote"] = max(0, state["coyote"] - 1)
    elif state["on_ground"]:
        state["coyote"] = 0

    # ---- 9) Recover squash, clamp world ----
    player["squash"] = lerp(player["squash"], 1.0, 0.2)
    if player["y"] > WORLD_H + 200 or player["x"] < -300 or player["x"] > SCREEN_W + 300:
        reset()

    # ---- 10) History for graphs ----
    hist["y"].append(player["y"])
    hist["vy"].append(player["vy"])
    hist["ay"].append(state["current_gravity"])


# ============================================================================
# Rendering
# ============================================================================
COL_SKY_TOP  = (16, 19, 26)
COL_SKY_BOT  = (42, 31, 26)
COL_STAR     = (240, 232, 210)
COL_PLAT     = (183, 131, 99)
COL_PLAT_TOP = (241, 197, 145)
COL_PLAT_DARK= (138,  90,  58)
COL_PLAYER   = (217, 119,  87)
COL_EYE_WHITE= (255, 230, 212)
COL_EYE_DARK = (17,  17,  17)
COL_HUD      = (255, 230, 212)
COL_ACCENT   = (255, 107,  53)
COL_TEAL     = (127, 209, 200)
COL_GREEN    = (152, 195, 121)
COL_BLUE     = (111, 179, 210)
COL_MUTED    = (136, 146, 163)

# Pre-generated "stars" for the sky, so they don't flicker each frame.
import random
_rng = random.Random(7)
STARS = [(_rng.randint(0, SCREEN_W), _rng.randint(0, WORLD_H // 2)) for _ in range(40)]


def draw_sky(screen):
    # Vertical gradient, hand-rolled without numpy.
    for y in range(WORLD_H):
        t = y / WORLD_H
        r = int(lerp(COL_SKY_TOP[0], COL_SKY_BOT[0], t))
        g = int(lerp(COL_SKY_TOP[1], COL_SKY_BOT[1], t))
        b = int(lerp(COL_SKY_TOP[2], COL_SKY_BOT[2], t))
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_W, y))
    for (sx, sy) in STARS:
        screen.set_at((sx, sy), COL_STAR)


def draw_platforms(screen):
    for (px, py, pw, ph) in PLATFORMS:
        pygame.draw.rect(screen, COL_PLAT,     (px, py, pw, ph))
        pygame.draw.rect(screen, COL_PLAT_TOP, (px, py, pw, 5))
        pygame.draw.rect(screen, COL_PLAT_DARK,(px, py + 5, pw, 2))


def draw_player(screen):
    cx = int(player["x"] + PLAYER_W / 2)
    by = int(player["y"] + PLAYER_H)

    # Squash/stretch. squash<1 → wider+shorter (landing); >1 → taller+narrower (launch).
    stretch_y = player["squash"]
    stretch_x = 1.0 / player["squash"]
    if not state["on_ground"]:
        air = max(-0.15, min(0.22, -player["vy"] / 80))
        stretch_y *= 1 + air
        stretch_x *= 1 - air * 0.6

    bw = int(PLAYER_W * stretch_x)
    bh = int(PLAYER_H * stretch_y)
    top_left = (cx - bw // 2, by - bh)

    # Body: rounded-rect (pygame doesn't have rounded rects, cheat with circle + rect)
    pygame.draw.rect(screen, COL_PLAYER, (*top_left, bw, bh), border_radius=min(bw, bh) // 2)

    # Eyes
    eye_r  = max(2, bw // 9)
    eye_y  = top_left[1] + bh // 2 - 2
    eye_dx = bw // 5
    for ex in (cx - eye_dx, cx + eye_dx):
        pygame.draw.circle(screen, COL_EYE_WHITE, (ex, eye_y), eye_r + 1)
        pygame.draw.circle(screen, COL_EYE_DARK,  (ex, eye_y), max(2, eye_r - 1))


def draw_graphs(screen):
    y0 = WORLD_H
    pad = 12
    col_gap = 12
    cols = 3
    col_w = (SCREEN_W - pad * 2 - col_gap * (cols - 1)) // cols
    col_h = GRAPH_H - pad * 2

    pygame.draw.rect(screen, (11, 13, 16), (0, y0, SCREEN_W, GRAPH_H))
    pygame.draw.line(screen, (255, 255, 255, 64), (0, y0), (SCREEN_W, y0), 1)

    series = [
        ("y (position)",  hist["y"],  COL_BLUE,   0,   WORLD_H, True,  False),
        ("vy (velocity)", hist["vy"], COL_ACCENT, -22, 22,      False, True),
        ("ay (gravity)",  hist["ay"], COL_GREEN,  0,   3.0,     False, False),
    ]

    for i, (label, data, color, mn, mx, invert, zero_line) in enumerate(series):
        x0 = pad + i * (col_w + col_gap)
        pygame.draw.rect(screen, (255, 255, 255, 10), (x0, y0 + pad, col_w, col_h))
        # Label
        font = pygame.font.SysFont("consolas,monospace", 14)
        label_surf = font.render(label, True, COL_HUD)
        screen.blit(label_surf, (x0 + 6, y0 + pad + 4))

        if zero_line:
            zy = y0 + pad + int(col_h * ((0 - mn) / (mx - mn)))
            pygame.draw.line(screen, (255, 255, 255), (x0, zy), (x0 + col_w, zy), 1)

        # Plot
        pts = []
        for j, v in enumerate(data):
            t = j / (HIST_LEN - 1) if HIST_LEN > 1 else 0
            norm = max(0.0, min(1.0, (v - mn) / (mx - mn) if mx != mn else 0))
            plot_y = norm if invert else (1 - norm)
            pts.append((int(x0 + t * col_w), int(y0 + pad + plot_y * col_h)))
        if len(pts) > 1:
            pygame.draw.lines(screen, color, False, pts, 2)
        # Current-value dot
        if pts:
            pygame.draw.circle(screen, color, pts[-1], 3)


def draw_hud(screen, font, show_help):
    # Top-left live state
    lines = [
        f"vx {player['vx']:+6.2f}  vy {player['vy']:+6.2f}  ay {state['current_gravity']:+5.2f}",
        f"ground {'Y' if state['on_ground'] else ' '}  coyote {state['coyote']}  buffer {state['buffer']}",
    ]
    for i, line in enumerate(lines):
        surf = font.render(line, True, COL_HUD)
        screen.blit(surf, (12, 10 + i * 18))

    # Top-right: active toggles
    active = ", ".join([k for k in TRICK_KEYS if config[k]]) or "NONE (realistic)"
    surf = font.render(f"tricks: {active}", True, COL_MUTED)
    screen.blit(surf, (SCREEN_W - surf.get_width() - 12, 10))

    # Bottom-left: controls hint
    hint = "H help · R reset · 1-7 toggle trick · [  ]  gravity · -  =  jump strength"
    surf = font.render(hint, True, COL_MUTED)
    screen.blit(surf, (12, WORLD_H - 22))

    if show_help:
        draw_help_overlay(screen, font)


def draw_help_overlay(screen, font):
    lines = [
        ("CONTROLS",                   COL_ACCENT),
        ("A/D or ←/→          move",   COL_HUD),
        ("Space / W / ↑       jump",   COL_HUD),
        ("S / ↓               fast fall", COL_HUD),
        ("R                   reset",  COL_HUD),
        ("",                           COL_HUD),
        ("TRICKS (press to toggle)",   COL_ACCENT),
        ("1  variable jump height",    COL_HUD),
        ("2  coyote time",             COL_HUD),
        ("3  jump buffer",             COL_HUD),
        ("4  apex hangtime",           COL_HUD),
        ("5  asymmetric gravity",      COL_HUD),
        ("6  fast fall",               COL_HUD),
        ("7  realistic mode (all off)",COL_HUD),
        ("",                           COL_HUD),
        ("TUNING",                     COL_ACCENT),
        ("[  ]  gravity",              COL_HUD),
        ("-  =  jump strength",        COL_HUD),
        ("G     toggle graphs",        COL_HUD),
        ("H     toggle this help",     COL_HUD),
    ]
    panel_w, panel_h = 420, 470
    panel_x = (SCREEN_W - panel_w) // 2
    panel_y = (WORLD_H - panel_h) // 2
    bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    bg.fill((11, 13, 16, 230))
    screen.blit(bg, (panel_x, panel_y))
    pygame.draw.rect(screen, COL_ACCENT, (panel_x, panel_y, panel_w, panel_h), 2)

    for i, (text, color) in enumerate(lines):
        surf = font.render(text, True, color)
        screen.blit(surf, (panel_x + 24, panel_y + 22 + i * 20))


# ============================================================================
# Main loop
# ============================================================================
def main():
    pygame.init()
    pygame.display.set_caption("Mario Jump Playground — Macromedia GPG")
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas,monospace", 14)

    show_help   = True
    show_graphs = True
    running = True

    while running:
        # ---- events ----
        jump_pressed  = False
        jump_released = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    jump_pressed = True
                elif event.key == pygame.K_r:
                    reset()
                elif event.key == pygame.K_h:
                    show_help = not show_help
                elif event.key == pygame.K_g:
                    show_graphs = not show_graphs
                elif event.key == pygame.K_ESCAPE:
                    running = False
                # Toggle tricks
                elif event.key == pygame.K_1:  config["variable_jump"]      = not config["variable_jump"]
                elif event.key == pygame.K_2:  config["coyote_time"]        = not config["coyote_time"]
                elif event.key == pygame.K_3:  config["jump_buffer"]        = not config["jump_buffer"]
                elif event.key == pygame.K_4:  config["apex_hang"]          = not config["apex_hang"]
                elif event.key == pygame.K_5:  config["asymmetric_gravity"] = not config["asymmetric_gravity"]
                elif event.key == pygame.K_6:  config["fast_fall"]          = not config["fast_fall"]
                elif event.key == pygame.K_7:
                    # Realistic: flip all tricks off together
                    config["realistic"] = not config["realistic"]
                    if config["realistic"]:
                        for k in TRICK_KEYS: config[k] = False
                    else:
                        for k in TRICK_KEYS: config[k] = True
                # Tune gravity / jump
                elif event.key == pygame.K_LEFTBRACKET:  config["gravity"]       = max(0.1, config["gravity"] - 0.05)
                elif event.key == pygame.K_RIGHTBRACKET: config["gravity"]       = min(2.0, config["gravity"] + 0.05)
                elif event.key == pygame.K_MINUS:        config["jump_strength"] = max(5.0, config["jump_strength"] - 0.5)
                elif event.key == pygame.K_EQUALS:       config["jump_strength"] = min(22.0, config["jump_strength"] + 0.5)

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    jump_released = True
                    if player["vy"] < 0:
                        state["released_during_rise"] = True

        # ---- physics step ----
        keys = pygame.key.get_pressed()
        update(keys, jump_pressed, jump_released)

        # ---- render ----
        draw_sky(screen)
        draw_platforms(screen)
        draw_player(screen)
        if show_graphs:
            draw_graphs(screen)
        else:
            pygame.draw.rect(screen, (11, 13, 16), (0, WORLD_H, SCREEN_W, GRAPH_H))
        draw_hud(screen, font, show_help)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
