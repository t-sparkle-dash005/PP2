#imports
import pygame, sys, random, os

#variables
CELL = 20
COLS = 30
ROWS = 20
HUD_HEIGHT = 40

WIN_W = COLS * CELL
WIN_H = ROWS * CELL + HUD_HEIGHT

#game setup
FOODS_PER_LEVEL = 3
BASE_FPS = 8
FPS_PER_LEVEL = 2

#directions for moving snake
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (0, 0, 0)
WALL_COLOR = (100, 100, 100)
SNAKE_COLOR = (0, 200, 0)
RED = (220, 60, 60)
HUD_BG = (20, 20, 20)
HUD_TEXT = (255, 255, 255)
LEVEL_COLOR = (255, 210,  60)

#weight Colors fod food
WEIGHT_COLORS = {
    1: (255, 230, 0),
    2: (255, 102, 255),
    3: (255, 0, 102)
}

#rectangles for border and HUD, not part of the grid
def cell_rect(col, row):
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * CELL, CELL, CELL)

#food class with weight and respawn logic
class Food:
    def __init__(self):
        self.pos = (1, 1)
        self.weight = 1
        self.spawn_time = 0

    def respawn(self, snake_body):
        snake_set = set(snake_body)
        candidates = [
            (c, r)
            for c in range(1, COLS - 1)
            for r in range(1, ROWS - 1)
            if (c, r) not in snake_set
        ]
        if candidates:
            self.pos = random.choice(candidates)
            self.weight = random.randint(1, 3)
            self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface, font):
        rect = cell_rect(*self.pos)
        #drawing colored food based on weight
        pygame.draw.rect(surface, WEIGHT_COLORS[self.weight], rect)
        
        #drawing weight text
        weight_font = pygame.font.SysFont("ARCADECLASSIC", 16, bold=True)
        weight_surf = weight_font.render(str(self.weight), True, BLACK)
        #centering text in cell
        text_x = rect.x + (CELL - weight_surf.get_width()) // 2
        text_y = rect.y + (CELL - weight_surf.get_height()) // 2
        surface.blit(weight_surf, (text_x, text_y))

#Snake class for moving snake, growing, and collision with walls and self
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        mid_c = COLS // 2
        mid_r = ROWS // 2
        self.body = [(mid_c, mid_r), (mid_c - 1, mid_r)]
        self.direction = RIGHT
        self._next_dir = RIGHT
        self.grew = False

    def set_direction(self, new_dir):
        opposite = (-new_dir[0], -new_dir[1])
        if new_dir != opposite:
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

    def eat(self):
        self.grew = True

    def head(self):
        return self.body[0]

    def hits_wall(self):
        hx, hy = self.head()
        return hx <= 0 or hx >= COLS - 1 or hy <= 0 or hy >= ROWS - 1

    def hits_self(self):
        return self.head() in self.body[1:]

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, SNAKE_COLOR, cell_rect(*segment))

def draw_hud(surface, score, level, font):
    pygame.draw.rect(surface, HUD_BG, pygame.Rect(0, 0, WIN_W, HUD_HEIGHT))
    score_surf = font.render(f"SCORE {score}", True, HUD_TEXT)
    level_surf = font.render(f"LEVEL {level}", True, LEVEL_COLOR)
    surface.blit(score_surf, (10, 10))
    surface.blit(level_surf, (WIN_W - level_surf.get_width() - 10, 10))

def draw_walls(surface):
    for c in range(COLS):
        pygame.draw.rect(surface, WALL_COLOR, cell_rect(c, 0))
        pygame.draw.rect(surface, WALL_COLOR, cell_rect(c, ROWS - 1))
    for r in range(1, ROWS - 1):
        pygame.draw.rect(surface, WALL_COLOR, cell_rect(0, r))
        pygame.draw.rect(surface, WALL_COLOR, cell_rect(COLS - 1, r))

def draw_game_over(surface, score, level, font):
    overlay = pygame.Surface((WIN_W, WIN_H))
    overlay.set_alpha(160)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))

    cx = WIN_W // 2
    lines = [
        ("GAME OVER", RED),
        (f"Score  {score}      Level  {level}", WHITE),
        ("Press   ENTER   to   Restart", WHITE)
    ]

    y = WIN_H // 2 - len(lines) * 20
    for text, color in lines:
        surf = font.render(text, True, color)
        surface.blit(surf, (cx - surf.get_width() // 2, y))
        y += 40

#main game loop: events, UPDs, drawing, timing, game over, restart
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    clock = pygame.time.Clock()
    
    # Fonts
    try:
        font = pygame.font.Font("ARCADECLASSIC.TTF", 20)
    except:
        font = pygame.font.SysFont("monospace", 20, bold=True)
    try:
        small_font = pygame.font.Font("ARCADECLASSIC.TTF", 14)
    except:
        small_font = pygame.font.SysFont("monospace", 14, bold=True)

    snake = Snake()
    food = Food()
    food.respawn(snake.body)

    score = 0
    level = 1
    foods_this_level = 0
    fps = BASE_FPS
    game_over = False

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:    snake.set_direction(UP)
                    if event.key == pygame.K_DOWN:  snake.set_direction(DOWN)
                    if event.key == pygame.K_LEFT:  snake.set_direction(LEFT)
                    if event.key == pygame.K_RIGHT: snake.set_direction(RIGHT)

                if game_over and event.key == pygame.K_RETURN:
                    snake = Snake()
                    food = Food()
                    score = 0
                    level = 1
                    foods_this_level = 0
                    fps = BASE_FPS
                    game_over = False
                    food.respawn(snake.body)

        if not game_over:
            #disappearing food (weights 3 and 2 only)
            if food.weight == 3:
                if current_time - food.spawn_time > 5000: #5 sec
                    food.respawn(snake.body)
                    
            if food.weight == 2:
                if current_time - food.spawn_time > 10000: #10 sec
                    food.respawn(snake.body)
                    
            snake.move()

            if snake.hits_wall() or snake.hits_self():
                game_over = True
            elif snake.head() == food.pos:
                snake.eat()
                # Score based on food weight
                score += food.weight * 10
                foods_this_level += 1

                if foods_this_level >= FOODS_PER_LEVEL:
                    level += 1
                    foods_this_level = 0
                    fps = BASE_FPS + (level - 1) * FPS_PER_LEVEL
                
                food.respawn(snake.body)

        screen.fill(BG_COLOR)
        draw_walls(screen)
        
        #draw food with weights and text
        food.draw(screen, small_font)
        snake.draw(screen)
        
        draw_hud(screen, score, level, font)

        if game_over:
            draw_game_over(screen, score, level, font)

        pygame.display.flip()
        clock.tick(fps if not game_over else 30)
#entry point!
if __name__ == "__main__":
    main()