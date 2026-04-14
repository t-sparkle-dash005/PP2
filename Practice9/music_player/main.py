import pygame
import sys
import os
from player import MusicPlayer

WIDTH, HEIGHT = 520, 280
FPS = 30
BG = (18,  18,  28)
ACCENT = (100, 180, 255)
WHITE = (235, 235, 235)
GREY = (120, 120, 140)
BAR_COLOR = (60,  120, 200)
BAR_BG = (40,   40,  55)

MUSIC_DIR = os.path.join(os.path.dirname(__file__), "music")


def draw_ui(screen: pygame.Surface, player: MusicPlayer,
            title_font, body_font, small_font) -> None:
    screen.fill(BG)

    title = title_font.render("Music Player", True, ACCENT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 24))

    track = body_font.render(player.current_name, True, WHITE)
    screen.blit(track, (WIDTH // 2 - track.get_width() // 2, 90))

    status = body_font.render(player.status, True,
                               ACCENT if player.playing else GREY)
    screen.blit(status, (WIDTH // 2 - status.get_width() // 2, 130))

    pos   = min(player.position_sec, 60)
    ratio = pos / 60.0
    bar_x, bar_y, bar_w, bar_h = 60, 175, 400, 12
    pygame.draw.rect(screen, BAR_BG,    (bar_x, bar_y, bar_w, bar_h), border_radius=6)
    if ratio > 0:
        pygame.draw.rect(screen, BAR_COLOR,
                         (bar_x, bar_y, int(bar_w * ratio), bar_h), border_radius=6)
    pos_lbl = small_font.render(f"{pos:05.2f}s", True, GREY)
    screen.blit(pos_lbl, (bar_x + bar_w + 8, bar_y - 2))

    keys = "[P] Play  [S] Stop  [N] Next  [B] Back  [Q] Quit"
    guide = small_font.render(keys, True, GREY)
    screen.blit(guide, (WIDTH // 2 - guide.get_width() // 2, HEIGHT - 30))

    counter = small_font.render(
        f"Track {player.index + 1} / {len(player.playlist)}", True, GREY)
    screen.blit(counter, (WIDTH // 2 - counter.get_width() // 2, 158))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    try:
        player = MusicPlayer(MUSIC_DIR)
    except FileNotFoundError as e:
        print(e); sys.exit(1)

    title_font = pygame.font.SysFont("segoeui", 22, bold=True)
    body_font  = pygame.font.SysFont("segoeui", 17)
    small_font = pygame.font.SysFont("monospace", 13)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_p: player.play()
                    case pygame.K_s: player.stop()
                    case pygame.K_n: player.next_track()
                    case pygame.K_b: player.prev_track()
                    case pygame.K_q: pygame.quit(); sys.exit()

        draw_ui(screen, player, title_font, body_font, small_font)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()