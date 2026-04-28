#imports
import pygame, math

#initializing
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
    pygame.display.set_caption("PaintApp")
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
                if event.key == pygame.K_F4 and alt_pressed:
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
        
        #tools, colors
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
                elif event.key == pygame.K_2: self.color = (255, 0, 0)
                elif event.key == pygame.K_3: self.color = (0, 255, 0)
                elif event.key == pygame.K_4: self.color = (0, 0, 255)

                #original tools
                elif event.key == pygame.K_b: self.tool = 'brush'
                elif event.key == pygame.K_e: self.tool = 'eraser'
                elif event.key == pygame.K_r: self.tool = 'rect'
                elif event.key == pygame.K_c: self.tool = 'circle'

                elif event.key == pygame.K_s: self.tool = 'square'
                elif event.key == pygame.K_t: self.tool = 'right_triangle'
                elif event.key == pygame.K_g: self.tool = 'equil_triangle'
                elif event.key == pygame.K_h: self.tool = 'rhombus'

                #clear screen
                elif event.key == pygame.K_SPACE:
                    self.canvas.fill(self.bg_color)

            #mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.drawing = True
                    self.start_pos = event.pos
                    self.last_pos = event.pos
                    self.current_pos = event.pos

            #finish shape on mouse release
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

    def _square_points(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        #pick the shorter side to keep the square proper
        side = min(abs(dx), abs(dy))
        sx = side if dx >= 0 else -side
        sy = side if dy >= 0 else -side
        x0, y0 = start
        return [
            (x0,      y0),
            (x0 + sx, y0),
            (x0 + sx, y0 + sy),
            (x0,      y0 + sy),
        ]

    def _right_triangle_points(self, start, end):

        ax, ay = start
        bx, by = end[0], start[1]
        cx, cy = start[0], end[1]
        return [(ax, ay), (bx, by), (cx, cy)]

    def _equil_triangle_points(self, start, end):
        x0, y0 = start
        x1 = end[0]
        base = abs(x1 - x0)
        if base == 0:
            base = 1
        height = int(base * math.sqrt(3) / 2)
        mid_x = (x0 + x1) // 2
        
        #base on bottom, apex above
        return [
            (x0,   y0 + height),
            (x1,   y0 + height),
            (mid_x, y0),
        ]

    def _rhombus_points(self, start, end):

        cx, cy = start
        half_w = abs(end[0] - start[0])
        half_h = abs(end[1] - start[1])
        if half_w == 0: half_w = 1
        if half_h == 0: half_h = 1
        return [
            (cx, cy - half_h),
            (cx + half_w, cy),
            (cx, cy + half_h),
            (cx - half_w, cy),
        ]


    def commit_shape(self):
        sp, ep = self.start_pos, self.current_pos
        if not (sp and ep):
            return

        if self.tool == 'rect':
            rect = pygame.Rect(sp[0], sp[1], ep[0] - sp[0], ep[1] - sp[1])
            rect.normalize()
            pygame.draw.rect(self.canvas, self.color, rect, self.radius)

        elif self.tool == 'circle':
            dx, dy = ep[0] - sp[0], ep[1] - sp[1]
            rad = int(math.hypot(dx, dy))
            pygame.draw.circle(self.canvas, self.color, sp, rad, self.radius)

        elif self.tool == 'square':
            pts = self._square_points(sp, ep)
            pygame.draw.polygon(self.canvas, self.color, pts, self.radius)

        elif self.tool == 'right_triangle':
            pts = self._right_triangle_points(sp, ep)
            pygame.draw.polygon(self.canvas, self.color, pts, self.radius)

        elif self.tool == 'equil_triangle':
            pts = self._equil_triangle_points(sp, ep)
            pygame.draw.polygon(self.canvas, self.color, pts, self.radius)

        elif self.tool == 'rhombus':
            pts = self._rhombus_points(sp, ep)
            pygame.draw.polygon(self.canvas, self.color, pts, self.radius)

    def _draw_preview(self, surface):
        sp, ep = self.start_pos, self.current_pos
        if not (sp and ep):
            return

        if self.tool == 'rect':
            rect = pygame.Rect(sp[0], sp[1], ep[0] - sp[0], ep[1] - sp[1])
            rect.normalize()
            pygame.draw.rect(surface, self.color, rect, self.radius)

        elif self.tool == 'circle':
            dx, dy = ep[0] - sp[0], ep[1] - sp[1]
            rad = int(math.hypot(dx, dy))
            pygame.draw.circle(surface, self.color, sp, rad, self.radius)

        elif self.tool == 'square':
            pts = self._square_points(sp, ep)
            pygame.draw.polygon(surface, self.color, pts, self.radius)

        elif self.tool == 'right_triangle':
            pts = self._right_triangle_points(sp, ep)
            pygame.draw.polygon(surface, self.color, pts, self.radius)

        elif self.tool == 'equil_triangle':
            pts = self._equil_triangle_points(sp, ep)
            pygame.draw.polygon(surface, self.color, pts, self.radius)

        elif self.tool == 'rhombus':
            pts = self._rhombus_points(sp, ep)
            pygame.draw.polygon(surface, self.color, pts, self.radius)

    def Render(self, screen):
        
        #permanent canvas
        screen.blit(self.canvas, (0, 0))
        
        #live preview while dragging a shape
        if self.drawing and self.current_pos:
            self._draw_preview(screen)
        
        #UI bar at the bottom
        ui_rect = pygame.Rect(0, 570, 800, 30)
        pygame.draw.rect(screen, (200, 200, 200), ui_rect)
        pygame.draw.line(screen, (100, 100, 100), (0, 570), (800, 570), 2)
        
        ui_line = (
            f"Tool: {self.tool.upper()}  "
            f"|  B=Brush    E=Eraser    R=Rect    C=Circle    S=Square    T=RightTR    Y=EquilTR    H=Rhombus  "
            f"| Color(1-4): {self.color}  |  Space=Clear"
        )
        text_surface = self.font.render(ui_line, True, (0, 0, 0))
        screen.blit(text_surface, (6, 576))


#start the game
run_game(800, 600, 60, PaintScene())