# game.py
import pygame
import random

# Game Constants
CELL = 20
COLS, ROWS = 30, 20
HUD_HEIGHT = 40
WIN_W = COLS * CELL
WIN_H = ROWS * CELL + HUD_HEIGHT

FOODS_PER_LEVEL = 3
BASE_FPS = 8
FPS_PER_LEVEL = 2

# Directions
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

# Colors
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

def cell_rect(col, row):
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * CELL, CELL, CELL)

class Snake:
    def __init__(self, color):
        self.color = color
        self.reset()

    def reset(self):
        mid_c, mid_r = COLS // 2, ROWS // 2
        self.body = [(mid_c, mid_r), (mid_c - 1, mid_r)]
        self.direction = RIGHT
        self._next_dir = RIGHT
        self.grew = False
        self.shielded = False
        self.dead = False

    def set_direction(self, new_dir):
        if new_dir != (-self.direction[0], -self.direction[1]):
            self._next_dir = new_dir

    def move(self):
        self.direction = self._next_dir
        hx, hy = self.body[0]
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        if not self.grew:
            self.body.pop()
        self.grew = False

    def eat(self, amount=1):
        self.grew = True

    def shrink(self):
        if len(self.body) > 2:
            self.body.pop()
            self.body.pop()
        else:
            self.dead = True

    def head(self):
        return self.body[0]

    def hits_wall(self):
        hx, hy = self.head()
        hit = hx <= 0 or hx >= COLS - 1 or hy <= 0 or hy >= ROWS - 1
        if hit and self.shielded:
            self.shielded = False
            # Wrap around instead of dying
            if hx <= 0: hx = COLS - 2
            elif hx >= COLS - 1: hx = 1
            elif hy <= 0: hy = ROWS - 2
            elif hy >= ROWS - 1: hy = 1
            self.body[0] = (hx, hy)
            return False
        return hit

    def hits_self(self):
        hit = self.head() in self.body[1:]
        if hit and self.shielded:
            self.shielded = False
            return False
        return hit

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            color = SHIELD_COLOR if self.shielded and i == 0 else self.color
            pygame.draw.rect(surface, color, cell_rect(*segment))

class Item:
    def __init__(self):
        self.pos = (-1, -1)
        self.spawn_time = 0

    def get_free_pos(self, snake_body, obstacles, other_items=None):
        occupied = set(snake_body) | set(obstacles)
        if other_items:
            occupied |= set(other_items)
        candidates = [(c, r) for c in range(1, COLS - 1) for r in range(1, ROWS - 1) if (c, r) not in occupied]
        return random.choice(candidates) if candidates else (-1, -1)

class Food(Item):
    def __init__(self):
        super().__init__()
        self.weight = 1

    def respawn(self, snake_body, obstacles, other_items=None):
        self.pos = self.get_free_pos(snake_body, obstacles, other_items)
        self.weight = random.randint(1, 3)
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface, font):
        if self.pos == (-1, -1): return
        rect = cell_rect(*self.pos)
        pygame.draw.rect(surface, WEIGHT_COLORS[self.weight], rect)
        text = font.render(str(self.weight), True, BLACK)
        surface.blit(text, (rect.x + (CELL - text.get_width())//2, rect.y + (CELL - text.get_height())//2))

class Poison(Item):
    def __init__(self):
        super().__init__()
        self.active = False

    def try_spawn(self, snake_body, obstacles, food_pos):
        if random.random() < 0.3: # 30% chance to spawn with food
            self.pos = self.get_free_pos(snake_body, obstacles, [food_pos])
            self.active = True
            self.spawn_time = pygame.time.get_ticks()
        else:
            self.active = False
            self.pos = (-1, -1)

    def draw(self, surface):
        if self.active and self.pos != (-1, -1):
            pygame.draw.rect(surface, POISON_COLOR, cell_rect(*self.pos))

class PowerUp(Item):
    def __init__(self):
        super().__init__()
        self.active = False
        self.type = None

    def try_spawn(self, snake_body, obstacles, other_items):
        if not self.active and random.random() < 0.15: # 15% chance
            self.pos = self.get_free_pos(snake_body, obstacles, other_items)
            self.type = random.choice(["boost", "slow", "shield"])
            self.active = True
            self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface):
        if self.active and self.pos != (-1, -1):
            pygame.draw.rect(surface, POWERUP_COLORS[self.type], cell_rect(*self.pos))

def generate_obstacles(level, snake_body):
    if level < 3: return []
    obs = []
    # Avoid spawning near the center (snake start area)
    safe_zone = [(COLS//2 + dx, ROWS//2 + dy) for dx in range(-3, 4) for dy in range(-3, 4)]
    occupied = set(snake_body) | set(safe_zone)
    num_obs = (level - 2) * 3
    
    candidates = [(c, r) for c in range(1, COLS - 1) for r in range(1, ROWS - 1) if (c, r) not in occupied]
    random.shuffle(candidates)
    return candidates[:num_obs]

# Main game engine runner
def run_game(screen, settings, personal_best):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20, bold=True)
    small_font = pygame.font.SysFont("monospace", 14, bold=True)

    snake_color = tuple(settings.get("snake_color", SNAKE_COLOR))
    snake = Snake(snake_color)
    
    level, score = 1, 0
    foods_this_level = 0
    obstacles = generate_obstacles(level, snake.body)

    food = Food()
    poison = Poison()
    powerup = PowerUp()
    
    food.respawn(snake.body, obstacles)
    poison.try_spawn(snake.body, obstacles, food.pos)

    # Powerup tracking
    active_power_effect = None
    power_end_time = 0

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, level, True # Quit signal
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: snake.set_direction(UP)
                if event.key == pygame.K_DOWN: snake.set_direction(DOWN)
                if event.key == pygame.K_LEFT: snake.set_direction(LEFT)
                if event.key == pygame.K_RIGHT: snake.set_direction(RIGHT)

        # Clear expired items
        if food.weight in [2, 3] and current_time - food.spawn_time > (10000 if food.weight == 2 else 5000):
            food.respawn(snake.body, obstacles)
            poison.try_spawn(snake.body, obstacles, food.pos)
        
        if powerup.active and current_time - powerup.spawn_time > 8000:
            powerup.active = False

        if active_power_effect in ["boost", "slow"] and current_time > power_end_time:
            active_power_effect = None

        snake.move()

        # Collisions
        hit_obs = snake.head() in obstacles
        if snake.hits_wall() or snake.hits_self() or hit_obs or snake.dead:
            running = False

        # Interactions
        head = snake.head()
        if head == food.pos:
            snake.eat()
            score += food.weight * 10
            foods_this_level += 1
            if foods_this_level >= FOODS_PER_LEVEL:
                level += 1
                foods_this_level = 0
                obstacles = generate_obstacles(level, snake.body)
            food.respawn(snake.body, obstacles)
            poison.try_spawn(snake.body, obstacles, food.pos)
            powerup.try_spawn(snake.body, obstacles, [food.pos, poison.pos])

        if poison.active and head == poison.pos:
            snake.shrink()
            poison.active = False
            if snake.dead: running = False

        if powerup.active and head == powerup.pos:
            if powerup.type == "shield":
                snake.shielded = True
            else:
                active_power_effect = powerup.type
                power_end_time = current_time + 5000
            powerup.active = False

        # Render
        screen.fill(BG_COLOR)
        if settings.get("grid", False):
            for x in range(0, WIN_W, CELL): pygame.draw.line(screen, (30, 30, 30), (x, HUD_HEIGHT), (x, WIN_H))
            for y in range(HUD_HEIGHT, WIN_H, CELL): pygame.draw.line(screen, (30, 30, 30), (0, y), (WIN_W, y))

        # Draw borders and obstacles
        for c in range(COLS):
            pygame.draw.rect(screen, WALL_COLOR, cell_rect(c, 0))
            pygame.draw.rect(screen, WALL_COLOR, cell_rect(c, ROWS - 1))
        for r in range(1, ROWS - 1):
            pygame.draw.rect(screen, WALL_COLOR, cell_rect(0, r))
            pygame.draw.rect(screen, WALL_COLOR, cell_rect(COLS - 1, r))
        
        for obs in obstacles:
            pygame.draw.rect(screen, OBS_COLOR, cell_rect(*obs))

        food.draw(screen, small_font)
        poison.draw(screen)
        powerup.draw(screen)
        snake.draw(screen)

        # HUD
        pygame.draw.rect(screen, HUD_BG, pygame.Rect(0, 0, WIN_W, HUD_HEIGHT))
        screen.blit(font.render(f"SCORE {score}", True, HUD_TEXT), (10, 10))
        screen.blit(font.render(f"LVL {level}", True, LEVEL_COLOR), (150, 10))
        screen.blit(font.render(f"BEST {personal_best}", True, (180, 180, 255)), (WIN_W - 120, 10))

        pygame.display.flip()
        
        # Calculate speed
        fps = BASE_FPS + (level - 1) * FPS_PER_LEVEL
        if active_power_effect == "boost": fps += 6
        elif active_power_effect == "slow": fps = max(4, fps - 4)
        clock.tick(fps)

    return score, level, False