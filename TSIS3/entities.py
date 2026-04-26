import pygame
import random
import os
from pygame.locals import K_LEFT, K_RIGHT

#colors
PLAYER_BODY   = (30,  120, 255)
PLAYER_DARK   = (10,   60, 160)
PLAYER_GLASS  = (150, 200, 255)
ENEMY_BODY    = (220,  50,  40)
ENEMY_DARK    = (120,  20,  10)
ENEMY_GLASS   = (255, 160, 150)
WHEEL_COLOR   = (30,   30,  30)
WHEEL_RIM     = (180, 180, 180)
COIN_GOLD     = (255, 215,   0)
COIN_DARK     = (160, 120,   0)
COIN_SHINE    = (255, 255, 180)

SCREEN_W = 400
SCREEN_H = 600

#lane centres inside the road (road occupies x=60..340)
LANES  = [110, 200, 290]
LANE_W = 80


def _draw_car(surface, body_col, dark_col, glass_col, w=50, h=80):
    #draw a top-down car onto sufrace
    surf = surface
    #shadow
    pygame.draw.ellipse(surf, (0, 0, 0, 60), pygame.Rect(4, 6, w - 8, h - 4))
    #body
    pygame.draw.rect(surf, body_col, pygame.Rect(4,  4, w - 8, h - 8),  border_radius=8)
    pygame.draw.rect(surf, dark_col, pygame.Rect(4,  4, w - 8, h - 8),  border_radius=8, width=2)
    #cabin / windshields
    pygame.draw.rect(surf, glass_col, pygame.Rect(10, 14, w - 20, 18), border_radius=4)   # front
    pygame.draw.rect(surf, glass_col, pygame.Rect(10, h - 32, w - 20, 14), border_radius=4) # rear
    #stripe
    pygame.draw.rect(surf, dark_col, pygame.Rect(4,  h // 2 - 3, w - 8, 6))
    #wheels
    for wx, wy in [(2, 8), (w - 10, 8), (2, h - 22), (w - 10, h - 22)]:
        pygame.draw.rect(surf, WHEEL_COLOR, pygame.Rect(wx, wy, 8, 14), border_radius=3)
        pygame.draw.rect(surf, WHEEL_RIM, pygame.Rect(wx + 1, wy + 2, 6, 10), border_radius=2)
    #headlights / tail-lights
    pygame.draw.circle(surf, (255, 255, 180), (10,  6), 4)
    pygame.draw.circle(surf, (255, 255, 180), (w-10, 6), 4)
    pygame.draw.circle(surf, (255, 80,  60), (10,  h - 6), 4)
    pygame.draw.circle(surf, (255, 80,  60), (w-10, h - 6), 4)


class Player(pygame.sprite.Sprite):
    W, H = 50, 80
    SPEED = 5

    def __init__(self):
        super().__init__()
        #try loading an image first
        img_path = os.path.join("assets", "Player.png")
        if os.path.exists(img_path):
            raw = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(raw, (self.W, self.H))
        else:
            self.image = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            _draw_car(self.image, PLAYER_BODY, PLAYER_DARK, PLAYER_GLASS, self.W, self.H)

        self.base_image = self.image.copy()
        self.rect = self.image.get_rect(center=(200, 510))
        self.lane = 1
        self.target_x = LANES[1]   #smooth lane-switch target

        #status effects
        self.boost_ticks = 0          #frames of speed-boost remaining
        self.invincible = 0          #frames of post-crash invincibility

    def move(self, pressed):
        #move left/right, respecting road boundaries
        spd = self.SPEED + (2 if self.boost_ticks > 0 else 0)

        self.image = self.base_image
        if pressed[K_LEFT]  and self.rect.left > 60:
            self.rect.x -= spd
        if pressed[K_RIGHT] and self.rect.right < 340:
            self.rect.x += spd

        if self.boost_ticks > 0:
            self.boost_ticks -= 1
        if self.invincible > 0:
            self.invincible -= 1
            #blink while invincible
            self.image.set_alpha(100 if (self.invincible // 6) % 2 else 255)

    def apply_boost(self, frames=120):
        self.boost_ticks = frames

    def grant_invincibility(self, frames=90):
        self.invincible = frames
        self.image.set_alpha(255)

    @property
    def is_invincible(self):
        return self.invincible > 0



class Enemy(pygame.sprite.Sprite):
    W, H = 50, 80

    def __init__(self, speed_ref: list):
        #speed_ref is a 1-element list so we can mutate global speed
        super().__init__()
        img_path = os.path.join("assets", "Enemy.png")
        if os.path.exists(img_path):
            raw = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(raw, (self.W, self.H))
        else:
            self.image = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            _draw_car(self.image, ENEMY_BODY, ENEMY_DARK, ENEMY_GLASS, self.W, self.H)
            #flip vertically so headlights face down
            self.image = pygame.transform.flip(self.image, False, True)

        self.speed_ref = speed_ref
        self.rect = self.image.get_rect()
        self._spawn()

    def _spawn(self):
        lane = random.choice(LANES)
        self.rect.centerx = lane
        self.rect.bottom = random.randint(-200, -60)

    def move(self, score_ref: list) -> bool:
        #returns True when enemy passes the bottom score event
        self.rect.y += self.speed_ref[0]
        if self.rect.top > SCREEN_H:
            self._spawn()
            return True
        return False


class Coin(pygame.sprite.Sprite):
    DIM = 40

    def __init__(self, speed_ref: list):
        super().__init__()
        self.speed_ref = speed_ref
        self.weight = 1
        self._build_surface()

    def _build_surface(self):
        self.weight = random.randint(1, 3)
        r = self.DIM // 2
        self.image = pygame.Surface((self.DIM, self.DIM), pygame.SRCALPHA)
        # shadow
        pygame.draw.ellipse(self.image, (0,0,0,50), pygame.Rect(4, r+4, self.DIM-8, r-4))
        # body
        pygame.draw.circle(self.image, COIN_GOLD,  (r, r), r)
        pygame.draw.circle(self.image, COIN_SHINE, (r-4, r-4), r//3)
        pygame.draw.circle(self.image, COIN_DARK,  (r, r), r, 2)
        # weight text
        fnt = pygame.font.SysFont("consolas", 20, bold=True)
        txt = fnt.render(str(self.weight), True, COIN_DARK)
        self.image.blit(txt, txt.get_rect(center=(r, r)))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.top = random.randint(-400, -60)

    def move(self):
        self.rect.y += self.speed_ref[0]
        if self.rect.top > SCREEN_H:
            self._build_surface()

    def reset(self):
        self._build_surface()


class SpeedBoost(pygame.sprite.Sprite):
    W, H = 50, 40

    def __init__(self, speed_ref: list):
        super().__init__()
        self.speed_ref = speed_ref
        self.image = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        self._draw()
        self.rect  = self.image.get_rect()
        self._spawn()
        self.anim_t = 0

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        # green arrow pointing down (represents going forward = boost)
        pts = [(self.W//2, self.H-4), (4, 4), (self.W-4, 4)]
        pygame.draw.polygon(self.image, (0, 230, 80),  pts)
        pygame.draw.polygon(self.image, (0, 180, 50),  pts, 2)
        fnt = pygame.font.SysFont("consolas", 11, bold=True)
        txt = fnt.render("BOOST", True, (0, 255, 100))
        self.image.blit(txt, txt.get_rect(center=(self.W//2, self.H//2)))

    def _spawn(self):
        self.rect.centerx = random.choice(LANES)
        self.rect.top = random.randint(-700, -200)

    def move(self):
        self.rect.y += self.speed_ref[0]
        if self.rect.top > SCREEN_H:
            self._spawn()



class Cone(pygame.sprite.Sprite):
    W, H = 30, 40

    def __init__(self, speed_ref: list, lane: int = None):
        super().__init__()
        self.speed_ref = speed_ref
        self.image = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        self._draw_cone()
        self.rect = self.image.get_rect()
        self._spawn(lane)

    def _draw_cone(self):
        # alternating orange/white stripes traffic cone
        tip = (self.W // 2, 0)
        base_l = (2, self.H)
        base_r = (self.W - 2, self.H)
        # main cone
        pygame.draw.polygon(self.image, (255, 100, 0),   [tip, base_l, base_r])
        # white stripe
        mid_y = self.H * 2 // 3
        w_mid = int((self.H - mid_y) / self.H * self.W * 0.5)
        mx = self.W // 2
        stripe_pts = [
            (mx - w_mid - 4, mid_y),
            (mx + w_mid + 4, mid_y),
            (mx + w_mid, mid_y + 8),
            (mx - w_mid, mid_y + 8),
        ]
        pygame.draw.polygon(self.image, (240, 240, 240), stripe_pts)
        # outline
        pygame.draw.polygon(self.image, (180, 60, 0), [tip, base_l, base_r], 2)
        # base plate
        pygame.draw.rect(self.image, (60, 60, 60), pygame.Rect(0, self.H - 6, self.W, 6), border_radius=2)

    def _spawn(self, lane=None):
        self.rect.centerx = lane if lane is not None else random.choice(LANES)
        self.rect.top = random.randint(-500, -80)

    def move(self):
        self.rect.y += self.speed_ref[0]
        if self.rect.top > SCREEN_H:
            self._spawn()



class Checkpoint(pygame.sprite.Sprite):
    """Horizontal gate across the road. Crossing awards bonus coins."""
    W, H = 280, 24

    def __init__(self, speed_ref: list, score_trigger: int):
        super().__init__()
        self.speed_ref = speed_ref
        self.score_trigger = score_trigger
        self.active = False
        self.crossed = False
        self.image = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        self._draw()
        self.rect  = self.image.get_rect()
        self.rect.centerx = 200
        self.rect.top = -100

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        # checkered banner
        sq = 12
        cols = [(255, 255, 255), (0, 0, 0)]
        for c in range(self.W // sq + 1):
            for r in range(self.H // sq + 1):
                color = cols[(c + r) % 2]
                pygame.draw.rect(self.image, color,
                                 pygame.Rect(c * sq, r * sq, sq, sq))
        # yellow border
        pygame.draw.rect(self.image, (255, 220, 0),
                         pygame.Rect(0, 0, self.W, self.H), 3)
        fnt = pygame.font.SysFont("consolas", 13, bold=True)
        txt = fnt.render("CHECKPOINT  +5 COINS", True, (255, 220, 0))
        self.image.blit(txt, txt.get_rect(center=(self.W // 2, self.H // 2)))

    def activate(self):
        self.active  = True
        self.crossed = False
        self.rect.centerx = 200
        self.rect.top = -self.H - 10

    def move(self) -> bool:
        #returns True when player has crossed it
        if not self.active:
            return False
        self.rect.y += self.speed_ref[0]
        if self.rect.top > SCREEN_H:
            self.active = False
            self.crossed = True
            return False
        return False

    def check_cross(self, player_rect) -> bool:
        if self.active and self.rect.colliderect(player_rect):
            self.active  = False
            self.crossed = True
            return True
        return False