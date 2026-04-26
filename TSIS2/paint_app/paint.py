import pygame,  sys

from tools import flood_fill, save_canvas, draw_shape

pygame.init()

#variables
WIDTH, HEIGHT = 900, 700
UI_HEIGHT = 80
CANVAS_HEIGHT = HEIGHT - UI_HEIGHT

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

COLORS = [BLACK, RED, GREEN, BLUE]

shape_tools = ['line', 'rect', 'circle', 'square', 'right_tri', 'eq_tri', 'rhombus']

screen = pygame.display.set_mode((WIDTH, HEIGHT))


#canvas setup
canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

action_history = [canvas.copy()]

#state variables for avoiding definition inside the loop
current_tool = 'pencil'
current_color = BLACK
brush_size = 2 #2 small, 5 medium, 10 large
drawing = False
start_pos = None

#text tools' variables
typing = False
text_input = ""
text_pos = (0, 0)
font = pygame.font.SysFont("Arial", 24)
ui_font = pygame.font.SysFont("Arial", 16)

clock = pygame.time.Clock()

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, UI_HEIGHT))
    
    #display active tools
    instr_1 = ui_font.render("TOOLS: [P]encil, [E]raser, [L]ine, [F]ill, [T]ext | SAVE: Ctrl+S | UNDO: Ctrl+Z", True, BLACK)
    instr_2 = ui_font.render("SHAPES: [R]ect, [S]quare, [C]ircle, [1] Right Tri, [2] Eq Tri, [3] Rhombus", True, BLACK)
    instr_3 = ui_font.render(f"ACTIVE TOOL: {current_tool.upper()} | BRUSH SIZE: {brush_size}px (Keys: 7, 8, 9)", True, BLUE)
    
    screen.blit(instr_1, (10, 5))
    screen.blit(instr_2, (10, 25))
    screen.blit(instr_3, (10, 50))
    
    #available colors
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(450 + i * 40, 25, 30, 30)
        pygame.draw.rect(screen, color, rect)
        if current_color == color:
            pygame.draw.rect(screen, WHITE, rect, 2)

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, UI_HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                save_canvas(canvas)
                continue

            if typing:
                if event.key == pygame.K_RETURN:
                    action_history.append(canvas.copy())
                    text_surface = font.render(text_input, True, current_color)
                    canvas.blit(text_surface, (text_pos[0], text_pos[1] - UI_HEIGHT))
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode
            else:
                #tool selection shortcuts
                if event.key == pygame.K_p: current_tool = 'pencil'
                elif event.key == pygame.K_e: current_tool = 'eraser'
                elif event.key == pygame.K_l: current_tool = 'line'
                elif event.key == pygame.K_f: current_tool = 'fill'
                elif event.key == pygame.K_t: current_tool = 'text'
                #shape shortcuts
                elif event.key == pygame.K_r: current_tool = 'rect'
                elif event.key == pygame.K_s: current_tool = 'square'
                elif event.key == pygame.K_c: current_tool = 'circle'
                elif event.key == pygame.K_1: current_tool = 'right_tri'
                elif event.key == pygame.K_2: current_tool = 'eq_tri'
                elif event.key == pygame.K_3: current_tool = 'rhombus'
                #brush sizes
                elif event.key == pygame.K_7: brush_size = 2
                elif event.key == pygame.K_8: brush_size = 5
                elif event.key == pygame.K_9: brush_size = 10

                #undo feature
                if mods & pygame.KMOD_CTRL and event.key == pygame.K_z:
                    if len(action_history) > 1:
                        action_history.pop()
                        canvas = action_history[-1].copy()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                
                #check if user chose a color
                if y < UI_HEIGHT:
                    for i, color in enumerate(COLORS):
                        if 450 + i * 40 <= x <= 480 + i * 40 and 25 <= y <= 55:
                            current_color = color
                    continue

                canvas_pos = (x, y - UI_HEIGHT)

                if current_tool == 'fill':
                    action_history.append(canvas.copy())
                    flood_fill(canvas, canvas_pos, current_color)
                elif current_tool == 'text':
                    typing = True
                    text_input = ""
                    text_pos = event.pos
                else:
                    drawing = True
                    start_pos = canvas_pos
                    typing = False
                    action_history.append(canvas.copy())

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                canvas_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                if current_tool == 'pencil':
                    pygame.draw.line(canvas, current_color, start_pos, canvas_pos, brush_size)
                    start_pos = canvas_pos
                elif current_tool == 'eraser':
                    pygame.draw.line(canvas, WHITE, start_pos, canvas_pos, brush_size * 2) #eraser is a bit thicker
                    start_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                canvas_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                
                #draw shapes on mouse release
                shape_tools = ['line', 'rect', 'circle', 'square', 'right_tri', 'eq_tri', 'rhombus']
                if current_tool in shape_tools:
                    draw_shape(canvas, current_tool, start_pos, canvas_pos, current_color, brush_size)

    #prieviews while drawing shapes
    shape_tools = ['line', 'rect', 'circle', 'square', 'right_tri', 'eq_tri', 'rhombus']
    if drawing and current_tool in shape_tools:
        mouse_pos = pygame.mouse.get_pos()
        preview_start = (start_pos[0], start_pos[1] + UI_HEIGHT)
        draw_shape(screen, current_tool, preview_start, mouse_pos, current_color, brush_size)

    #preview text input
    if typing:
        txt_surf = font.render(text_input + ("|" if pygame.time.get_ticks() % 1000 < 500 else ""), True, current_color)
        screen.blit(txt_surf, text_pos)
    
    draw_ui()
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
sys.exit()