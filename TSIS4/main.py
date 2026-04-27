# main.py
import pygame
import sys
import json
import os
import db
from game import run_game, WIN_W, WIN_H, SNAKE_COLOR


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR, HUD_BG = (0, 0, 0), (20, 20, 20)
WALL_COLOR = (100, 100, 100)
OBS_COLOR = (150, 150, 150)
RED = (220, 60, 60)
POISON_COLOR = (29, 117, 5)
SNAKE_COLOR = (0, 200, 0)
LEVEL_COLOR = (255, 210, 60)
SHIELD_COLOR = (100, 200, 255)
HUD_TEXT = (200, 200, 200)

WEIGHT_COLORS = {1: (255, 230, 0), 2: (255, 102, 255), 3: (255, 0, 102)}
POWERUP_COLORS = {"boost": (0, 255, 255), "slow": (100, 255, 100), "shield": SHIELD_COLOR}

# Setup Settings
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {"snake_color": list(SNAKE_COLOR), "grid": False, "sound": True}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding='utf-8', errors='replace') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding='utf-8', errors='replace') as f:
        json.dump(settings, f)

# Helper for Drawing Text
def draw_text(surface, text, size, x, y, color=(255, 255, 255), center=True):
    font = pygame.font.SysFont("monospace", size, bold=True)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(surf, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    clock = pygame.time.Clock()

    db.init_db()
    settings = load_settings()

    state = "MENU"
    username = ""
    player_id = None
    personal_best = 0
    last_score, last_level = 0, 0

    while True:
        screen.fill((0, 0, 0))

        if state == "MENU":
            draw_text(screen, "SNAKE REBORN", 40, WIN_W//2, 100, (0, 255, 0))
            draw_text(screen, "Username:", 20, WIN_W//2, 200)
            
            # Username input box
            box = pygame.Rect(WIN_W//2 - 100, 220, 200, 40)
            pygame.draw.rect(screen, (50, 50, 50), box)
            pygame.draw.rect(screen, (255, 255, 255), box, 2)
            draw_text(screen, username + ("|" if pygame.time.get_ticks() % 1000 < 500 else ""), 20, WIN_W//2, 240)

            draw_text(screen, "Press ENTER to Play", 20, WIN_W//2, 320, (255, 255, 0))
            draw_text(screen, "Press L for Leaderboard", 20, WIN_W//2, 360, (100, 200, 255))
            draw_text(screen, "Press S for Settings", 20, WIN_W//2, 400, (200, 200, 200))
            draw_text(screen, "Press ESC to Quit", 20, WIN_W//2, 440, (255, 100, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username.strip():
                        player_id = db.get_or_create_player(username.strip())
                        personal_best = db.get_personal_best(player_id)
                        state = "GAME"
                    elif event.key == pygame.K_l:
                        state = "LEADERBOARD"
                    elif event.key == pygame.K_s:
                        state = "SETTINGS"
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif len(username) < 15 and event.unicode.isprintable():
                        username += event.unicode

        elif state == "GAME":
            last_score, last_level, force_quit = run_game(screen, settings, personal_best)
            if force_quit:
                pygame.quit()
                sys.exit()
            
            db.save_game(player_id, last_score, last_level)
            personal_best = db.get_personal_best(player_id) # Refresh best
            state = "GAMEOVER"

        elif state == "GAMEOVER":
            draw_text(screen, "GAME OVER", 50, WIN_W//2, 150, (255, 50, 50))
            draw_text(screen, f"Score: {last_score}", 30, WIN_W//2, 250)
            draw_text(screen, f"Level: {last_level}", 30, WIN_W//2, 300)
            draw_text(screen, f"Personal Best: {personal_best}", 25, WIN_W//2, 350, (255, 215, 0))
            
            draw_text(screen, "Press ENTER to Retry", 20, WIN_W//2, 450, (0, 255, 0))
            draw_text(screen, "Press M for Main Menu", 20, WIN_W//2, 500, (200, 200, 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        state = "GAME"
                    elif event.key == pygame.K_m:
                        state = "MENU"

        elif state == "LEADERBOARD":
            draw_text(screen, "TOP 10 SCORES", 35, WIN_W//2, 50, (255, 215, 0))
            
            # Fetch and draw leaderboard
            board = db.get_leaderboard()
            y = 120
            draw_text(screen, f"{'RANK':<5} {'NAME':<15} {'SCORE':<7} {'LVL':<5} {'DATE':<10}", 16, 20, y, (150, 150, 150), center=False)
            y += 30
            for rank, name, score, lvl, date in board:
                draw_text(screen, f"{rank:<5} {name:<15} {score:<7} {lvl:<5} {date:<10}", 16, 20, y, center=False)
                y += 25

            draw_text(screen, "Press ESC to return", 20, WIN_W//2, 500, (100, 100, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "MENU"

        elif state == "SETTINGS":
            draw_text(screen, "SETTINGS", 40, WIN_W//2, 100, (200, 200, 200))
            
            grid_status = "ON" if settings.get("grid") else "OFF"
            sound_status = "ON" if settings.get("sound") else "OFF"
            
            draw_text(screen, f"[G] Grid Overlay: {grid_status}", 25, WIN_W//2, 220)
            draw_text(screen, f"[S] Sound: {sound_status}", 25, WIN_W//2, 280)
            draw_text(screen, "[C] Randomize Snake Color", 25, WIN_W//2, 340)
            
            # Show current color
            color_box = pygame.Rect(WIN_W//2 - 25, 370, 50, 50)
            pygame.draw.rect(screen, settings.get("snake_color", SNAKE_COLOR), color_box)
            pygame.draw.rect(screen, WHITE, color_box, 2)

            draw_text(screen, "Press ESC to Save & Return", 20, WIN_W//2, 500, (255, 255, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        settings["grid"] = not settings.get("grid", False)
                    elif event.key == pygame.K_s:
                        settings["sound"] = not settings.get("sound", True)
                    elif event.key == pygame.K_c:
                        import random
                        settings["snake_color"] = [random.randint(50, 255) for _ in range(3)]
                    elif event.key == pygame.K_ESCAPE:
                        save_settings(settings)
                        state = "MENU"

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()