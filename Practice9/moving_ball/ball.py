import pygame

class Ball:

    RADIUS = 25
    STEP   = 20
    COLOR  = (220, 50, 50)

    def __init__(self, screen_w: int, screen_h: int):
        self.x = screen_w // 2
        self.y = screen_h // 2
        self.screen_w = screen_w
        self.screen_h = screen_h

    def move(self, dx: int, dy: int) -> None:
        new_x = self.x + dx
        new_y = self.y + dy

        if self.RADIUS <= new_x <= self.screen_w - self.RADIUS:
            self.x = new_x
        if self.RADIUS <= new_y <= self.screen_h - self.RADIUS:
            self.y = new_y

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.COLOR, (self.x, self.y), self.RADIUS)
        pygame.draw.circle(surface, (160, 30, 30), (self.x, self.y), self.RADIUS, 2)