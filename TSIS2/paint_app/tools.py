import pygame, os, math
from datetime import datetime


def flood_fill(surface, pos, fill_color):
    #fills a closed region with fill_colors, DFS algo is used
    target_color = surface.get_at(pos)
    fill_color_obj = pygame.Color(*fill_color)
    
    if target_color == fill_color_obj:
        return

    width, height = surface.get_size()
    stack = [pos]

    while stack:
        x, y = stack.pop()
        if 0 <= x < width and 0 <= y < height:
            if surface.get_at((x, y)) == target_color:
                surface.set_at((x, y), fill_color_obj)
                stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

def save_canvas(surface):
    #saves the canvas as a .png file with a timestamp
    save_dir = "assets"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"canvas_{timestamp}.png")
    pygame.image.save(surface, filename)
    print(f"Canvas saved successfully as: {filename}")

def draw_shape(surface, tool, start_pos, end_pos, color, size):
    #draws shapes based on start and end coordinates
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    if tool == 'line':
        pygame.draw.line(surface, color, start_pos, end_pos, size)
        
    elif tool == 'rect':
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x1-x2), abs(y1-y2))
        pygame.draw.rect(surface, color, rect)
        
    elif tool == 'circle':
        radius = int(((x1-x2)**2 + (y1-y2)**2)**0.5)
        pygame.draw.circle(surface, color, start_pos, radius)
        
    elif tool == 'square':
        side = min(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(min(x1, x2), min(y1, y2), side, side)
        pygame.draw.rect(surface, color, rect)
        
    elif tool == 'right_tri':
        #right triangle with right angle at start_pos
        pygame.draw.polygon(surface, color, [(x1, y1), (x1, y2), (x2, y2)])
        
    elif tool == 'eq_tri':
        #equilateral triangle
        side = abs(x2 - x1)
        height = int(side * math.sqrt(3) / 2)
        #points are start_pos, (x2, y2), and the third vertex calculated to form an eq_tr
        pygame.draw.polygon(surface, color, [(x1, y2), (x2, y2), ((x1+x2)//2, y2 - height)])
        
    elif tool == 'rhombus':
        #rhombus
        pygame.draw.polygon(surface, color, [
            ((x1+x2)//2, y1),
            (x2, (y1+y2)//2),
            ((x1+x2)//2, y2),
            (x1, (y1+y2)//2)
        ])