import pygame
import sys
from clock import MickeyClock

def main():
    pygame.init()

    temp_screen = pygame.display.set_mode((100, 100))
    pygame.display.set_caption("Mickey's Clock")

    mickey_clock = MickeyClock(0, 0)
    width, height = mickey_clock.get_size()
    

    mickey_clock.center = (width // 2, height // 2)

    screen = pygame.display.set_mode((width, height))
    

    fps_clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mickey_clock.draw(screen)


        pygame.display.flip()
        fps_clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()