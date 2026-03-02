import pygame
import sys
import random
import time
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1400, 800
FPS = 60

# Colors
BACKGROUND = (15, 23, 42)  # #0F172A
SIDEBAR_BG = (30, 41, 59)  # #1E293B
ACCENT_BLUE = (56, 189, 248)  # #38BDF8
ACCENT_GREEN = (16, 185, 129)  # #10B981
ACCENT_RED = (239, 68, 68)  # #EF4444
ACCENT_YELLOW = (245, 158, 11)  # #F59E0B
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)  # #94A3B8
DARK_GRAY = (51, 65, 85)  # #334155
PURPLE = (139, 92, 246)  # #8B5CF6
PINK = (236, 72, 153)  # #EC4899

class NexusHangman:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Nexus Hangman")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_xsmall = pygame.font.Font(None, 24)
        
        # Load emoji font if available
        try:
            self.emoji_font = pygame.font.SysFont("segoeuisymbol", 36)
        except:
            self.emoji_font = self.font_small
        
        # Word categories
        self.word_categories = {
            "Programming": ["PYTHON", "JAVASCRIPT", "DOCKER", "KUBERNETES", "TYPESCRIPT"],
            "Animals": ["ELEPHANT", "GIRAFFE", "PENGUIN", "CHIMPANZEE", "LEOPARD"],
            "Countries": ["PAKISTAN", "GERMANY", "AUSTRALIA", "SINGAPORE", "EGYPT"],
            "Fruits": ["PINEAPPLE", "STRAWBERRY", "WATERMELON", "BLUEBERRY", "POMEGRANATE"],
            "Space": ["NEBULA", "ASTRONAUT", "SATELLITE", "METEORITE", "SUPERNOVA"],
            "Sports": ["CRICKET", "FOOTBALL", "BASKETBALL", "WRESTLING", "BADMINTON"],
            "Movies": ["INCEPTION", "AVATAR", "GLADIATOR", "INTERSTELLAR", "AVENGERS"],
            "Cars": ["LAMBORGHINI", "FERRARI", "TESLA", "PORSCHE", "BUGATTI"],
            "Cities": ["LONDON", "TOKYO", "DUBAI", "ISTANBUL", "NEWYORK"],
            "Food": ["BURGER", "PIZZA", "SPAGHETTI", "LASAGNA", "SANDWICH"]
        }
        
        # Game state
        self.score = 0
        self.current_category = "Programming"
        self.word = ""
        self.guessed_word = []
        self.wrong_guesses = 0
        self.max_wrong = 6
        self.hints_left = 3
        self.game_over = False
        self.won = False
        
        # Keyboard layout - All 3 rows
        self.keyboard_rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.letter_buttons = []
        self.create_keyboard()
        
        # Category buttons
        self.category_buttons = []
        self.create_category_buttons()
        
        # Start with splash screen
        self.show_splash = True
        self.splash_time = 0
        self.splash_duration = 3000
        
        # Animation variables
        self.hangman_parts = []
        self.particles = []
        self.animation_time = 0
        
        # Start new game
        self.start_new_game()

    def create_keyboard(self):
        """Create keyboard button positions - All 3 rows visible"""
        self.letter_buttons = []
        keyboard_top = HEIGHT - 280
        button_width = 55
        button_height = 55
        button_margin = 6
        
        # Game area starts at 350px
        game_area_start = 350
        game_area_width = WIDTH - game_area_start
        
        # Row 1: QWERTYUIOP (10 letters)
        row1_width = 10 * (button_width + button_margin) - button_margin
        row1_x_start = game_area_start + (game_area_width - row1_width) // 2
        for i, letter in enumerate(self.keyboard_rows[0]):
            x = row1_x_start + i * (button_width + button_margin)
            y = keyboard_top
            button = {
                'rect': pygame.Rect(x, y, button_width, button_height),
                'letter': letter,
                'enabled': True,
                'color': DARK_GRAY
            }
            self.letter_buttons.append(button)
        
        # Row 2: ASDFGHJKL (9 letters)
        row2_width = 9 * (button_width + button_margin) - button_margin
        row2_x_start = game_area_start + (game_area_width - row2_width) // 2
        for i, letter in enumerate(self.keyboard_rows[1]):
            x = row2_x_start + i * (button_width + button_margin)
            y = keyboard_top + button_height + button_margin + 5
            button = {
                'rect': pygame.Rect(x, y, button_width, button_height),
                'letter': letter,
                'enabled': True,
                'color': DARK_GRAY
            }
            self.letter_buttons.append(button)
        
        # Row 3: ZXCVBNM (7 letters)
        row3_width = 7 * (button_width + button_margin) - button_margin
        row3_x_start = game_area_start + (game_area_width - row3_width) // 2
        for i, letter in enumerate(self.keyboard_rows[2]):
            x = row3_x_start + i * (button_width + button_margin)
            y = keyboard_top + 2 * (button_height + button_margin + 5)
            button = {
                'rect': pygame.Rect(x, y, button_width, button_height),
                'letter': letter,
                'enabled': True,
                'color': DARK_GRAY
            }
            self.letter_buttons.append(button)

    def create_category_buttons(self):
        """Create category button positions"""
        self.category_buttons = []
        start_x = 50
        start_y = 150
        button_width = 250
        button_height = 40
        button_margin = 5
        
        categories = list(self.word_categories.keys())
        for i, category in enumerate(categories):
            x = start_x
            y = start_y + i * (button_height + button_margin)
            button = {
                'rect': pygame.Rect(x, y, button_width, button_height),
                'category': category,
                'selected': category == self.current_category
            }
            self.category_buttons.append(button)

    def start_new_game(self):
        """Start a new game"""
        self.word = random.choice(self.word_categories[self.current_category]).upper()
        self.guessed_word = ["_" for _ in self.word]
        self.wrong_guesses = 0
        self.hints_left = 3
        self.game_over = False
        self.won = False
        self.hangman_parts = []
        
        # Reset keyboard
        for button in self.letter_buttons:
            button['enabled'] = True
            button['color'] = DARK_GRAY
        
        # Create particles for animation
        self.particles = []
        for _ in range(30):
            particle = {
                'x': random.randint(400, WIDTH - 100),
                'y': random.randint(100, HEIGHT - 350),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'color': random.choice([ACCENT_BLUE, ACCENT_GREEN, ACCENT_RED, ACCENT_YELLOW, PURPLE]),
                'size': random.randint(2, 4)
            }
            self.particles.append(particle)

    def draw_splash_screen(self):
        """Draw the splash screen"""
        self.screen.fill(BACKGROUND)
        
        # Animated title
        title = "NEXUS HANGMAN"
        title_font = pygame.font.Font(None, 86)
        title_surface = title_font.render(title, True, ACCENT_BLUE)
        title_rect = title_surface.get_rect(center=(WIDTH//2, HEIGHT//3))
        
        # Pulsing effect
        pulse = math.sin(pygame.time.get_ticks() * 0.002) * 10
        title_surface = pygame.transform.scale(title_surface, 
                                             (int(title_rect.width + pulse), 
                                              int(title_rect.height + pulse)))
        title_rect = title_surface.get_rect(center=(WIDTH//2, HEIGHT//3))
        
        self.screen.blit(title_surface, title_rect)
        
        # Draw animated hangman
        self.draw_animated_hangman_splash()
        
        # Loading text
        loading_font = pygame.font.Font(None, 36)
        loading_text = "Loading Game" + "." * ((pygame.time.get_ticks() // 500) % 4)
        loading_surface = loading_font.render(loading_text, True, GRAY)
        loading_rect = loading_surface.get_rect(center=(WIDTH//2, HEIGHT//3 * 2))
        self.screen.blit(loading_surface, loading_rect)
        
        # Progress bar
        progress_width = 400
        progress_height = 20
        progress_x = WIDTH//2 - progress_width//2
        progress_y = HEIGHT//3 * 2 + 50
        
        # Background
        pygame.draw.rect(self.screen, DARK_GRAY, 
                        (progress_x, progress_y, progress_width, progress_height), 
                        border_radius=10)
        
        # Progress fill
        progress = min(self.splash_time / self.splash_duration, 1.0)
        fill_width = int(progress_width * progress)
        pygame.draw.rect(self.screen, ACCENT_BLUE, 
                        (progress_x, progress_y, fill_width, progress_height), 
                        border_radius=10)
        
        # Countdown
        remaining = max(0, 3 - int(self.splash_time / 1000))
        countdown_font = pygame.font.Font(None, 48)
        countdown_surface = countdown_font.render(str(remaining), True, ACCENT_YELLOW)
        countdown_rect = countdown_surface.get_rect(center=(WIDTH//2, HEIGHT//3 * 2 + 100))
        
        # Pulsing countdown
        countdown_pulse = math.sin(pygame.time.get_ticks() * 0.005) * 5
        countdown_surface = pygame.transform.scale(countdown_surface, 
                                                 (int(countdown_rect.width + countdown_pulse), 
                                                  int(countdown_rect.height + countdown_pulse)))
        countdown_rect = countdown_surface.get_rect(center=(WIDTH//2, HEIGHT//3 * 2 + 100))
        
        self.screen.blit(countdown_surface, countdown_rect)

    def draw_animated_hangman_splash(self):
        """Draw animated hangman for splash screen"""
        center_x, center_y = WIDTH//2, HEIGHT//2
        time_ms = pygame.time.get_ticks()
        
        # Draw gallows
        pygame.draw.line(self.screen, GRAY, 
                        (center_x - 150, center_y + 100), 
                        (center_x + 150, center_y + 100), 8)
        pygame.draw.line(self.screen, GRAY, 
                        (center_x - 100, center_y + 100), 
                        (center_x - 100, center_y - 100), 8)
        pygame.draw.line(self.screen, GRAY, 
                        (center_x - 100, center_y - 100), 
                        (center_x, center_y - 100), 8)
        pygame.draw.line(self.screen, ACCENT_BLUE, 
                        (center_x, center_y - 100), 
                        (center_x, center_y - 60), 4)
        
        # Animated body parts with color cycling
        colors = [ACCENT_RED, ACCENT_YELLOW, ACCENT_GREEN, ACCENT_BLUE, PURPLE, PINK]
        time_factor = time_ms * 0.001
        
        # Head (pulsing)
        head_radius = 20 + math.sin(time_factor * 3) * 5
        pygame.draw.circle(self.screen, colors[int(time_factor) % len(colors)], 
                          (center_x, center_y - 60 + head_radius), 
                          head_radius, 5)
        
        # Body (rotating)
        body_length = 60
        body_angle = math.sin(time_factor * 2) * 0.2
        body_end_x = center_x + math.sin(body_angle) * body_length
        body_end_y = center_y - 60 + head_radius * 2 + math.cos(body_angle) * body_length
        pygame.draw.line(self.screen, colors[(int(time_factor) + 1) % len(colors)], 
                        (center_x, center_y - 60 + head_radius * 2), 
                        (body_end_x, body_end_y), 5)
        
        # Arms (waving)
        arm_length = 40
        arm_angle = math.sin(time_factor * 4) * 0.5
        
        # Left arm
        left_arm_end_x = center_x - math.cos(arm_angle) * arm_length
        left_arm_end_y = center_y - 60 + head_radius * 2 + 20 + math.sin(arm_angle) * arm_length
        pygame.draw.line(self.screen, colors[(int(time_factor) + 2) % len(colors)], 
                        (center_x, center_y - 60 + head_radius * 2 + 20), 
                        (left_arm_end_x, left_arm_end_y), 5)
        
        # Right arm
        right_arm_end_x = center_x + math.cos(arm_angle) * arm_length
        right_arm_end_y = center_y - 60 + head_radius * 2 + 20 + math.sin(-arm_angle) * arm_length
        pygame.draw.line(self.screen, colors[(int(time_factor) + 3) % len(colors)], 
                        (center_x, center_y - 60 + head_radius * 2 + 20), 
                        (right_arm_end_x, right_arm_end_y), 5)
        
        # Legs (kicking)
        leg_length = 50
        leg_angle = math.sin(time_factor * 3) * 0.3
        
        # Left leg
        left_leg_end_x = center_x - math.cos(leg_angle) * leg_length
        left_leg_end_y = body_end_y + math.sin(leg_angle) * leg_length
        pygame.draw.line(self.screen, colors[(int(time_factor) + 4) % len(colors)], 
                        (body_end_x, body_end_y), 
                        (left_leg_end_x, left_leg_end_y), 5)
        
        # Right leg
        right_leg_end_x = center_x + math.cos(leg_angle) * leg_length
        right_leg_end_y = body_end_y + math.sin(-leg_angle) * leg_length
        pygame.draw.line(self.screen, colors[(int(time_factor) + 5) % len(colors)], 
                        (body_end_x, body_end_y), 
                        (right_leg_end_x, right_leg_end_y), 5)

    def draw_main_screen(self):
        """Draw the main game screen"""
        # Background
        self.screen.fill(BACKGROUND)
        
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(self.screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
            
            # Update particle position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Bounce off edges
            if particle['x'] < 350 or particle['x'] > WIDTH - 100:
                particle['vx'] *= -1
            if particle['y'] < 100 or particle['y'] > HEIGHT - 280:
                particle['vy'] *= -1
        
        # Draw sidebar
        pygame.draw.rect(self.screen, SIDEBAR_BG, (0, 0, 350, HEIGHT))
        
        # Draw title
        title = self.font_large.render(" HANGMAN", True, ACCENT_BLUE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        # Draw categories title
        categories_title = self.font_medium.render("CATEGORIES", True, GRAY)
        self.screen.blit(categories_title, (175 - categories_title.get_width()//2, 100))
        
        # Draw category buttons
        for button in self.category_buttons:
            color = ACCENT_BLUE if button['selected'] else DARK_GRAY
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=8)
            
            # Button text
            text = self.font_xsmall.render(button['category'], True, WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
            
            # Glow effect for selected button
            if button['selected']:
                pygame.draw.rect(self.screen, ACCENT_BLUE, button['rect'], 2, border_radius=8)
        
        # Draw score in top-left corner (outside sidebar)
        score_bg = pygame.Rect(360, 15, 200, 50)
        pygame.draw.rect(self.screen, DARK_GRAY, score_bg, border_radius=10)
        pygame.draw.rect(self.screen, ACCENT_BLUE, score_bg, 2, border_radius=10)
        
        # Score text with trophy emoji
        score_text = self.font_medium.render(f"🏆 Score: {self.score}", True, ACCENT_YELLOW)
        self.screen.blit(score_text, (375, 25))
        
        # Draw hints button in top-right corner with emoji
        hint_bg = pygame.Rect(WIDTH - 220, 15, 200, 50)
        hint_color = ACCENT_YELLOW if self.hints_left > 0 else GRAY
        pygame.draw.rect(self.screen, hint_color, hint_bg, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, hint_bg, 2, border_radius=10)
        
        # Hint text with lightbulb emoji
        hint_text = self.font_medium.render(f"💡 Hints: {self.hints_left}", True, (0, 0, 0))
        self.screen.blit(hint_text, (WIDTH - 210, 25))
        
        # Draw hangman
        self.draw_hangman()
        
        # Draw word
        word_display = " ".join(self.guessed_word)
        word_surface = self.font_large.render(word_display, True, ACCENT_BLUE)
        word_rect = word_surface.get_rect(center=(WIDTH//2 + 50, 250))
        self.screen.blit(word_surface, word_rect)
        
        # Draw keyboard
        self.draw_keyboard()
        
        # Draw game over message
        if self.game_over:
            self.draw_game_over()

    def draw_hangman(self):
        """Draw the hangman based on wrong guesses"""
        start_x, start_y = 750, 350
        
        # Draw gallows
        pygame.draw.line(self.screen, GRAY, 
                        (start_x - 100, start_y + 100), 
                        (start_x + 100, start_y + 100), 5)  # Base
        pygame.draw.line(self.screen, GRAY, 
                        (start_x - 50, start_y + 100), 
                        (start_x - 50, start_y - 50), 5)  # Pole
        pygame.draw.line(self.screen, GRAY, 
                        (start_x - 50, start_y - 50), 
                        (start_x + 50, start_y - 50), 5)  # Top beam
        pygame.draw.line(self.screen, ACCENT_BLUE, 
                        (start_x + 50, start_y - 50), 
                        (start_x + 50, start_y - 10), 2)  # Rope
        
        # Draw hangman parts based on wrong guesses
        colors = [ACCENT_RED, ACCENT_YELLOW, ACCENT_GREEN, ACCENT_BLUE, PURPLE, PINK]
        
        if self.wrong_guesses >= 1:  # Head
            pygame.draw.circle(self.screen, colors[0], 
                             (start_x + 50, start_y + 10), 20, 3)
            self.hangman_parts.append(('head', start_x + 50, start_y + 10))
        
        if self.wrong_guesses >= 2:  # Body
            pygame.draw.line(self.screen, colors[1], 
                            (start_x + 50, start_y + 30), 
                            (start_x + 50, start_y + 80), 3)
        
        if self.wrong_guesses >= 3:  # Left arm
            pygame.draw.line(self.screen, colors[2], 
                            (start_x + 50, start_y + 40), 
                            (start_x + 20, start_y + 60), 3)
        
        if self.wrong_guesses >= 4:  # Right arm
            pygame.draw.line(self.screen, colors[3], 
                            (start_x + 50, start_y + 40), 
                            (start_x + 80, start_y + 60), 3)
        
        if self.wrong_guesses >= 5:  # Left leg
            pygame.draw.line(self.screen, colors[4], 
                            (start_x + 50, start_y + 80), 
                            (start_x + 20, start_y + 110), 3)
        
        if self.wrong_guesses >= 6:  # Right leg
            pygame.draw.line(self.screen, colors[5], 
                            (start_x + 50, start_y + 80), 
                            (start_x + 80, start_y + 110), 3)

    def draw_keyboard(self):
        """Draw the keyboard - All 3 rows"""
        # Draw keyboard background
        keyboard_bg = pygame.Rect(350, HEIGHT - 280, WIDTH - 350, 280)
        pygame.draw.rect(self.screen, (25, 35, 55), keyboard_bg)
        
        # Draw keyboard title
        keyboard_title = self.font_small.render("VIRTUAL KEYBOARD", True, GRAY)
        self.screen.blit(keyboard_title, (WIDTH//2 - keyboard_title.get_width()//2, HEIGHT - 275))
        
        # Draw keyboard buttons
        for button in self.letter_buttons:
            # Draw button
            color = button['color'] if button['enabled'] else (button['color'][0]//2, 
                                                              button['color'][1]//2, 
                                                              button['color'][2]//2)
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(self.screen, ACCENT_BLUE if button['enabled'] else GRAY, 
                            button['rect'], 2, border_radius=8)
            
            # Draw letter
            letter_color = WHITE if button['enabled'] else GRAY
            letter_surface = self.font_small.render(button['letter'], True, letter_color)
            letter_rect = letter_surface.get_rect(center=button['rect'].center)
            self.screen.blit(letter_surface, letter_rect)
            
            # Hover effect
            mouse_pos = pygame.mouse.get_pos()
            if button['rect'].collidepoint(mouse_pos) and button['enabled']:
                pygame.draw.rect(self.screen, ACCENT_BLUE, button['rect'], 3, border_radius=8)

    def draw_game_over(self):
        """Draw game over message"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        if self.won:
            message = "🎉 YOU WIN! 🎉"
            color = ACCENT_GREEN
        else:
            message = f"💀 GAME OVER!\nWord: {self.word}"
            color = ACCENT_RED
        
        # Draw message with animation
        message_font = pygame.font.Font(None, 64)
        lines = message.split('\n')
        for i, line in enumerate(lines):
            message_surface = message_font.render(line, True, color)
            message_rect = message_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 50 + i * 80))
            
            # Pulsing effect
            pulse = math.sin(pygame.time.get_ticks() * 0.005) * 5
            scaled_surface = pygame.transform.scale(message_surface, 
                                                  (int(message_rect.width + pulse), 
                                                   int(message_rect.height + pulse)))
            scaled_rect = scaled_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 50 + i * 80))
            self.screen.blit(scaled_surface, scaled_rect)
        
        # Draw play again button
        button_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 50, 300, 60)
        pygame.draw.rect(self.screen, ACCENT_BLUE, button_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, button_rect, 3, border_radius=15)
        
        button_text = self.font_medium.render("🔄 PLAY AGAIN", True, WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # Handle letter input
                if not self.game_over:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        self.handle_letter_guess(letter)
                
                # Handle hint with 'H' key
                if event.key == pygame.K_h and self.hints_left > 0 and not self.game_over:
                    self.use_hint()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.show_splash:
                    # Skip splash on click
                    self.show_splash = False
                
                elif self.game_over:
                    # Check play again button
                    button_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 50, 300, 60)
                    if button_rect.collidepoint(mouse_pos):
                        self.start_new_game()
                
                else:
                    # Check keyboard buttons
                    for button in self.letter_buttons:
                        if button['rect'].collidepoint(mouse_pos) and button['enabled']:
                            self.handle_letter_guess(button['letter'])
                    
                    # Check category buttons
                    for button in self.category_buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            self.current_category = button['category']
                            for b in self.category_buttons:
                                b['selected'] = (b['category'] == self.current_category)
                            self.start_new_game()
                    
                    # Check hint button
                    hint_rect = pygame.Rect(WIDTH - 220, 15, 200, 50)
                    if hint_rect.collidepoint(mouse_pos) and self.hints_left > 0:
                        self.use_hint()
        
        return True

    def handle_letter_guess(self, letter):
        """Handle a letter guess"""
        # Find the button
        for button in self.letter_buttons:
            if button['letter'] == letter and button['enabled']:
                button['enabled'] = False
                
                if letter in self.word:
                    # Correct guess
                    button['color'] = ACCENT_GREEN
                    
                    # Reveal letters
                    for i, l in enumerate(self.word):
                        if l == letter:
                            self.guessed_word[i] = letter
                    
                    self.score += 10
                    
                    # Animation effect
                    self.create_explosion(letter)
                    
                else:
                    # Wrong guess
                    button['color'] = ACCENT_RED
                    self.wrong_guesses += 1
                    self.score = max(0, self.score - 5)
                
                self.check_game_status()
                break

    def create_explosion(self, letter):
        """Create particle explosion for correct guess"""
        for _ in range(20):
            particle = {
                'x': random.randint(400, WIDTH - 100),
                'y': random.randint(100, 300),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'color': random.choice([ACCENT_GREEN, ACCENT_BLUE, ACCENT_YELLOW]),
                'size': random.randint(3, 8),
                'life': 60
            }
            self.particles.append(particle)

    def use_hint(self):
        """Use a hint"""
        if self.hints_left > 0:
            indices = [i for i, l in enumerate(self.guessed_word) if l == "_"]
            if indices:
                idx = random.choice(indices)
                hint_letter = self.word[idx]
                self.handle_letter_guess(hint_letter)
                self.hints_left -= 1

    def check_game_status(self):
        """Check if game is won or lost"""
        if "_" not in self.guessed_word:
            self.game_over = True
            self.won = True
            self.score += 50  # Bonus for winning
            
            # Victory particles
            for _ in range(100):
                particle = {
                    'x': WIDTH // 2,
                    'y': HEIGHT // 2,
                    'vx': random.uniform(-5, 5),
                    'vy': random.uniform(-5, 5),
                    'color': random.choice([ACCENT_GREEN, ACCENT_YELLOW, ACCENT_BLUE, PURPLE]),
                    'size': random.randint(2, 6),
                    'life': 90
                }
                self.particles.append(particle)
                
        elif self.wrong_guesses >= self.max_wrong:
            self.game_over = True
            self.won = False

    def update(self):
        """Update game state"""
        self.animation_time += 1
        
        if self.show_splash:
            self.splash_time += self.clock.get_time()
            if self.splash_time >= self.splash_duration:
                self.show_splash = False
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            if 'life' in particle:
                particle['life'] -= 1
                if particle['life'] <= 0:
                    self.particles.remove(particle)
            
            # Remove particles that go off screen
            if (particle['x'] < 0 or particle['x'] > WIDTH or 
                particle['y'] < 0 or particle['y'] > HEIGHT):
                self.particles.remove(particle)

    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            
            self.update()
            
            if self.show_splash:
                self.draw_splash_screen()
            else:
                self.draw_main_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = NexusHangman()
    game.run()