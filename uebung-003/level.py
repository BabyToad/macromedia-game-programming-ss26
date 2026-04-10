# level.py
# Level loader and manager. Parses .rfg level files, holds enemies and
# obstacles, draws background.

import os
import re
import pygame
from entity import Entity
from enemy import Enemy
from obstacle import Obstacle
from settings import ASSET_DIR, SCREEN_WIDTH, SCREEN_HEIGHT


class Level(Entity):
    """Loads and manages a level from a .rfg file.

    Parses enemies, obstacles, background image, and metadata.
    In this skeleton, step() is empty (no scrolling, no enemy spawning).
    """

    def __init__(self):
        super().__init__()
        self.enemies: list[Enemy] = []
        self.obstacles: list[Obstacle] = []
        self.background_image: pygame.Surface | None = None

        self.num_tracks = 0          # Number of tracks (columns)
        self.duration = 0            # Level duration in frames
        self.music_name = ""         # Background music filename (not loaded)

        # Raw level data storage (2D array, matching C++ structure)
        self.level_data: list[list[int]] = []

    # ------------------------------------------------------------------ #
    #  load — parse a .rfg level file                                    #
    # ------------------------------------------------------------------ #
    def load(self, filename: str):
        """Parse a .rfg level file and populate enemies, obstacles, etc."""
        filepath = os.path.join(ASSET_DIR, filename)

        # Initial level movement — scrolls downward (mirrors C++ dir.set(0, 1))
        self.pos = pygame.Vector2(0, 0)
        self.dir = pygame.Vector2(0, 1)

        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Level config line: L T(2) B(background.png) M(music) D(2000)
                if line.startswith("L "):
                    self._parse_level_line(line)

                # Enemy line: E D(1) S(1) A(enemy) N(5) T(0) P(100)
                elif line.startswith("E "):
                    self._parse_enemy_line(line)

                # Obstacle line: O T(0) D(100) L(100) C(35,56,90) W(5)
                elif line.startswith("O "):
                    self._parse_obstacle_line(line)

    # ------------------------------------------------------------------ #
    #  step — EMPTY in skeleton (no scrolling, no enemy spawning)        #
    # ------------------------------------------------------------------ #
    def step(self):
        """Per-frame update. Empty in the skeleton — no scrolling or
        enemy spawning. Students implement this in Uebung 003."""
        pass

    # ------------------------------------------------------------------ #
    #  draw — render background image                                    #
    # ------------------------------------------------------------------ #
    def draw(self, screen: pygame.Surface):
        """Draw the background image at the level's position."""
        if self.background_image:
            screen.blit(self.background_image, (int(self.pos.x), int(self.pos.y)))

    # ================================================================== #
    #  Private parsing helpers                                           #
    # ================================================================== #

    def _parse_param(self, text: str, key: str) -> str | None:
        """Extract value from a parameter like T(2) or B(background.png)."""
        match = re.search(rf"{key}\(([^)]*)\)", text)
        return match.group(1) if match else None

    def _parse_level_line(self, line: str):
        """Parse: L T(2) B(background.png) M(Backgnd001music) D(2000)"""
        # Number of tracks
        val = self._parse_param(line, "T")
        if val:
            self.num_tracks = int(val)

        # Background image
        val = self._parse_param(line, "B")
        if val:
            bg_name = val
            # If the filename doesn't already have an extension, add .png
            if not os.path.splitext(bg_name)[1]:
                bg_name += ".png"
            bg_path = os.path.join(ASSET_DIR, bg_name)
            try:
                self.background_image = pygame.image.load(bg_path).convert()
            except pygame.error:
                print(f"Warning: could not load background {bg_path}")

        # Music (stored but not loaded in skeleton)
        val = self._parse_param(line, "M")
        if val:
            self.music_name = val

        # Duration
        val = self._parse_param(line, "D")
        if val:
            self.duration = int(val)

        # Initialize level_data 2D array (num_tracks x duration)
        # Mirrors C++ level_data[track][frame] structure
        if self.num_tracks > 0 and self.duration > 0:
            self.level_data = [
                [0] * self.duration for _ in range(self.num_tracks)
            ]

        # Position background so bottom aligns with bottom of screen
        # Mirrors C++: pos.y = -background_image.getHeight() + SCREEN_HEIGHT
        if self.background_image:
            self.pos.y = -self.background_image.get_height() + SCREEN_HEIGHT

    def _parse_enemy_line(self, line: str):
        """Parse: E D(1) S(1) A(enemy) N(5) T(0) P(100)
        STUB: Parses the line but does NOT create enemies yet.
        Students implement enemy creation and spawning in Uebung 003."""
        # Values are parsed but not used — mirrors C++ skeleton behavior
        damage = int(self._parse_param(line, "D") or 1)
        speed = int(self._parse_param(line, "S") or 1)
        anim_prefix = self._parse_param(line, "A") or "enemy"
        count = int(self._parse_param(line, "N") or 1)
        track = int(self._parse_param(line, "T") or 0)
        position = int(self._parse_param(line, "P") or 0)
        # TODO: Students create and store Enemy objects here

    def _parse_obstacle_line(self, line: str):
        """Parse: O T(0) D(100) L(100) C(35,56,90) W(5)
        Creates Obstacle objects (not drawn or collision-checked)."""
        track = int(self._parse_param(line, "T") or 0)
        duration_start = int(self._parse_param(line, "D") or 0)
        length = int(self._parse_param(line, "L") or 0)
        width = int(self._parse_param(line, "W") or 5)

        # Parse color: C(R,G,B)
        color_str = self._parse_param(line, "C") or "255,255,255"
        color_parts = color_str.split(",")
        color = (
            int(color_parts[0]),
            int(color_parts[1]),
            int(color_parts[2]),
        )

        obstacle = Obstacle(
            track=track,
            duration_start=duration_start,
            length=length,
            color=color,
            width=width,
        )

        # Compute screen coordinates
        # X position: centered on the border between track and track+1
        # Y position: placed relative to the screen using duration as a
        # pixel offset from the top (students may adjust when adding scrolling)
        if self.num_tracks > 0:
            track_width = SCREEN_WIDTH // self.num_tracks
            obstacle_x = track_width * (track + 1)
            obstacle.x1 = obstacle_x - width // 2
            obstacle.x2 = obstacle_x + width // 2
            obstacle.y1 = duration_start
            obstacle.y2 = duration_start + length

        self.obstacles.append(obstacle)
