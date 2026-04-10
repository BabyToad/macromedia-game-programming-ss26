# enemy.py
# STUBBED enemy class. Students will implement AI, drawing, and collision.

import pygame
from entity import Entity


class Enemy(Entity):
    """STUB: Enemy entity. Has fields but no real behavior yet.

    Students should implement:
    - step(target): move toward target
    - draw(): render the enemy
    - Collision with player shots
    - Spawning from level data
    """

    def __init__(self):
        super().__init__()
        self.damage = 0             # Damage dealt to player on contact
        self.starting_point = 0     # Spawn frame (when in the level duration)
        self.ready = False          # Whether the enemy has been activated
        self.alive = True           # Whether the enemy is still alive

    # ------------------------------------------------------------------ #
    #  setup — initialize enemy (extends Entity.setup)                   #
    # ------------------------------------------------------------------ #
    def setup(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        image_prefix: str,
        anim_speed: int,
        hp: int,
        damage: int = 1,
    ):
        """Initialize enemy with position, images, and damage."""
        super().setup(x, y, dx, dy, image_prefix, anim_speed, hp)
        self.damage = damage
        self.ready = False
        self.alive = True

    # ------------------------------------------------------------------ #
    #  step — STUB: calculates direction toward target but doesn't move  #
    # ------------------------------------------------------------------ #
    def step(self, target_pos: pygame.Vector2):
        """STUB: Calculate direction toward target.
        The C++ version computes the vector but doesn't apply it.
        Students should implement actual movement here."""
        if self.alive:
            # Calculate direction toward target (not applied — stub)
            direction = target_pos - self.pos
            # TODO: Normalize direction, apply speed, move toward target

    # ------------------------------------------------------------------ #
    #  is_alive — check if enemy HP is above 0 (latches to dead)        #
    # ------------------------------------------------------------------ #
    def is_alive(self) -> bool:
        """Return True if the enemy is alive. Once HP drops to 0,
        alive is permanently set to False (mirrors C++ behavior)."""
        if self.hp <= 0:
            self.alive = False
        return self.alive
