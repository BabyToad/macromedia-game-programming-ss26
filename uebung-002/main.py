import pygame

# ---- Bildschirm ----
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# ---- Farben (Rot, Grün, Blau, [Alpha]) ----
BACKGROUND_COL = (20, 100, 200)
GROUND_COL = (80, 70, 30)
PLAYER_COL = (30, 210, 76)
CIRCLE_COL = (200, 200, 255)
TEXT_COL = (255, 255, 255)

# ---- pygame starten ----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump & Run")
clock = pygame.time.Clock()

# ---- Player ----
player_x = 100.0
player_y = 100.0
player_radius = 20
player_moving_left = False
player_moving_right = False
player_movement_y = 0
gravity = 0.1

# ---- Bouncing circle (aus dem "Boing boing"-Beispiel) ----
circle_x = 300.0
circle_y = 50.0
circle_radius = 10
circle_movement_x = 1.0
circle_movement_y = 0.0
gravity = 0.1

# ---- Obstacles (Boden + Plattformen) ----
# Jedes Obstacle ist ein pygame.Rect(x, y, breite, hoehe)
obstacles = []

# Boden
obstacles.append(pygame.Rect(5, SCREEN_HEIGHT - 10, SCREEN_WIDTH - 10, 10))

# Plattform 001
obstacles.append(pygame.Rect(200, SCREEN_HEIGHT - 60, 200, 10))

# ---- Status-Text ----
status = "Wheee!"

# ============================================================
# Game Loop
# ============================================================

running = True
while running:

    # ---- Events ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_moving_left = True
            elif event.key == pygame.K_d:
                player_moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_moving_left = False
            elif event.key == pygame.K_d:
                player_moving_right = False

    # ---- Update ----

    # Player-Bewegung
    if player_moving_right:
        player_x += 3
    elif player_moving_left:
        player_x -= 3

   # Player: Gravitation
    player_movement_y += gravity
    player_y += player_movement_y

    # Bouncing circle: Gravitation + Bewegung
    circle_movement_y += gravity
    circle_x += circle_movement_x
    circle_y += circle_movement_y

    # Bouncing circle: Am Boden abprallen
    if circle_y >= SCREEN_HEIGHT - 20 - circle_radius:
        circle_movement_y = -circle_movement_y

    # Bouncing circle: An den Seiten abprallen
    if circle_x <= circle_radius or circle_x >= SCREEN_WIDTH - circle_radius:
        circle_movement_x = -circle_movement_x

    # ---- Draw ----
    screen.fill(BACKGROUND_COL)

    # Obstacles zeichnen
    for obs in obstacles:
        pygame.draw.rect(screen, GROUND_COL, obs)

    # Bouncing circle zeichnen
    pygame.draw.circle(screen, CIRCLE_COL, (int(circle_x), int(circle_y)), circle_radius)

    # Player zeichnen
    pygame.draw.circle(screen, PLAYER_COL, (int(player_x), int(player_y)), player_radius)

    # Text zeichnen
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(status, True, TEXT_COL)
    screen.blit(text_surface, (30, 30))

    # ---- Flip ----
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
