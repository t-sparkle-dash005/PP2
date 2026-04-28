#imports
import pygame, sys, os, random, time
from pygame.locals import *

#initializing pygame and mixer for music
pygame.init()
pygame.mixer.init()

#FPS setup
FPS = 60
FramePerSec = pygame.time.Clock()

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GAME_OVER_BG = (54, 1, 63)

COIN_GOLD = (255, 223, 0)
COIN_COLOR = (102, 77, 0)

#variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

#coins score
COIN_SCORE = 0


#setting up fonts
pixel_font_small = pygame.font.SysFont("Consolas", 20, bold=True)
pixel_font = pygame.font.Font("assets/ARCADECLASSIC.TTF", 64)


background = pygame.image.load("assets/AnimatedStreet.png")

#screen setup
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE, SPEED
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            
    #every 5 coins increase speed of enemy for 0.05 seconds
        if SCORE % 5 == 0 and SCORE != 0:
            original_speed = SPEED
            
            SPEED += 0.05 #enemy's speed gets very fast, so only added 0.05
            pygame.time.set_timer(INC_SPEED, 500, loops=1)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        #initial weight of coin, randomly selected 1-3
        self.weight = random.randint(1, 3)
        self.reset()
        
    def move(self):
        global SPEED
        #move using global SPEED so coins speed up with enemies
        self.rect.move_ip(0, SPEED)
        #if coin falls off the screen, respawn it
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        self.weight = random.randint(1, 3)
        
        
        COIN_DIMENSION = 40
        RADIUS = COIN_DIMENSION // 2
        
        #create a Surface with an alpha channel for transparency around the circle
        self.image = pygame.Surface((COIN_DIMENSION, COIN_DIMENSION), pygame.SRCALPHA)
        
        #draw the coin
        pygame.draw.circle(self.image, COIN_GOLD, (RADIUS, RADIUS), RADIUS)
        
        #draw weight on the coin
        weight_font = pygame.font.SysFont("Consolas", 32, bold=True)
        text_surf = weight_font.render(str(self.weight), True, COIN_COLOR)
        #center text inside the new circle surface
        text_rect = text_surf.get_rect(center=(RADIUS, RADIUS))
        self.image.blit(text_surf, text_rect)
        
        self.rect = self.image.get_rect()
        self.rect.top = random.randint(-300, -50)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), self.rect.top)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

#setup sprites
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(Coin())

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(*coins)

#user events
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#music setup
pygame.mixer.music.load("assets/background.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

#main game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    
    #UI text
    score_label = pixel_font_small.render(f"Total: {SCORE}", True, BLACK)
    coin_label = pixel_font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(score_label, (10, 10))
    DISPLAYSURF.blit(coin_label, (SCREEN_WIDTH - 120, 10))

    #UPD sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #coin and player collision
    collected_coin = pygame.sprite.spritecollideany(P1, coins)
    if collected_coin:
        pygame.mixer.Sound("assets/coin_received.wav").play()
        COIN_SCORE += collected_coin.weight
        collected_coin.reset()
        
    #coin and enemy collision
    for coin in coins:
        if pygame.sprite.spritecollideany(coin, enemies):
            coin.reset()

    #player and enemy collision
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("assets/crash.wav").play()
        pygame.mixer.music.stop()
        
        time.sleep(0.5)
        DISPLAYSURF.fill(GAME_OVER_BG)
        text_surface = pixel_font.render("GAME OVER", True, WHITE)
        DISPLAYSURF.blit(text_surface, (SCREEN_WIDTH//2 - text_surface.get_width()//2, SCREEN_HEIGHT//2 - text_surface.get_height()//2))
        pygame.display.update()
        
        for entity in all_sprites:
            entity.kill()
            
        time.sleep(2)
        pygame.quit()
        sys.exit()
        
    pygame.display.update()
    FramePerSec.tick(FPS)