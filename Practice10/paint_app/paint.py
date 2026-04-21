import pygame, sys
import math

pygame.init()

#scene framework
class SceneBase:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pygame Paint Extension")
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        
        #filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(fps)

#main scene
class PaintScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.canvas = pygame.Surface((800, 600))
        #white background
        self.canvas.fill((255, 255, 255))
        
        #tools,colors
        self.tool = 'brush'
        self.color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.radius = 5
        
        self.drawing = False
        self.start_pos = None
        self.current_pos = None
        self.last_pos = None
        
        self.font = pygame.font.SysFont(None, 16)
        
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            #tools and colors selection
            if event.type == pygame.KEYDOWN:
                #colors
                if event.key == pygame.K_1: self.color = (0, 0, 0)
                #RGB presets
                elif event.key == pygame.K_2: self.color = (255, 0, 0)
                elif event.key == pygame.K_3: self.color = (0, 255, 0)
                elif event.key == pygame.K_4: self.color = (0, 0, 255)

                #tools
                elif event.key == pygame.K_b: self.tool = 'brush'
                elif event.key == pygame.K_e: self.tool = 'eraser'
                elif event.key == pygame.K_r: self.tool = 'rect'
                elif event.key == pygame.K_c: self.tool = 'circle'
                
                #clear screen
                elif event.key == pygame.K_SPACE:
                    self.canvas.fill(self.bg_color)

            #mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #hold left click to draw
                if event.button == 1:
                    self.drawing = True
                    self.start_pos = event.pos
                    self.last_pos = event.pos
                    self.current_pos = event.pos
#finish shape sizes
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.drawing:
                    self.drawing = False
                    self.current_pos = event.pos
                    self.commit_shape()

            elif event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    self.current_pos = event.pos
                    if self.tool in ['brush', 'eraser']:
                        self.draw_brush()

    def draw_brush(self):
        #select color based on tool
        draw_color = self.bg_color if self.tool == 'eraser' else self.color
        
        #draw line from last to current position for smoothness
        pygame.draw.line(self.canvas, draw_color, self.last_pos, self.current_pos, self.radius * 2)
        
        pygame.draw.circle(self.canvas, draw_color, self.current_pos, self.radius)
        
        self.last_pos = self.current_pos

    def commit_shape(self):
        """Draws the final shape onto the permanent canvas when the mouse is released."""
        if self.tool == 'rect' and self.start_pos and self.current_pos:
            rect = pygame.Rect(self.start_pos[0], self.start_pos[1],
                            self.current_pos[0] - self.start_pos[0],
                            self.current_pos[1] - self.start_pos[1])
            #ensure width and height are positive
            rect.normalize()
            pygame.draw.rect(self.canvas, self.color, rect, self.radius)
            
        elif self.tool == 'circle' and self.start_pos and self.current_pos:
            dx = self.current_pos[0] - self.start_pos[0]
            dy = self.current_pos[1] - self.start_pos[1]
            #pythagorean distance for radius
            rad = int(math.hypot(dx, dy))
            pygame.draw.circle(self.canvas, self.color, self.start_pos, rad, self.radius)

    def Render(self, screen):
        #permanent canvas
        screen.blit(self.canvas, (0, 0))
        
        #preview shape while drawing
        if self.drawing and self.current_pos:
            if self.tool == 'rect':
                rect = pygame.Rect(self.start_pos[0], self.start_pos[1],
                                self.current_pos[0] - self.start_pos[0],
                                self.current_pos[1] - self.start_pos[1])
                rect.normalize()
                pygame.draw.rect(screen, self.color, rect, self.radius)
            elif self.tool == 'circle':
                dx = self.current_pos[0] - self.start_pos[0]
                dy = self.current_pos[1] - self.start_pos[1]
                rad = int(math.hypot(dx, dy))
                pygame.draw.circle(screen, self.color, self.start_pos, rad, self.radius)
        
        #UI text
        ui_rect = pygame.Rect(0, 570, 800, 30)
        pygame.draw.rect(screen, (200, 200, 200), ui_rect)
        pygame.draw.line(screen, (100, 100, 100), (0, 570), (800, 570), 2)
        
        cell = [f"Tool (B/E/R/C): {self.tool.upper()} | Color (1-5): {self.color} | Clear (Space)"]
        for i, row in enumerate(cell):
            text_surface = self.font.render(row, True, (0, 0, 0))
            screen.blit(text_surface, (10, 575 + i * 20))

#start the game
run_game(800, 600, 60, PaintScene())