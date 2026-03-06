from vpython import *
import random
import time

# === SIMPLER 3D TETRIS - WORKING VERSION ===

# Game settings
GRID_SIZE = 6  # Smaller grid for better performance
CELL_SIZE = 1
score = 0
game_over = False

# Colors
colors = [color.red, color.green, color.blue, color.yellow, color.orange, color.purple, color.cyan]

# Simple 3D shapes (tetrominoes)
shapes = [
    # I-shape (straight line)
    [[0,0,0], [1,0,0], [2,0,0], [3,0,0]],
    
    # O-shape (square)
    [[0,0,0], [1,0,0], [0,1,0], [1,1,0]],
    
    # T-shape
    [[0,0,0], [1,0,0], [2,0,0], [1,1,0]],
    
    # L-shape
    [[0,0,0], [0,1,0], [0,2,0], [1,0,0]],
    
    # J-shape
    [[1,0,0], [1,1,0], [1,2,0], [0,2,0]],
    
    # S-shape
    [[0,1,0], [1,1,0], [1,0,0], [2,0,0]],
    
    # Z-shape
    [[0,0,0], [1,0,0], [1,1,0], [2,1,0]]
]

# Setup scene
scene = canvas(title='Simple 3D Tetris', width=900, height=700,
               center=vector(GRID_SIZE/2, GRID_SIZE/2, GRID_SIZE/2),
               background=color.black)

# Draw grid
for i in range(GRID_SIZE + 1):
    # X lines
    curve(pos=[vector(i, 0, 0), vector(i, GRID_SIZE, 0)], color=color.gray(0.3))
    curve(pos=[vector(i, 0, GRID_SIZE), vector(i, GRID_SIZE, GRID_SIZE)], color=color.gray(0.3))
    # Y lines
    curve(pos=[vector(0, i, 0), vector(GRID_SIZE, i, 0)], color=color.gray(0.3))
    curve(pos=[vector(0, i, GRID_SIZE), vector(GRID_SIZE, i, GRID_SIZE)], color=color.gray(0.3))
    # Z lines
    curve(pos=[vector(0, 0, i), vector(GRID_SIZE, 0, i)], color=color.gray(0.3))
    curve(pos=[vector(0, GRID_SIZE, i), vector(GRID_SIZE, GRID_SIZE, i)], color=color.gray(0.3))

# Game variables
grid = {}  # {(x,y,z): block}
current_piece = []
current_shape = None
current_color = None
current_pos = vector(GRID_SIZE//2, GRID_SIZE-2, GRID_SIZE//2)

# UI
score_label = label(pos=vector(-2, GRID_SIZE+2, 0), text='Score: 0', height=20, color=color.white)
game_over_label = label(pos=vector(GRID_SIZE/2, GRID_SIZE/2, GRID_SIZE/2), 
                       text='', height=30, color=color.red, visible=False)

# Instructions
instructions = label(pos=vector(-2, GRID_SIZE, 0), 
                    text='Controls:\nArrow Keys: Move\nA/D: Rotate\nSpace: Drop\nR: Restart', 
                    height=14, color=color.cyan)

def create_piece():
    """Create a new falling piece"""
    global current_piece, current_shape, current_color, current_pos
    
    # Clear old piece
    for block in current_piece:
        block.visible = False
    
    # Choose random shape and color
    current_shape = random.choice(shapes)
    current_color = random.choice(colors)
    current_pos = vector(GRID_SIZE//2, GRID_SIZE-2, GRID_SIZE//2)
    
    # Create new piece
    current_piece = []
    for block in current_shape:
        pos = current_pos + vector(block[0], block[1], block[2])
        b = box(pos=pos, size=vector(CELL_SIZE*0.9, CELL_SIZE*0.9, CELL_SIZE*0.9),
                color=current_color, opacity=0.8)
        current_piece.append(b)
    
    # Check if game over
    if not is_valid_position(current_pos):
        end_game()
        return False
    
    return True

def is_valid_position(pos):
    """Check if piece can be at this position"""
    for block in current_shape:
        x = int(pos.x + block[0])
        y = int(pos.y + block[1])
        z = int(pos.z + block[2])
        
        # Check bounds
        if x < 0 or x >= GRID_SIZE or y < 0 or z < 0 or z >= GRID_SIZE:
            return False
        
        # Check collision with placed blocks
        if (x, y, z) in grid:
            return False
    
    return True

def move_piece(dx, dy, dz):
    """Move the current piece"""
    global current_pos
    
    if game_over:
        return False
    
    new_pos = current_pos + vector(dx, dy, dz)
    
    if is_valid_position(new_pos):
        current_pos = new_pos
        for block in current_piece:
            block.pos += vector(dx, dy, dz)
        return True
    
    # If moving down failed, lock the piece
    if dy < 0:
        lock_piece()
        check_full_layers()
        create_piece()
    
    return False

def rotate_piece():
    """Simple rotation - just change color for now"""
    global current_color
    if game_over:
        return
    
    # Change color as visual feedback
    current_color = random.choice(colors)
    for block in current_piece:
        block.color = current_color

def lock_piece():
    """Lock the piece into the grid"""
    global grid
    
    for block in current_piece:
        x = int(round(block.pos.x))
        y = int(round(block.pos.y))
        z = int(round(block.pos.z))
        
        block.opacity = 1.0
        grid[(x, y, z)] = block

def check_full_layers():
    """Check for full horizontal layers"""
    global score, grid
    
    # Simple layer checking - just Y layers
    for y in range(GRID_SIZE):
        full = True
        for x in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                if (x, y, z) not in grid:
                    full = False
                    break
        
        if full:
            # Remove this layer
            for x in range(GRID_SIZE):
                for z in range(GRID_SIZE):
                    if (x, y, z) in grid:
                        grid[(x, y, z)].visible = False
                        del grid[(x, y, z)]
            
            # Move blocks above down
            for y_above in range(y + 1, GRID_SIZE):
                for x in range(GRID_SIZE):
                    for z in range(GRID_SIZE):
                        if (x, y_above, z) in grid:
                            block = grid.pop((x, y_above, z))
                            block.pos.y -= 1
                            grid[(x, y_above - 1, z)] = block
            
            score += 100
            score_label.text = f'Score: {score}'

def end_game():
    """End the game"""
    global game_over
    game_over = True
    game_over_label.text = f'GAME OVER\nScore: {score}'
    game_over_label.visible = True

def restart_game():
    """Restart the game"""
    global grid, score, game_over, current_piece
    
    # Clear grid
    for block in grid.values():
        block.visible = False
    grid = {}
    
    # Clear current piece
    for block in current_piece:
        block.visible = False
    current_piece = []
    
    # Reset variables
    score = 0
    game_over = False
    score_label.text = 'Score: 0'
    game_over_label.visible = False
    
    # Start new game
    create_piece()

# Keyboard handling using scene.bind
def keydown(evt):
    """Handle key presses"""
    key = evt.key
    
    if game_over:
        if key == 'r':
            restart_game()
        return
    
    if key == 'left':
        move_piece(-1, 0, 0)
    elif key == 'right':
        move_piece(1, 0, 0)
    elif key == 'up':
        move_piece(0, 0, 1)
    elif key == 'down':
        move_piece(0, 0, -1)
    elif key == ' ':
        # Hard drop
        while move_piece(0, -1, 0):
            pass
    elif key == 'a':
        rotate_piece()
    elif key == 'r':
        restart_game()

# Bind keyboard events
scene.bind('keydown', keydown)

# Initialize game
create_piece()
last_fall_time = time.time()

# Main game loop
while True:
    rate(30)  # Control game speed
    
    # Automatic falling
    if not game_over and time.time() - last_fall_time > 0.5:
        move_piece(0, -1, 0)
        last_fall_time = time.time()