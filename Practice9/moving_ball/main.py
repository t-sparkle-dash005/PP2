import pygame
import sys
from ball import Ball

WIDTH, HEIGHT = 600, 480
FPS = 60
BG_COLOR = (255, 255, 255)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    clock  = pygame.time.Clock()

    ball   = Ball(WIDTH, HEIGHT)
    font   = pygame.font.SysFont("monospace", 14)

    KEY_MAP = {
        pygame.K_UP:    (0,           -Ball.STEP),
        pygame.K_DOWN:  (0,            Ball.STEP),
        pygame.K_LEFT:  (-Ball.STEP,   0),
        pygame.K_RIGHT: ( Ball.STEP,   0),
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key in KEY_MAP:
                    ball.move(*KEY_MAP[event.key])

        screen.fill(BG_COLOR)
        ball.draw(screen)

        hint = font.render("Arrow keys to move  |  ESC to quit", True, (180, 180, 180))
        screen.blit(hint, (10, HEIGHT - 24))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()