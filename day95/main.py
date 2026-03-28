"""
Space Invaders–style game (pygame).
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass

import pygame


# ------------------------------ CONFIG ------------------------------ #
SCREEN_W = 800
SCREEN_H = 640
FPS = 60

PLAYER_SPEED = 7
BULLET_SPEED = 12
ALIEN_BULLET_SPEED = 5
ALIEN_DROP = 18
ALIEN_BASE_SPEED = 1.2
ALIEN_SPEEDUP_PER_KILL = 0.04
ALIEN_SHOOT_INTERVAL_MS = 900

PLAYER_LIVES = 3
ALIEN_ROWS = 5
ALIEN_COLS = 11
ALIEN_W = 36
ALIEN_H = 26
ALIEN_PAD_X = 12
ALIEN_PAD_Y = 10
ALIEN_START_Y = 80

SHIELD_BLOCK = 8
SHIELD_ROWS = 3
SHIELD_COLS = 5

BLACK = (10, 10, 18)
WHITE = (240, 240, 245)
GREEN = (80, 255, 120)
RED = (255, 70, 90)
CYAN = (100, 220, 255)
YELLOW = (255, 230, 80)
ALIEN_COLOR_1 = (180, 255, 140)
ALIEN_COLOR_2 = (120, 220, 100)


# ------------------------------ ENTITIES ------------------------------ #
@dataclass
class Bullet:
    rect: pygame.Rect
    dy: int
    from_player: bool


@dataclass
class ShieldBlock:
    rect: pygame.Rect
    hits: int = 2


def build_shields() -> list[ShieldBlock]:
    blocks: list[ShieldBlock] = []
    gap = SCREEN_W // 4
    base_y = SCREEN_H - 160
    for i in range(4):
        cx = gap * i + gap // 2 - (SHIELD_COLS * SHIELD_BLOCK) // 2
        for row in range(SHIELD_ROWS):
            for col in range(SHIELD_COLS):
                # Skip corners for a classic “bunker” shape
                if (row == SHIELD_ROWS - 1) and (col == 0 or col == SHIELD_COLS - 1):
                    continue
                x = cx + col * SHIELD_BLOCK
                y = base_y + row * SHIELD_BLOCK
                blocks.append(ShieldBlock(pygame.Rect(x, y, SHIELD_BLOCK - 1, SHIELD_BLOCK - 1)))
    return blocks


def spawn_aliens() -> list[pygame.Rect]:
    aliens: list[pygame.Rect] = []
    total_w = ALIEN_COLS * (ALIEN_W + ALIEN_PAD_X) - ALIEN_PAD_X
    start_x = (SCREEN_W - total_w) // 2
    for row in range(ALIEN_ROWS):
        for col in range(ALIEN_COLS):
            x = start_x + col * (ALIEN_W + ALIEN_PAD_X)
            y = ALIEN_START_Y + row * (ALIEN_H + ALIEN_PAD_Y)
            aliens.append(pygame.Rect(x, y, ALIEN_W, ALIEN_H))
    return aliens


def alien_color(row: int) -> tuple[int, int, int]:
    return ALIEN_COLOR_1 if row % 2 == 0 else ALIEN_COLOR_2


def draw_alien(surf: pygame.Surface, rect: pygame.Rect, row: int) -> None:
    c = alien_color(row)
    pygame.draw.rect(surf, c, rect)
    pygame.draw.rect(surf, (40, 80, 40), rect, 1)
    # Simple “invader” detail
    eye = rect.inflate(-20, -12)
    pygame.draw.rect(surf, BLACK, eye)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Space Invaders — ← → move, Space fire, R restart, Esc quit")
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small = pygame.font.Font(None, 24)

    player = pygame.Rect(SCREEN_W // 2 - 24, SCREEN_H - 48, 48, 22)
    aliens = spawn_aliens()
    alien_dir = 1
    alien_speed = ALIEN_BASE_SPEED
    bullets: list[Bullet] = []
    shields = build_shields()

    score = 0
    lives = PLAYER_LIVES
    game_over = False
    win = False
    last_shot = 0
    alien_shoot_accum = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and (game_over or win):
                    # Restart
                    player = pygame.Rect(SCREEN_W // 2 - 24, SCREEN_H - 48, 48, 22)
                    aliens = spawn_aliens()
                    alien_dir = 1
                    alien_speed = ALIEN_BASE_SPEED
                    bullets.clear()
                    shields = build_shields()
                    score = 0
                    lives = PLAYER_LIVES
                    game_over = False
                    win = False
                    last_shot = 0
                if not game_over and not win and event.key == pygame.K_SPACE:
                    if now - last_shot > 350:
                        bullets.append(
                            Bullet(
                                pygame.Rect(player.centerx - 2, player.top - 8, 4, 12),
                                -BULLET_SPEED,
                                True,
                            )
                        )
                        last_shot = now

        keys = pygame.key.get_pressed()
        if not game_over and not win:
            if keys[pygame.K_LEFT]:
                player.x = max(0, player.x - PLAYER_SPEED)
            if keys[pygame.K_RIGHT]:
                player.x = min(SCREEN_W - player.width, player.x + PLAYER_SPEED)

            # Alien movement
            if aliens:
                step = alien_dir * alien_speed
                hit_edge = any(
                    a.x + step < 0 or a.x + a.width + step > SCREEN_W for a in aliens
                )
                if hit_edge:
                    alien_dir *= -1
                    for a in aliens:
                        a.y += ALIEN_DROP
                    if any(a.bottom >= player.top - 10 for a in aliens):
                        game_over = True
                else:
                    for a in aliens:
                        a.x += step

                alien_shoot_accum += dt
                while alien_shoot_accum >= ALIEN_SHOOT_INTERVAL_MS:
                    alien_shoot_accum -= ALIEN_SHOOT_INTERVAL_MS
                    bottom_y = max(a.y for a in aliens)
                    bottom_aliens = [a for a in aliens if a.y == bottom_y]
                    if bottom_aliens:
                        shooter = random.choice(bottom_aliens)
                        bullets.append(
                            Bullet(
                                pygame.Rect(shooter.centerx - 2, shooter.bottom, 4, 10),
                                ALIEN_BULLET_SPEED,
                                False,
                            )
                        )

            # Bullets
            for b in bullets[:]:
                b.rect.y += b.dy
                if b.rect.bottom < 0 or b.rect.top > SCREEN_H:
                    bullets.remove(b)
                    continue
                # Player bullet vs aliens
                if b.from_player:
                    hit = b.rect.collidelist(aliens)
                    if hit != -1:
                        alien = aliens.pop(hit)
                        bullets.remove(b)
                        row = (alien.y - ALIEN_START_Y) // (ALIEN_H + ALIEN_PAD_Y)
                        row = max(0, min(ALIEN_ROWS - 1, row))
                        score += 10 * (ALIEN_ROWS - row)
                        alien_speed += ALIEN_SPEEDUP_PER_KILL
                        continue
                    # Shields
                    for blk in shields[:]:
                        if b.rect.colliderect(blk.rect):
                            blk.hits -= 1
                            bullets.remove(b)
                            if blk.hits <= 0:
                                shields.remove(blk)
                            break
                else:
                    if b.rect.colliderect(player):
                        bullets.remove(b)
                        lives -= 1
                        if lives <= 0:
                            game_over = True
                    else:
                        for blk in shields[:]:
                            if b.rect.colliderect(blk.rect):
                                blk.hits -= 1
                                bullets.remove(b)
                                if blk.hits <= 0:
                                    shields.remove(blk)
                                break

            if not aliens:
                win = True

        # Draw
        screen.fill(BLACK)
        pygame.draw.rect(screen, (30, 30, 50), (0, SCREEN_H - 36, SCREEN_W, 36))

        for blk in shields:
            shade = 80 + blk.hits * 60
            pygame.draw.rect(screen, (shade, shade, 120), blk.rect)

        for i, a in enumerate(aliens):
            row = i // ALIEN_COLS
            draw_alien(screen, a, row)

        pygame.draw.polygon(
            screen,
            CYAN,
            [
                (player.centerx, player.top),
                (player.right, player.bottom),
                (player.left, player.bottom),
            ],
        )

        for b in bullets:
            color = YELLOW if b.from_player else RED
            pygame.draw.rect(screen, color, b.rect)

        hud = f"Score: {score}    Lives: {lives}"
        screen.blit(font.render(hud, True, WHITE), (16, 12))

        if game_over:
            screen.blit(
                font.render("GAME OVER — R to restart", True, RED),
                (SCREEN_W // 2 - 200, SCREEN_H // 2 - 20),
            )
        elif win:
            screen.blit(
                font.render("YOU WIN — R to restart", True, GREEN),
                (SCREEN_W // 2 - 180, SCREEN_H // 2 - 20),
            )
        else:
            screen.blit(small.render("← → move   Space fire   Esc quit", True, (150, 150, 170)), (16, SCREEN_H - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
