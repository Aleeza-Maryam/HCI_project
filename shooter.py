import pygame
import random
import math
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 200)
ORANGE = (255, 150, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BACKGROUND = (20, 20, 35)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        self.hovered = False
        self.clicked = False
        
    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def check_click(self, pos, click):
        if self.rect.collidepoint(pos) and click:
            self.clicked = True
            return True
        self.clicked = False
        return False

class Player:
    def __init__(self, x, y):
        # 3D position (x, y, z) - z is depth
        self.x = x
        self.y = y
        self.z = 0  # Player is at depth 0 (closest)
        
        # Movement
        self.speed = 5
        self.width = 40
        self.height = 60
        self.color = BLUE
        
        # Health
        self.health = 100
        self.max_health = 100
        self.invincible = False
        self.invincible_timer = 0
        
        # Shooting
        self.bullets = 30
        self.max_bullets = 30
        self.reloading = False
        self.reload_time = 0
        self.reload_duration = 60  # frames
        
        # 3D perspective
        self.perspective_factor = 0.8
        
    def move(self, dx, dy, boundaries):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Keep within boundaries
        if 0 <= new_x <= boundaries[0] - self.width:
            self.x = new_x
        if 0 <= new_y <= boundaries[1] - self.height:
            self.y = new_y
            
    def shoot(self):
        if self.bullets > 0 and not self.reloading:
            self.bullets -= 1
            return Bullet(self.x + self.width//2, self.y, 0)
        return None
        
    def start_reload(self):
        if not self.reloading and self.bullets < self.max_bullets:
            self.reloading = True
            self.reload_time = 0
            return True
        return False
        
    def update(self):
        if self.reloading:
            self.reload_time += 1
            if self.reload_time >= self.reload_duration:
                self.reloading = False
                self.bullets = self.max_bullets
                
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
                
    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            self.invincible = True
            self.invincible_timer = 30  # 0.5 seconds
            return True
        return False
        
    def draw(self, screen):
        # Draw player with 3D perspective (darker as it goes up)
        color = self.color
        if self.invincible and pygame.time.get_ticks() % 200 < 100:
            color = WHITE
            
        # Draw 3D-like box
        base_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        top_rect = pygame.Rect(self.x - 5, self.y - 10, self.width + 10, self.height + 5)
        
        pygame.draw.rect(screen, (color[0]//2, color[1]//2, color[2]//2), base_rect)
        pygame.draw.rect(screen, color, top_rect, border_radius=5)
        
        # Draw face/eyes
        pygame.draw.circle(screen, WHITE, (int(self.x + self.width//3), int(self.y + self.height//3)), 5)
        pygame.draw.circle(screen, WHITE, (int(self.x + 2*self.width//3), int(self.y + self.height//3)), 5)
        
    def get_screen_pos(self):
        # Convert 3D position to screen position with perspective
        screen_x = self.x
        screen_y = self.y - self.z * self.perspective_factor
        return screen_x, screen_y

class Enemy:
    def __init__(self, pattern_type, difficulty):
        self.pattern_type = pattern_type
        self.difficulty = difficulty
        
        # Set initial position based on pattern
        if pattern_type == "left_right":
            self.x = random.choice([-50, SCREEN_WIDTH])
            self.y = random.randint(100, SCREEN_HEIGHT - 200)
            self.dx = random.choice([-2, 2]) * (1 + difficulty * 0.5)
            self.dy = 0
        elif pattern_type == "up_down":
            self.x = random.randint(100, SCREEN_WIDTH - 100)
            self.y = random.choice([-50, SCREEN_HEIGHT])
            self.dx = 0
            self.dy = random.choice([-2, 2]) * (1 + difficulty * 0.5)
        else:  # straight line
            angle = random.uniform(0, 2 * math.pi)
            speed = 2 * (1 + difficulty * 0.5)
            self.dx = math.cos(angle) * speed
            self.dy = math.sin(angle) * speed
            
            # Start from edge
            if abs(self.dx) > abs(self.dy):
                self.x = -50 if self.dx > 0 else SCREEN_WIDTH + 50
                self.y = random.randint(100, SCREEN_HEIGHT - 100)
            else:
                self.x = random.randint(100, SCREEN_WIDTH - 100)
                self.y = -50 if self.dy > 0 else SCREEN_HEIGHT + 50
        
        # 3D properties
        self.z = random.randint(50, 200)  # Depth
        self.size = 40 - self.z * 0.1  # Smaller when farther
        
        # Enemy properties
        self.color = random.choice([RED, ORANGE, PURPLE])
        self.health = 30
        self.value = 10 * (difficulty + 1)
        
        # Movement pattern variables
        self.pattern_timer = 0
        self.pattern_duration = random.randint(60, 120)
        
    def update(self):
        # Update position based on pattern
        if self.pattern_type == "left_right":
            self.x += self.dx
            # Reverse direction at edges
            if self.x < -100 or self.x > SCREEN_WIDTH + 100:
                self.dx *= -1
                
        elif self.pattern_type == "up_down":
            self.y += self.dy
            # Reverse direction at edges
            if self.y < -100 or self.y > SCREEN_HEIGHT + 100:
                self.dy *= -1
                
        else:  # straight line
            self.x += self.dx
            self.y += self.dy
            
        # Update pattern timer
        self.pattern_timer += 1
        if self.pattern_timer >= self.pattern_duration:
            self.pattern_timer = 0
            # Occasionally change direction slightly
            if random.random() < 0.3:
                angle = math.atan2(self.dy, self.dx) + random.uniform(-0.5, 0.5)
                speed = math.sqrt(self.dx**2 + self.dy**2)
                self.dx = math.cos(angle) * speed
                self.dy = math.sin(angle) * speed
                
    def draw(self, screen):
        # Draw enemy with 3D perspective
        screen_x = self.x
        screen_y = self.y - self.z * 0.5
        
        # Size decreases with distance
        draw_size = max(20, self.size)
        
        # Create 3D effect with multiple circles
        pygame.draw.circle(screen, 
                          (self.color[0]//2, self.color[1]//2, self.color[2]//2),
                          (int(screen_x), int(screen_y + draw_size//3)),
                          draw_size//2)
        
        pygame.draw.circle(screen, self.color,
                          (int(screen_x), int(screen_y)),
                          draw_size//2)
        
        # Draw eyes
        eye_offset = draw_size // 4
        pygame.draw.circle(screen, BLACK,
                          (int(screen_x - eye_offset), int(screen_y - eye_offset//2)),
                          draw_size//6)
        pygame.draw.circle(screen, BLACK,
                          (int(screen_x + eye_offset), int(screen_y - eye_offset//2)),
                          draw_size//6)
        
    def get_hitbox(self):
        # Simple rectangle hitbox for collision
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        
    def is_off_screen(self):
        return (self.x < -200 or self.x > SCREEN_WIDTH + 200 or 
                self.y < -200 or self.y > SCREEN_HEIGHT + 200)

class Bullet:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.speed = 10
        self.size = 8
        self.color = YELLOW
        
    def update(self):
        self.y -= self.speed
        
    def draw(self, screen):
        # Draw bullet with trail for 3D effect
        screen_y = self.y - self.z * 0.3
        
        # Bullet body
        pygame.draw.circle(screen, self.color,
                          (int(self.x), int(screen_y)),
                          self.size//2)
        
        # Light core
        pygame.draw.circle(screen, WHITE,
                          (int(self.x), int(screen_y)),
                          self.size//4)
        
        # Trail
        for i in range(3):
            trail_y = screen_y + self.speed * i * 0.5
            trail_size = self.size * (1 - i * 0.3)
            pygame.draw.circle(screen, ORANGE,
                              (int(self.x), int(trail_y)),
                              trail_size//2)
        
    def get_hitbox(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        
    def is_off_screen(self):
        return self.y < -50

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.z = random.randint(0, 100)
        self.power_type = power_type
        self.size = 30
        self.speed = 1
        self.float_offset = 0
        
        # Set color based on type
        if power_type == "shield":
            self.color = BLUE
        elif power_type == "rapid_fire":
            self.color = GREEN
        elif power_type == "double_score":
            self.color = YELLOW
        elif power_type == "health":
            self.color = RED
            
    def update(self):
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.005) * 5
        
    def draw(self, screen):
        screen_y = self.y + self.float_offset - self.z * 0.3
        
        # Draw with 3D effect
        pygame.draw.circle(screen, 
                          (self.color[0]//2, self.color[1]//2, self.color[2]//2),
                          (int(self.x), int(screen_y + self.size//4)),
                          self.size//2)
        
        pygame.draw.circle(screen, self.color,
                          (int(self.x), int(screen_y)),
                          self.size//2)
        
        # Draw symbol
        font = pygame.font.SysFont(None, 24)
        if self.power_type == "shield":
            symbol = "S"
        elif self.power_type == "rapid_fire":
            symbol = "R"
        elif self.power_type == "double_score":
            symbol = "2X"
        elif self.power_type == "health":
            symbol = "+"
            
        text = font.render(symbol, True, WHITE)
        text_rect = text.get_rect(center=(self.x, screen_y))
        screen.blit(text, text_rect)
        
    def get_hitbox(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

class Game:
    def __init__(self):
        # Initialize settings first
        self.sound_on = True
        self.music_on = True
        self.button_size = 1.0
        self.high_contrast = False
        self.vibration_enabled = True
        self.difficulty = 1  # 0: easy, 1: medium, 2: hard
        
        # Now setup screen and other components
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("3D Shooter Game - HCI Project")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.small_font = pygame.font.SysFont(None, 24)
        
        # Game states
        self.state = "menu"  # menu, playing, settings, game_over
        
        # Game objects
        self.player = None
        self.enemies = []
        self.bullets = []
        self.powerups = []
        self.particles = []
        
        # Game stats
        self.score = 0
        self.high_score = 0
        self.game_time = 0
        self.enemy_spawn_timer = 0
        self.powerup_spawn_timer = 0
        
        # Power-up effects
        self.shield_active = False
        self.shield_timer = 0
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.double_score = False
        self.double_score_timer = 0
        
        # Controls
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        
        # Touch controls (for mobile-like interface)
        self.touch_controls = {
            "left": pygame.Rect(50, SCREEN_HEIGHT - 150, 100, 100),
            "right": pygame.Rect(200, SCREEN_HEIGHT - 150, 100, 100),
            "shoot": pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 150, 100, 100),
            "reload": pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150, 100, 100),
            "jump": pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 150, 100, 100)
        }
        
        # Load sounds (simulated - you can add actual sound files)
        self.shoot_sound = None
        self.hit_sound = None
        self.reload_sound = None
        
        # Create UI elements after settings are initialized
        self.create_ui_elements()
        
    def create_ui_elements(self):
        # Menu buttons
        self.start_button = Button(SCREEN_WIDTH//2 - 100, 300, 200, 60, 
                                  "START GAME", GREEN, (100, 255, 100))
        self.settings_button = Button(SCREEN_WIDTH//2 - 100, 380, 200, 60,
                                     "SETTINGS", BLUE, (100, 150, 255))
        self.quit_button = Button(SCREEN_WIDTH//2 - 100, 460, 200, 60,
                                 "QUIT", RED, (255, 100, 100))
        
        # Difficulty buttons
        self.easy_button = Button(SCREEN_WIDTH//2 - 150, 250, 140, 50,
                                 "EASY", GREEN, (100, 255, 100))
        self.medium_button = Button(SCREEN_WIDTH//2, 250, 140, 50,
                                   "MEDIUM", YELLOW, (255, 255, 100))
        self.hard_button = Button(SCREEN_WIDTH//2 + 150, 250, 140, 50,
                                 "HARD", RED, (255, 100, 100))
        
        # Settings buttons
        sound_text = "SOUND: ON" if self.sound_on else "SOUND: OFF"
        music_text = "MUSIC: ON" if self.music_on else "MUSIC: OFF"
        contrast_text = "HIGH CONTRAST: OFF"
        
        self.sound_toggle = Button(SCREEN_WIDTH//2 - 100, 250, 200, 50,
                                  sound_text, BLUE, (100, 150, 255))
        self.music_toggle = Button(SCREEN_WIDTH//2 - 100, 320, 200, 50,
                                  music_text, BLUE, (100, 150, 255))
        self.contrast_toggle = Button(SCREEN_WIDTH//2 - 100, 390, 200, 50,
                                      contrast_text, BLUE, (100, 150, 255))
        self.back_button = Button(SCREEN_WIDTH//2 - 100, 500, 200, 50,
                                 "BACK", GRAY, DARK_GRAY)
        
        # Game over buttons
        self.restart_button = Button(SCREEN_WIDTH//2 - 150, 400, 140, 50,
                                    "RESTART", GREEN, (100, 255, 100))
        self.menu_button = Button(SCREEN_WIDTH//2 + 10, 400, 140, 50,
                                 "MENU", BLUE, (100, 150, 255))
        
    def start_game(self):
        self.state = "playing"
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT - 150)
        self.enemies = []
        self.bullets = []
        self.powerups = []
        self.particles = []
        
        self.score = 0
        self.game_time = 0
        self.enemy_spawn_timer = 0
        self.powerup_spawn_timer = 0
        
        self.shield_active = False
        self.shield_timer = 0
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.double_score = False
        self.double_score_timer = 0
        
    def spawn_enemy(self):
        pattern = random.choice(["left_right", "up_down", "straight"])
        enemy = Enemy(pattern, self.difficulty)
        self.enemies.append(enemy)
        
    def spawn_powerup(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 200)
        power_type = random.choice(["shield", "rapid_fire", "double_score", "health"])
        powerup = PowerUp(x, y, power_type)
        self.powerups.append(powerup)
        
    def create_particles(self, x, y, color, count=10):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            size = random.randint(2, 6)
            lifetime = random.randint(20, 40)
            self.particles.append({
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': size,
                'color': color,
                'lifetime': lifetime
            })
            
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                
    def draw_particles(self):
        for particle in self.particles:
            alpha = particle['lifetime'] / 40 * 255
            color = list(particle['color'])
            if len(color) == 3:
                color.append(int(alpha))
                
            pygame.draw.circle(self.screen, color[:3],
                              (int(particle['x']), int(particle['y'])),
                              particle['size'])
                              
    def activate_powerup(self, power_type):
        if power_type == "shield":
            self.shield_active = True
            self.shield_timer = 600  # 10 seconds
        elif power_type == "rapid_fire":
            self.rapid_fire = True
            self.rapid_fire_timer = 450  # 7.5 seconds
        elif power_type == "double_score":
            self.double_score = True
            self.double_score_timer = 300  # 5 seconds
        elif power_type == "health":
            self.player.health = min(self.player.max_health, self.player.health + 30)
            
    def update_powerups(self):
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
                
        if self.rapid_fire:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire = False
                
        if self.double_score:
            self.double_score_timer -= 1
            if self.double_score_timer <= 0:
                self.double_score = False
                
    def handle_collisions(self):
        # Bullet-enemy collisions
        for bullet in self.bullets[:]:
            bullet_hitbox = bullet.get_hitbox()
            
            for enemy in self.enemies[:]:
                if bullet_hitbox.colliderect(enemy.get_hitbox()):
                    enemy.health -= 10
                    
                    # Create hit particles
                    self.create_particles(bullet.x, bullet.y, YELLOW, 5)
                    
                    if enemy.health <= 0:
                        # Add score
                        score_to_add = enemy.value
                        if self.double_score:
                            score_to_add *= 2
                        self.score += score_to_add
                        
                        # Create explosion
                        self.create_particles(enemy.x, enemy.y, enemy.color, 15)
                        
                        # Random chance to drop powerup
                        if random.random() < 0.2:
                            self.spawn_powerup()
                            
                        self.enemies.remove(enemy)
                        
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break
                    
        # Player-enemy collisions
        if not self.shield_active:
            player_hitbox = pygame.Rect(self.player.x, self.player.y, 
                                       self.player.width, self.player.height)
            
            for enemy in self.enemies[:]:
                if player_hitbox.colliderect(enemy.get_hitbox()):
                    if self.player.take_damage(20):
                        # Create damage particles
                        self.create_particles(self.player.x + self.player.width//2,
                                            self.player.y + self.player.height//2,
                                            RED, 8)
                        
                        # Remove enemy on collision
                        self.create_particles(enemy.x, enemy.y, enemy.color, 10)
                        self.enemies.remove(enemy)
                        
        # Player-powerup collisions
        player_hitbox = pygame.Rect(self.player.x, self.player.y,
                                   self.player.width, self.player.height)
        
        for powerup in self.powerups[:]:
            if player_hitbox.colliderect(powerup.get_hitbox()):
                self.activate_powerup(powerup.power_type)
                self.create_particles(powerup.x, powerup.y, powerup.color, 8)
                self.powerups.remove(powerup)
                
    def draw_ui(self):
        if self.state == "playing":
            # Draw HUD
            # Health bar
            health_width = 200
            health_height = 20
            health_x = 20
            health_y = 20
            
            # Health bar background
            pygame.draw.rect(self.screen, RED,
                            (health_x, health_y, health_width, health_height))
            
            # Health bar fill
            health_ratio = self.player.health / self.player.max_health
            pygame.draw.rect(self.screen, GREEN,
                            (health_x, health_y, health_width * health_ratio, health_height))
            
            # Health bar border
            pygame.draw.rect(self.screen, WHITE,
                            (health_x, health_y, health_width, health_height), 2)
            
            # Health text
            health_text = self.font.render(f"Health: {int(self.player.health)}", True, WHITE)
            self.screen.blit(health_text, (health_x, health_y + health_height + 5))
            
            # Ammo display
            ammo_x = 20
            ammo_y = 70
            
            # Ammo bar
            ammo_width = 200
            ammo_height = 20
            ammo_ratio = self.player.bullets / self.player.max_bullets
            
            pygame.draw.rect(self.screen, DARK_GRAY,
                            (ammo_x, ammo_y, ammo_width, ammo_height))
            
            ammo_color = YELLOW if not self.player.reloading else GRAY
            pygame.draw.rect(self.screen, ammo_color,
                            (ammo_x, ammo_y, ammo_width * ammo_ratio, ammo_height))
            
            pygame.draw.rect(self.screen, WHITE,
                            (ammo_x, ammo_y, ammo_width, ammo_height), 2)
            
            # Ammo text
            if self.player.reloading:
                reload_progress = self.player.reload_time / self.player.reload_duration
                ammo_text = self.font.render(f"Reloading... {int(reload_progress * 100)}%", True, WHITE)
            else:
                ammo_text = self.font.render(f"Ammo: {self.player.bullets}/{self.player.max_bullets}", True, WHITE)
            self.screen.blit(ammo_text, (ammo_x, ammo_y + ammo_height + 5))
            
            # Score display
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (SCREEN_WIDTH - 200, 20))
            
            # Time display
            time_text = self.font.render(f"Time: {self.game_time//60}:{self.game_time%60:02d}", True, WHITE)
            self.screen.blit(time_text, (SCREEN_WIDTH - 200, 60))
            
            # Power-up indicators
            indicator_y = 120
            if self.shield_active:
                shield_text = self.small_font.render(f"SHIELD: {self.shield_timer//60}", True, BLUE)
                self.screen.blit(shield_text, (20, indicator_y))
                indicator_y += 25
                
            if self.rapid_fire:
                rapid_text = self.small_font.render(f"RAPID FIRE: {self.rapid_fire_timer//60}", True, GREEN)
                self.screen.blit(rapid_text, (20, indicator_y))
                indicator_y += 25
                
            if self.double_score:
                double_text = self.small_font.render(f"2X SCORE: {self.double_score_timer//60}", True, YELLOW)
                self.screen.blit(double_text, (20, indicator_y))
                
            # Draw touch controls (large buttons for HCI)
            if self.high_contrast:
                btn_color = WHITE
                border_color = BLACK
                text_color = BLACK
            else:
                btn_color = (100, 100, 100, 150)
                border_color = WHITE
                text_color = WHITE
                
            for control_name, rect in self.touch_controls.items():
                # Draw button background
                s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                s.fill(btn_color)
                self.screen.blit(s, rect)
                
                # Draw button border
                pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=15)
                
                # Draw button label
                if control_name == "left":
                    label = "←"
                elif control_name == "right":
                    label = "→"
                elif control_name == "shoot":
                    label = "FIRE"
                elif control_name == "reload":
                    label = "RELOAD"
                elif control_name == "jump":
                    label = "JUMP"
                    
                label_text = self.small_font.render(label, True, text_color)
                label_rect = label_text.get_rect(center=rect.center)
                self.screen.blit(label_text, label_rect)
                
        elif self.state == "menu":
            # Draw menu background
            self.screen.fill(BACKGROUND)
            
            # Draw title
            title_font = pygame.font.SysFont(None, 72)
            title = title_font.render("3D SHOOTER GAME", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title, title_rect)
            
            subtitle_font = pygame.font.SysFont(None, 36)
            subtitle = subtitle_font.render("HCI Project - Touch Controls", True, WHITE)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 220))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Draw difficulty selection
            diff_text = self.font.render("Select Difficulty:", True, WHITE)
            diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(diff_text, diff_rect)
            
            # Draw buttons
            self.start_button.draw(self.screen)
            self.settings_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.easy_button.draw(self.screen)
            self.medium_button.draw(self.screen)
            self.hard_button.draw(self.screen)
            
            # Highlight selected difficulty
            if self.difficulty == 0:
                pygame.draw.rect(self.screen, WHITE, self.easy_button.rect, 3, border_radius=10)
            elif self.difficulty == 1:
                pygame.draw.rect(self.screen, WHITE, self.medium_button.rect, 3, border_radius=10)
            else:
                pygame.draw.rect(self.screen, WHITE, self.hard_button.rect, 3, border_radius=10)
                
            # Draw high score
            hs_text = self.font.render(f"High Score: {self.high_score}", True, YELLOW)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH//2, 550))
            self.screen.blit(hs_text, hs_rect)
            
        elif self.state == "settings":
            self.screen.fill(BACKGROUND)
            
            # Draw title
            title_font = pygame.font.SysFont(None, 72)
            title = title_font.render("SETTINGS", True, BLUE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title, title_rect)
            
            # Draw settings buttons
            self.sound_toggle.draw(self.screen)
            self.music_toggle.draw(self.screen)
            self.contrast_toggle.draw(self.screen)
            self.back_button.draw(self.screen)
            
            # Update button texts to reflect current settings
            self.sound_toggle.text = f"SOUND: {'ON' if self.sound_on else 'OFF'}"
            self.music_toggle.text = f"MUSIC: {'ON' if self.music_on else 'OFF'}"
            self.contrast_toggle.text = f"HIGH CONTRAST: {'ON' if self.high_contrast else 'OFF'}"
            
            # Draw HCI features info
            info_font = pygame.font.SysFont(None, 28)
            info_lines = [
                "HCI Features Implemented:",
                "• Large, accessible touch controls",
                "• Visual feedback for all actions",
                "• Adjustable difficulty levels",
                "• Customizable settings",
                "• High contrast mode",
                "• Vibration feedback (simulated)"
            ]
            
            for i, line in enumerate(info_lines):
                info_text = info_font.render(line, True, WHITE)
                info_rect = info_text.get_rect(topleft=(50, 350 + i * 30))
                self.screen.blit(info_text, info_rect)
                
        elif self.state == "game_over":
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            title_font = pygame.font.SysFont(None, 72)
            title = title_font.render("GAME OVER", True, RED)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(title, title_rect)
            
            # Score display
            score_font = pygame.font.SysFont(None, 48)
            score_text = score_font.render(f"Final Score: {self.score}", True, YELLOW)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 280))
            self.screen.blit(score_text, score_rect)
            
            # Time survived
            time_text = score_font.render(f"Time Survived: {self.game_time//60}:{self.game_time%60:02d}", True, WHITE)
            time_rect = time_text.get_rect(center=(SCREEN_WIDTH//2, 330))
            self.screen.blit(time_text, time_rect)
            
            # Buttons
            self.restart_button.draw(self.screen)
            self.menu_button.draw(self.screen)
            
    def check_game_over(self):
        if self.player.health <= 0:
            if self.score > self.high_score:
                self.high_score = self.score
            self.state = "game_over"
            return True
        return False
        
    def run(self):
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_click = True
                    
                elif event.type == KEYDOWN:
                    if self.state == "playing":
                        if event.key == K_LEFT or event.key == K_a:
                            self.move_left = True
                        elif event.key == K_RIGHT or event.key == K_d:
                            self.move_right = True
                        elif event.key == K_UP or event.key == K_w:
                            self.move_up = True
                        elif event.key == K_DOWN or event.key == K_s:
                            self.move_down = True
                        elif event.key == K_SPACE:
                            bullet = self.player.shoot()
                            if bullet:
                                self.bullets.append(bullet)
                                # Visual feedback
                                self.create_particles(bullet.x, bullet.y, YELLOW, 3)
                        elif event.key == K_r:
                            if self.player.start_reload():
                                # Visual feedback
                                self.create_particles(
                                    self.player.x + self.player.width//2,
                                    self.player.y + self.player.height,
                                    BLUE, 5)
                        elif event.key == K_ESCAPE:
                            self.state = "menu"
                            
                elif event.type == KEYUP:
                    if self.state == "playing":
                        if event.key == K_LEFT or event.key == K_a:
                            self.move_left = False
                        elif event.key == K_RIGHT or event.key == K_d:
                            self.move_right = False
                        elif event.key == K_UP or event.key == K_w:
                            self.move_up = False
                        elif event.key == K_DOWN or event.key == K_s:
                            self.move_down = False
                            
            # State-specific handling
            if self.state == "menu":
                # Update button hover states
                self.start_button.check_hover(mouse_pos)
                self.settings_button.check_hover(mouse_pos)
                self.quit_button.check_hover(mouse_pos)
                self.easy_button.check_hover(mouse_pos)
                self.medium_button.check_hover(mouse_pos)
                self.hard_button.check_hover(mouse_pos)
                
                # Handle button clicks
                if mouse_click:
                    if self.start_button.check_click(mouse_pos, mouse_click):
                        self.start_game()
                        
                    elif self.settings_button.check_click(mouse_pos, mouse_click):
                        self.state = "settings"
                        
                    elif self.quit_button.check_click(mouse_pos, mouse_click):
                        running = False
                        
                    elif self.easy_button.check_click(mouse_pos, mouse_click):
                        self.difficulty = 0
                    elif self.medium_button.check_click(mouse_pos, mouse_click):
                        self.difficulty = 1
                    elif self.hard_button.check_click(mouse_pos, mouse_click):
                        self.difficulty = 2
                        
            elif self.state == "settings":
                # Update button hover states
                self.sound_toggle.check_hover(mouse_pos)
                self.music_toggle.check_hover(mouse_pos)
                self.contrast_toggle.check_hover(mouse_pos)
                self.back_button.check_hover(mouse_pos)
                
                # Handle button clicks
                if mouse_click:
                    if self.sound_toggle.check_click(mouse_pos, mouse_click):
                        self.sound_on = not self.sound_on
                        self.sound_toggle.text = f"SOUND: {'ON' if self.sound_on else 'OFF'}"
                        
                    elif self.music_toggle.check_click(mouse_pos, mouse_click):
                        self.music_on = not self.music_on
                        self.music_toggle.text = f"MUSIC: {'ON' if self.music_on else 'OFF'}"
                        
                    elif self.contrast_toggle.check_click(mouse_pos, mouse_click):
                        self.high_contrast = not self.high_contrast
                        self.contrast_toggle.text = f"HIGH CONTRAST: {'ON' if self.high_contrast else 'OFF'}"
                        
                    elif self.back_button.check_click(mouse_pos, mouse_click):
                        self.state = "menu"
                        
            elif self.state == "game_over":
                # Update button hover states
                self.restart_button.check_hover(mouse_pos)
                self.menu_button.check_hover(mouse_pos)
                
                # Handle button clicks
                if mouse_click:
                    if self.restart_button.check_click(mouse_pos, mouse_click):
                        self.start_game()
                    elif self.menu_button.check_click(mouse_pos, mouse_click):
                        self.state = "menu"
                        
            elif self.state == "playing":
                # Handle touch controls
                if mouse_click:
                    for control_name, rect in self.touch_controls.items():
                        if rect.collidepoint(mouse_pos):
                            if control_name == "left":
                                self.move_left = True
                            elif control_name == "right":
                                self.move_right = True
                            elif control_name == "shoot":
                                bullet = self.player.shoot()
                                if bullet:
                                    self.bullets.append(bullet)
                                    # Visual feedback
                                    self.create_particles(bullet.x, bullet.y, YELLOW, 3)
                                    # Button press feedback
                                    self.touch_controls["shoot"].inflate_ip(10, 10)
                            elif control_name == "reload":
                                if self.player.start_reload():
                                    # Visual feedback
                                    self.create_particles(
                                        self.player.x + self.player.width//2,
                                        self.player.y + self.player.height,
                                        BLUE, 5)
                                    # Button press feedback
                                    self.touch_controls["reload"].inflate_ip(10, 10)
                            elif control_name == "jump":
                                # Jump action (optional)
                                self.create_particles(
                                    self.player.x + self.player.width//2,
                                    self.player.y,
                                    WHITE, 10)
                                    
                # Reset button sizes
                for control_name in self.touch_controls:
                    rect = self.touch_controls[control_name]
                    if rect.width > 100:
                        rect.inflate_ip(-1, -1)
                        
                # Handle movement
                dx, dy = 0, 0
                if self.move_left:
                    dx -= 1
                if self.move_right:
                    dx += 1
                if self.move_up:
                    dy -= 1
                if self.move_down:
                    dy += 1
                    
                if dx != 0 or dy != 0:
                    self.player.move(dx, dy, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    
                # Auto-shoot with rapid fire power-up
                if self.rapid_fire and pygame.time.get_ticks() % 10 == 0:
                    bullet = self.player.shoot()
                    if bullet:
                        self.bullets.append(bullet)
                        
                # Update game objects
                self.player.update()
                
                for enemy in self.enemies:
                    enemy.update()
                    
                for bullet in self.bullets:
                    bullet.update()
                    
                for powerup in self.powerups:
                    powerup.update()
                    
                self.update_particles()
                self.update_powerups()
                
                # Spawn enemies based on difficulty
                self.enemy_spawn_timer += 1
                spawn_rate = max(10, 60 - self.difficulty * 20 - self.game_time // 300)
                if self.enemy_spawn_timer >= spawn_rate:
                    self.spawn_enemy()
                    self.enemy_spawn_timer = 0
                    
                # Spawn powerups
                self.powerup_spawn_timer += 1
                if self.powerup_spawn_timer >= 600:  # Every 10 seconds
                    self.spawn_powerup()
                    self.powerup_spawn_timer = 0
                    
                # Handle collisions
                self.handle_collisions()
                
                # Clean up off-screen objects
                self.enemies = [e for e in self.enemies if not e.is_off_screen()]
                self.bullets = [b for b in self.bullets if not b.is_off_screen()]
                
                # Update game time
                self.game_time += 1
                
                # Check game over
                self.check_game_over()
                
            # Draw everything
            if self.state == "playing":
                # Draw background with 3D effect
                self.screen.fill(BACKGROUND)
                
                # Draw grid for 3D effect
                for i in range(0, SCREEN_WIDTH, 50):
                    for j in range(0, SCREEN_HEIGHT, 50):
                        depth = j * 0.1
                        size = 50 - depth
                        if size > 0:
                            x = i + depth * 0.5
                            y = j + depth
                            pygame.draw.rect(self.screen, (40, 40, 60),
                                            (x, y, 2, 2))
                            
                # Draw game objects
                for powerup in self.powerups:
                    powerup.draw(self.screen)
                    
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                    
                for bullet in self.bullets:
                    bullet.draw(self.screen)
                    
                self.player.draw(self.screen)
                self.draw_particles()
                
            # Draw UI
            self.draw_ui()
            
            # Draw screen flash for damage
            if self.state == "playing" and self.player.invincible:
                flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                flash.fill((255, 50, 50, 100))
                self.screen.blit(flash, (0, 0))
                
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()