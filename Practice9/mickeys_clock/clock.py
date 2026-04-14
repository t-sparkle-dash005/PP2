import pygame
import datetime
from pathlib import Path

class MickeyClock:
    def __init__(self, center_x, center_y):
        self.center = (center_x, center_y)
        
        images_dir = Path(__file__).resolve().parent / "images"
        try:

            self.hand_min_img = pygame.image.load(str(images_dir / "mickey_hand_min.png")).convert_alpha()
            self.hand_sec_img = pygame.image.load(str(images_dir / "mickey_hand_sec.png")).convert_alpha()
            
            self.bg_img = pygame.image.load(str(images_dir / "mickey_clock_face.png")).convert_alpha()
            
            bg_rect = self.bg_img.get_rect()
            self.width = bg_rect.width
            self.height = bg_rect.height
            
        except pygame.error:
            print("Warning: Clock image files are missing. Creating placeholders.")
            self.width, self.height = 600, 600
            
            self.bg_img = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.bg_img.fill((220, 220, 180, 255))
            self.hand_min_img = pygame.Surface((15, 200), pygame.SRCALPHA)
            self.hand_min_img.fill((0, 0, 0, 255))
            
            self.hand_sec_img = pygame.Surface((10, 180), pygame.SRCALPHA)
            self.hand_sec_img.fill((255, 0, 0, 255))

    def get_size(self):
        """Returns the size of the clock face (based on the background image)."""
        return self.width, self.height

    def draw(self, surface):
        surface.blit(self.bg_img, (0, 0))
        
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        min_angle = minutes * -6
        sec_angle = seconds * -6

        self._draw_hand(surface, self.hand_min_img, min_angle)
        
        self._draw_hand(surface, self.hand_sec_img, sec_angle)

    def _draw_hand(self, surface, image, angle):
        """Rotates and draws a hand image from its base center."""

        rotated_image = pygame.transform.rotate(image, angle)
        

        rotated_rect = rotated_image.get_rect(center=self.center)
        
        surface.blit(rotated_image, rotated_rect.topleft)