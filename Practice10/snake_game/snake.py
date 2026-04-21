#imports
import pygame, sys, random

#constants
CELL = 20
COLS = 30
ROWS = 20
HUD_HEIGHT = 40

WIN_W = COLS * CELL
WIN_H = ROWS * CELL + HUD_HEIGHT

FOODS_PER_LEVEL = 3
BASE_FPS = 8
FPS_PER_LEVEL = 2

# directions
UP = ( 0, -1)
DOWN = ( 0,  1)
LEFT = (-1,  0)
RIGHT = ( 1,  0)

#colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BG_COLOR = (  0,   0,   0)
WALL_COLOR = (100, 100, 100)
SNAKE_COLOR = (  0, 200,   0)
FOOD_COLOR = (200,   0,   0)
HUD_BG = ( 20,  20,  20)
HUD_TEXT = (255, 255, 255)
LEVEL_COLOR = (255, 210,  60)

#pixels for border and HUD, not part of the grid
def cell_rect(col, row):
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * CELL, CELL, CELL)



class Food:
    def __init__(self):
        self.pos = (1, 1)

#placing food at a random inner cell
    def respawn(self, snake_body):
        snake_set  = set(snake_body)
        candidates = [
            (c, r)
            for c in range(1, COLS - 1)
            for r in range(1, ROWS - 1)
            if (c, r) not in snake_set
        ]
        if candidates:
            self.pos = random.choice(candidates)

    def draw(self, surface):
        pygame.draw.rect(surface, FOOD_COLOR, cell_rect(*self.pos))



class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        mid_c = COLS // 2
        mid_r = ROWS // 2
        self.body = [(mid_c, mid_r), (mid_c - 1, mid_r), (mid_c - 2, mid_r)]
        self.direction = RIGHT
        self._next_dir = RIGHT
        self.grew = False

#snake can't reverse into itself, ignore opposite direction
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

#game over if snake hits wall or itself
    def hits_wall(self):
        """Feature 1 — die if the snake enters the border ring."""
        hx, hy = self.head()
        return hx <= 0 or hx >= COLS - 1 or hy <= 0 or hy >= ROWS - 1

    def hits_self(self):
        return self.head() in self.body[1:]

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, SNAKE_COLOR, cell_rect(*segment))


#HUD and Score at the top
def draw_hud(surface, score, level, font):
    pygame.draw.rect(surface, HUD_BG, pygame.Rect(0, 0, WIN_W, HUD_HEIGHT))

    score_surf = font.render(f"SCORE: {score}", True, HUD_TEXT)
    level_surf = font.render(f"LEVEL: {level}", True, LEVEL_COLOR)

    surface.blit(score_surf, (10, 10))
    surface.blit(level_surf, (WIN_W - level_surf.get_width() - 10, 10))


#walls around the edge
def draw_walls(surface):
    for c in range(COLS):
        pygame.draw.rect(surface, WALL_COLOR, cell_rect(c, 0))
        pygame.draw.rect(surface, WALL_COLOR, cell_rect(c, ROWS - 1))
    for r in range(1, ROWS - 1):
        pygame.draw.rect(surface, WALL_COLOR, cell_rect(0, r))
        pygame.draw.rect(surface, WALL_COLOR, cell_rect(COLS - 1, r))


#game over screen
def draw_game_over(surface, score, level, font):
    overlay = pygame.Surface((WIN_W, WIN_H))
    overlay.set_alpha(160)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))

    cx = WIN_W // 2
    lines = [
        ("GAME OVER", (220,  60,  60)),
        (f"Score: {score}  Level: {level}", WHITE),
    ]

    y = WIN_H // 2 - len(lines) * 22
    for text, color in lines:
        surf = font.render(text, True, color)
        surface.blit(surf, (cx - surf.get_width() // 2, y))
        y += 40


#main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20, bold=True)

    snake = Snake()
    food = Food()
    food.respawn(snake.body)

    score = 0
    level = 1
    foods_this_level = 0
    fps = BASE_FPS
    game_over = False

    while True:
#event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                #arrow keys for direction
                if not game_over:
                    if event.key == pygame.K_UP:    snake.set_direction(UP)
                    if event.key == pygame.K_DOWN:  snake.set_direction(DOWN)
                    if event.key == pygame.K_LEFT:  snake.set_direction(LEFT)
                    if event.key == pygame.K_RIGHT: snake.set_direction(RIGHT)

                #restart
                if game_over and event.key == pygame.K_SPACE:
                    snake = Snake()
                    food = Food()
                    score = 0
                    level = 1
                    foods_this_level = 0
                    fps = BASE_FPS
                    game_over = False
                    food.respawn(snake.body)

#UPD
        if not game_over:
            snake.move()

            #wall collision
            if snake.hits_wall() or snake.hits_self():
                game_over = True

            elif snake.head() == food.pos:
                snake.eat()
                score            += 10
                foods_this_level += 1

                #level up every 3 foods, increase speed
                if foods_this_level >= FOODS_PER_LEVEL:
                    level            += 1
                    foods_this_level  = 0
                    fps = BASE_FPS + (level - 1) * FPS_PER_LEVEL
#respawn food in a free cell if eaten
                food.respawn(snake.body)

        screen.fill(BG_COLOR)
        draw_walls(screen)
        food.draw(screen)
        snake.draw(screen)
        #display score and level in the top
        draw_hud(screen, score, level, font)

        if game_over:
            draw_game_over(screen, score, level, font)

        pygame.display.flip()
        clock.tick(fps if not game_over else 30)


if __name__ == "__main__":
    main()