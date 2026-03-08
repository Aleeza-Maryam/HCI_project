import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Pong Game")
clock = pygame.time.Clock()

class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 7
        self.color = color
        
    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            
    def draw(self, screen):
        # Draw shadow
        shadow_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, 
                                 PADDLE_WIDTH, PADDLE_HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=8)
        
        # Draw gradient paddle
        for i in range(PADDLE_HEIGHT):
            # Calculate gradient color
            gradient_factor = i / PADDLE_HEIGHT
            r = int(self.color[0] * (1 - gradient_factor * 0.3))
            g = int(self.color[1] * (1 - gradient_factor * 0.3))
            b = int(self.color[2] * (1 - gradient_factor * 0.3))
            
            pygame.draw.line(screen, (r, g, b), 
                           (self.rect.x, self.rect.y + i),
                           (self.rect.x + PADDLE_WIDTH, self.rect.y + i))
        
        # Draw border
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)
        
    def ai_move(self, ball):
        """Simple AI for single-player mode"""
        if self.rect.centery < ball.rect.centery - 20:
            self.move(up=False)
        elif self.rect.centery > ball.rect.centery + 20:
            self.move(up=True)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, 
                               BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-5, 5])
        self.dy = random.choice([-4, -3, -2, 2, 3, 4])
        self.trail = []  # For particle trail
        self.color = (255, 255, 255)
        
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Add current position to trail
        self.trail.append((self.rect.centerx, self.rect.centery, 
                          pygame.time.get_ticks()))
        
        # Remove old trail points (older than 500ms)
        current_time = pygame.time.get_ticks()
        self.trail = [(x, y, t) for x, y, t in self.trail if current_time - t < 500]
        
        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1
            return True  # Return True for wall hit
        return False
        
    def draw(self, screen):
        # Draw trail particles
        for i, (x, y, t) in enumerate(self.trail):
            alpha = int(255 * (1 - i / len(self.trail)) * 0.5)
            radius = int(BALL_SIZE * (1 - i / len(self.trail)))
            
            if radius > 0:
                # Create surface with alpha for trail particle
                trail_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surf, (255, 255, 255, alpha), 
                                 (radius, radius), radius)
                screen.blit(trail_surf, (x - radius, y - radius))
        
        # Draw ball with 3D effect
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_SIZE)
        
        # Draw highlight
        highlight_pos = (self.rect.centerx - BALL_SIZE//3, 
                        self.rect.centery - BALL_SIZE//3)
        pygame.draw.circle(screen, (255, 255, 255, 200), highlight_pos, BALL_SIZE//3)
        
    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.dx = random.choice([-5, 5])
        self.dy = random.choice([-4, -3, -2, 2, 3, 4])
        self.trail = []

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
        return self.lifetime > 0
        
    def draw(self, screen):
        alpha = int(255 * (self.lifetime / 40))
        if alpha > 0:
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), 
                             (self.size, self.size), self.size)
            screen.blit(surf, (self.x - self.size, self.y - self.size))

def create_gradient_background(width, height):
    """Create a gradient background surface"""
    gradient = pygame.Surface((width, height))
    
    for y in range(height):
        # Create gradient from dark blue (top) to black (bottom)
        r = int(20 * (1 - y / height))
        g = int(40 * (1 - y / height))
        b = int(100 * (1 - y / height))
        
        pygame.draw.line(gradient, (r, g, b), (0, y), (width, y))
    
    # Add some stars
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        brightness = random.randint(100, 200)
        pygame.draw.circle(gradient, (brightness, brightness, brightness), 
                         (x, y), 1)
    
    return gradient

def draw_score(screen, left_score, right_score):
    font = pygame.font.Font(None, 100)
    
    # Left score with shadow
    left_shadow = font.render(str(left_score), True, (50, 50, 150))
    screen.blit(left_shadow, (WIDTH//4 + 4, 24))
    left_text = font.render(str(left_score), True, (100, 200, 255))
    screen.blit(left_text, (WIDTH//4, 20))
    
    # Right score with shadow
    right_shadow = font.render(str(right_score), True, (150, 50, 50))
    screen.blit(right_shadow, (3*WIDTH//4 + 4, 24))
    right_text = font.render(str(right_score), True, (255, 100, 100))
    screen.blit(right_text, (3*WIDTH//4, 20))
    
    # Draw score separator
    font_small = pygame.font.Font(None, 50)
    separator = font_small.render(":", True, WHITE)
    screen.blit(separator, (WIDTH//2 - separator.get_width()//2, 30))

def draw_net(screen):
    """Draw the center net with glow effect"""
    for y in range(0, HEIGHT, 35):
        # Glow effect (outer)
        pygame.draw.rect(screen, (100, 100, 255, 100), 
                        (WIDTH//2 - 4, y, 8, 20), border_radius=4)
        # Main net line
        pygame.draw.rect(screen, (200, 200, 255), 
                        (WIDTH//2 - 2, y, 4, 20), border_radius=2)

def create_sound_effect(frequency=440, duration=100):
    """Create a simple sound effect if no sound file is available"""
    sample_rate = 22050
    n_samples = int(round(duration * 0.001 * sample_rate))
    
    buf = bytearray()
    for i in range(n_samples):
        sample = int(127.0 * (i * frequency * 2 * 3.14159 / sample_rate))
        buf.append(128 + int(sample))
    
    return pygame.mixer.Sound(buffer=bytes(buf))

def main():
    # Create game objects
    player1 = Paddle(30, HEIGHT//2 - PADDLE_HEIGHT//2, (100, 150, 255))
    player2 = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, (255, 100, 100))
    ball = Ball()
    
    # Game state
    scores = [0, 0]
    single_player = True
    game_state = "PLAYING"  # PLAYING, PAUSED, GAME_OVER
    winner = None
    particles = []
    
    # Pre-render gradient background
    background = create_gradient_background(WIDTH, HEIGHT)
    
    # Try to load sounds, create simple ones if files not found
    try:
        pygame.mixer.init()
        
        # Create simple sound effects
        paddle_sound = create_sound_effect(660, 50)
        wall_sound = create_sound_effect(440, 50)
        score_sound = create_sound_effect(880, 150)
        
        # Try to load actual sound files if they exist
        sound_dir = "sounds"
        if os.path.exists(sound_dir):
            if os.path.exists(os.path.join(sound_dir, "paddle_hit.wav")):
                paddle_sound = pygame.mixer.Sound(os.path.join(sound_dir, "paddle_hit.wav"))
            if os.path.exists(os.path.join(sound_dir, "wall_hit.wav")):
                wall_sound = pygame.mixer.Sound(os.path.join(sound_dir, "wall_hit.wav"))
            if os.path.exists(os.path.join(sound_dir, "score.wav")):
                score_sound = pygame.mixer.Sound(os.path.join(sound_dir, "score.wav"))
            if os.path.exists(os.path.join(sound_dir, "background.mp3")):
                pygame.mixer.music.load(os.path.join(sound_dir, "background.mp3"))
                pygame.mixer.music.play(-1)
                
    except:
        print("Sound initialization failed - continuing without sound")
        paddle_sound = None
        wall_sound = None
        score_sound = None
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    single_player = not single_player
                elif event.key == pygame.K_p:
                    game_state = "PAUSED" if game_state == "PLAYING" else "PLAYING"
                elif event.key == pygame.K_r and game_state == "GAME_OVER":
                    # Reset game
                    scores = [0, 0]
                    ball.reset()
                    player1.rect.y = HEIGHT//2 - PADDLE_HEIGHT//2
                    player2.rect.y = HEIGHT//2 - PADDLE_HEIGHT//2
                    game_state = "PLAYING"
                    winner = None
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Draw background
        screen.blit(background, (0, 0))
        
        if game_state == "PLAYING":
            # Player controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player1.move(up=True)
            if keys[pygame.K_s]:
                player1.move(up=False)
            
            if not single_player:
                if keys[pygame.K_UP]:
                    player2.move(up=True)
                if keys[pygame.K_DOWN]:
                    player2.move(up=False)
            else:
                player2.ai_move(ball)
            
            # Move ball and check for wall hits
            wall_hit = ball.move()
            if wall_hit and wall_sound:
                wall_sound.play()
            
            # Ball collision with paddles
            if ball.rect.colliderect(player1.rect) and ball.dx < 0:
                ball.dx *= -1.1  # Slightly increase speed
                ball.dy = random.choice([-4, -3, -2, 2, 3, 4])
                
                # Create particles on hit
                for _ in range(10):
                    particles.append(Particle(ball.rect.centerx, ball.rect.centery, 
                                            (100, 150, 255)))
                
                if paddle_sound:
                    paddle_sound.play()
                    
            if ball.rect.colliderect(player2.rect) and ball.dx > 0:
                ball.dx *= -1.1
                ball.dy = random.choice([-4, -3, -2, 2, 3, 4])
                
                # Create particles on hit
                for _ in range(10):
                    particles.append(Particle(ball.rect.centerx, ball.rect.centery, 
                                            (255, 100, 100)))
                
                if paddle_sound:
                    paddle_sound.play()
            
            # Score points
            if ball.rect.left <= 0:
                scores[1] += 1
                if score_sound:
                    score_sound.play()
                ball.reset()
                if scores[1] >= 5:  # Winning score
                    game_state = "GAME_OVER"
                    winner = "Player 2" if not single_player else "AI"
                    
            if ball.rect.right >= WIDTH:
                scores[0] += 1
                if score_sound:
                    score_sound.play()
                ball.reset()
                if scores[0] >= 5:  # Winning score
                    game_state = "GAME_OVER"
                    winner = "Player 1"
        
        # Update particles
        particles = [p for p in particles if p.update()]
        
        # Draw game elements
        draw_net(screen)
        
        # Draw particles
        for particle in particles:
            particle.draw(screen)
        
        # Draw paddles and ball
        player1.draw(screen)
        player2.draw(screen)
        ball.draw(screen)
        
        # Draw score
        draw_score(screen, scores[0], scores[1])
        
        # Draw game info
        font = pygame.font.Font(None, 30)
        
        # Game mode info
        mode_text = "Single Player" if single_player else "Two Players"
        mode_display = font.render(f"Mode: {mode_text}", True, WHITE)
        mode_bg = pygame.Surface((mode_display.get_width() + 20, 
                                 mode_display.get_height() + 10), 
                                pygame.SRCALPHA)
        mode_bg.fill((0, 0, 0, 150))
        screen.blit(mode_bg, (10, HEIGHT - 40))
        screen.blit(mode_display, (20, HEIGHT - 35))
        
        # Controls info
        controls_text = font.render("SPACE: Toggle Mode | P: Pause | R: Restart | ESC: Quit", 
                                   True, (200, 200, 200))
        controls_bg = pygame.Surface((controls_text.get_width() + 20, 
                                     controls_text.get_height() + 10), 
                                    pygame.SRCALPHA)
        controls_bg.fill((0, 0, 0, 150))
        screen.blit(controls_bg, (WIDTH - controls_text.get_width() - 30, HEIGHT - 40))
        screen.blit(controls_text, (WIDTH - controls_text.get_width() - 20, HEIGHT - 35))
        
        # Draw game state overlays
        if game_state == "PAUSED":
            # Dark overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            # Paused text
            pause_font = pygame.font.Font(None, 80)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 100))
            pause_shadow = pause_font.render("PAUSED", True, (100, 100, 0))
            
            screen.blit(pause_shadow, 
                       (WIDTH//2 - pause_text.get_width()//2 + 4, 
                        HEIGHT//2 - pause_text.get_height()//2 + 4))
            screen.blit(pause_text, 
                       (WIDTH//2 - pause_text.get_width()//2, 
                        HEIGHT//2 - pause_text.get_height()//2))
            
            # Instruction
            inst_font = pygame.font.Font(None, 36)
            inst_text = inst_font.render("Press 'P' to resume", True, WHITE)
            screen.blit(inst_text, 
                       (WIDTH//2 - inst_text.get_width()//2, 
                        HEIGHT//2 + 60))
        
        elif game_state == "GAME_OVER":
            # Dark overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # Game over text
            go_font = pygame.font.Font(None, 90)
            go_text = go_font.render("GAME OVER", True, (255, 50, 50))
            go_shadow = go_font.render("GAME OVER", True, (100, 0, 0))
            
            screen.blit(go_shadow, 
                       (WIDTH//2 - go_text.get_width()//2 + 4, 
                        HEIGHT//2 - 100 + 4))
            screen.blit(go_text, 
                       (WIDTH//2 - go_text.get_width()//2, 
                        HEIGHT//2 - 100))
            
            # Winner text
            if winner:
                win_font = pygame.font.Font(None, 60)
                win_text = win_font.render(f"{winner} WINS!", True, (50, 255, 50))
                win_shadow = win_font.render(f"{winner} WINS!", True, (0, 100, 0))
                
                screen.blit(win_shadow, 
                           (WIDTH//2 - win_text.get_width()//2 + 3, 
                            HEIGHT//2 + 3))
                screen.blit(win_text, 
                           (WIDTH//2 - win_text.get_width()//2, 
                            HEIGHT//2))
            
            # Final score
            score_font = pygame.font.Font(None, 48)
            score_text = score_font.render(f"Final Score: {scores[0]} - {scores[1]}", 
                                          True, WHITE)
            screen.blit(score_text, 
                       (WIDTH//2 - score_text.get_width()//2, 
                        HEIGHT//2 + 70))
            
            # Restart instruction
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("Press 'R' to restart or ESC to quit", 
                                              True, (200, 200, 200))
            screen.blit(restart_text, 
                       (WIDTH//2 - restart_text.get_width()//2, 
                        HEIGHT//2 + 140))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()