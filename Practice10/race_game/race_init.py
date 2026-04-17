#Imports
import pygame, sys, random, time
from pygame.locals import *

#importing random for coin generation and time for "Game Over" splashscreen
import random, time

#Initializing 
pygame.init()
pygame.mixer.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#text color for Game Over screen
GAME_OVER = (54, 1, 63)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

#score for collected coins
COIN_SCORE = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
pixel_font = pygame.font.Font("assets/ARCADECLASSIC.TTF", 64)
 
background = pygame.image.load("assets/AnimatedStreet.png")
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


#--------->>Coin class created<<---------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #load and scale the coin image
        raw_pic = pygame.image.load("assets/Coin.png")
        self.image = pygame.transform.scale(raw_pic, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), -100)
        
    def move(self):
        #move the coin downwards
        self.rect.move_ip(0, 5)
        
        #avoid enemy collision
        avoid_enemy = pygame.sprite.spritecollideany(self, enemies)
        
        #reset coin position if it goes off the screen Or collides with an enemy
        if (self.rect.top > 600):
            self.rect.top = -50
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

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
                   
#Setting up Sprites
P1=Player()
E1=Enemy()

#new coin sprite
C1 = Coin()
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

#new group for coins
coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
pygame.mixer.music.load('assets/background.wav')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

while True:
    
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    
    # Display regular score
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    
    #display coin score in top right corner
    coin_text = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10)) 
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

#in case collision occurs between Player and Coin

    if pygame.sprite.spritecollideany(P1, coins):
        pygame.mixer.Sound('assets/coin_received.wav').play()
        pygame.mixer.music.set_volume(0.1)
        COIN_SCORE += 1
        C1.rect.top = -50
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)
        
#if collison between Coin and Enemy, reset Coin position without increasing score
    if pygame.sprite.spritecollideany(C1, enemies):
        C1.rect.top = -50
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('assets/crash.wav').play()
        pygame.mixer.music.stop()
        
        time.sleep(0.5)
        DISPLAYSURF.fill(GAME_OVER)
        font = pygame.font.Font(None, 36)
        text_surface = pixel_font.render("GAME OVER", False, (255, 255, 255))
        DISPLAYSURF.blit(text_surface, (SCREEN_WIDTH//2 - text_surface.get_width()//2, SCREEN_HEIGHT//2 - text_surface.get_height()//2))
        pygame.display.update()
        for entity in all_sprites:
                entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)