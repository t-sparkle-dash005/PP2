import pygame
import random

SCREEN_W = 400
SCREEN_H = 600

# road boundaries
ROAD_L = 60
ROAD_R = 340
ROAD_W = ROAD_R - ROAD_L

LANES = [110, 200, 290]
LANE_W = 80

# colour palette
ROAD_COLOR = (50,  52,  55)
CURB_A = (220, 30, 30)
CURB_B = (240, 240, 240)
GRASS_L = (34, 90, 34)
GRASS_R = (34, 90, 34)
DIVIDER_COLOR = (255, 255, 255)
EDGE_COLOR = (200, 200, 200)

#dashes
CURB_H = 20
DIVIDER_W = 6
DIVIDER_GAP = 30
DIVIDER_DASH = 40


class Road:
    #draws and scrolls the road surface every frame

    def __init__(self):
        self.scroll = 0          # vertical scroll offset
        self.curb_scroll = 0
        self.night_alpha = 0          # 0=day, 255=night
        self._overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)

    def update(self, speed: float):
        self.scroll      = (self.scroll + speed) % (CURB_H * 2)
        self.curb_scroll = self.scroll

    def draw(self, surface: pygame.Surface):
#grass
        surface.fill(GRASS_L, pygame.Rect(0, 0, ROAD_L, SCREEN_H))
        surface.fill(GRASS_R, pygame.Rect(ROAD_R, 0, SCREEN_W - ROAD_R, SCREEN_H))

        #road surface
        surface.fill(ROAD_COLOR, pygame.Rect(ROAD_L, 0, ROAD_W, SCREEN_H))

        #left curb
        self._draw_curb(surface, 0, ROAD_L)

        #right curb
        self._draw_curb(surface, ROAD_R, SCREEN_W - ROAD_R)

        #dashed lane dividers
        for lane_x in [155, 245]:
            self._draw_divider(surface, lane_x)

        #road edge lines
        pygame.draw.rect(surface, EDGE_COLOR, pygame.Rect(ROAD_L, 0, 3, SCREEN_H))
        pygame.draw.rect(surface, EDGE_COLOR, pygame.Rect(ROAD_R - 3, 0, 3, SCREEN_H))

        #night overlay
        if self.night_alpha > 0:
            self._overlay.fill((0, 0, 30, min(self.night_alpha, 180)))
            surface.blit(self._overlay, (0, 0))

    def _draw_curb(self, surface, x, w):
        offset = int(self.curb_scroll)
        # draw stripes from -CURB_H to SCREEN_H + CURB_H
        y = -CURB_H + offset % (CURB_H * 2) - CURB_H
        toggle = 0
        while y < SCREEN_H + CURB_H:
            color = CURB_A if toggle % 2 == 0 else CURB_B
            surface.fill(color, pygame.Rect(x, y, w, CURB_H))
            y += CURB_H
            toggle += 1

    def _draw_divider(self, surface, x):
        period = DIVIDER_DASH + DIVIDER_GAP
        offset  = int(self.scroll) % period
        y = -DIVIDER_DASH + offset - period
        while y < SCREEN_H + DIVIDER_DASH:
            pygame.draw.rect(surface, DIVIDER_COLOR,
                             pygame.Rect(x - DIVIDER_W // 2, y, DIVIDER_W, DIVIDER_DASH))
            y += period



class TrackEventManager:
    """
    Fires named events at score thresholds and queues notifications.
    Events: CHECKPOINT, LEVEL_UP, NIGHT_MODE, RUSH_HOUR, NARROW
    """

    # (score_threshold, event_name)
    EVENTS = [
        (5,  "CHECKPOINT"),
        (10, "LEVEL_UP"),
        (20, "CHECKPOINT"),
        (25, "NIGHT_MODE"),
        (30, "LEVEL_UP"),
        (35, "RUSH_HOUR"),
        (40, "CHECKPOINT"),
        (50, "LEVEL_UP"),
        (55, "CHECKPOINT"),
        (60, "RUSH_HOUR"),
        (70, "CHECKPOINT"),
        (80, "LEVEL_UP"),
        (90, "CHECKPOINT"),
        (100,"LEVEL_UP"),
    ]

    def __init__(self):
        self._fired = set()
        self.pending = []   # list of (event_name, extra_data)
        # repeat checkpoints every 20 after 100
        self._cp_next  = 120

    def update(self, score: int) -> list:
        """Call each frame. Returns list of newly fired event names."""
        fired = []
        for threshold, name in self.EVENTS:
            key = (threshold, name)
            if score >= threshold and key not in self._fired:
                self._fired.add(key)
                fired.append(name)

        # dynamic checkpoints beyond the preset list
        if score >= self._cp_next:
            fired.append("CHECKPOINT")
            self._cp_next += 20

        return fired

EVENT_MESSAGES = {
    "CHECKPOINT":  ("CHECKPOINT!",          (255, 220,  0)),
    "LEVEL_UP":    ("LEVEL UP!",            (80,  220, 255)),
    "NIGHT_MODE":  ("NIGHT DRIVING!",       (100, 100, 255)),
    "RUSH_HOUR":   ("RUSH HOUR!",           (255, 100,  60)),
    "NARROW":      ("ROAD NARROWS!",        (255, 160,  0)),
}


class NotificationBanner:
    """Displays a timed text banner in the middle of the screen."""

    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.text = ""
        self.color = (255, 255, 255)
        self.alpha = 0
        self._timer = 0
        self.DURATION = 120   # frames

    def trigger(self, event_name: str):
        msg, col  = EVENT_MESSAGES.get(event_name, (event_name, (255,255,255)))
        self.text  = msg
        self.color = col
        self._timer = self.DURATION
        self.alpha  = 255

    def update(self):
        if self._timer > 0:
            self._timer -= 1
            if self._timer < 40:
                self.alpha = int(255 * self._timer / 40)

    def draw(self, surface: pygame.Surface):
        if self._timer <= 0:
            return
        txt  = self.font.render(self.text, True, self.color)
        surf = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        surf.blit(txt, (0, 0))
        surf.set_alpha(self.alpha)
        cx = SCREEN_W // 2 - txt.get_width() // 2
        surface.blit(surf, (cx, SCREEN_H // 2 - 60))