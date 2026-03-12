import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Learning Lab")

# Language support
LANGUAGES = {
    'English': {
        'title': "Physics Learning Lab",
        'menu_items': ["Start Learning", "Topics", "Settings", "Exit"],
        'topics': ["Gravity", "Pendulum", "Circuits"],
        'back': "Back",
        'start': "Start",
        'reset': "Reset",
        'language': "Language",
        'high_contrast': "High Contrast",
        'large_text': "Large Text",
        'sound': "Sound",
        'select_topic': "Select Topic",
        'gravity_title': "Gravity Simulation",
        'settings_title': "Settings",
        'instructions': [
            "Click in black area to add planets",
            "Press SPACE to toggle simulation",
            "Press R to reset",
            "Press ESC for menu"
        ],
        'menu_instructions': [
            "Use ↑↓ arrows to navigate",
            "Press ENTER to select",
            "Press ESC to exit"
        ],
        'topic_instructions': "Use ←→ arrows, ENTER to select, ESC for menu",
        'settings_instructions': "Use ↑↓ arrows, ENTER to toggle, ESC for menu",
        'descriptions': [
            "Gravity simulation with planets",
            "Swinging pendulum physics",
            "Electrical circuit builder"
        ]
    },
    'Español': {
        'title': "Laboratorio de Física",
        'menu_items': ["Comenzar Aprendizaje", "Temas", "Configuración", "Salir"],
        'topics': ["Gravedad", "Péndulo", "Circuitos"],
        'back': "Atrás",
        'start': "Iniciar",
        'reset': "Reiniciar",
        'language': "Idioma",
        'high_contrast': "Alto Contraste",
        'large_text': "Texto Grande",
        'sound': "Sonido",
        'select_topic': "Seleccionar Tema",
        'gravity_title': "Simulación de Gravedad",
        'settings_title': "Configuración",
        'instructions': [
            "Haz clic en área negra para añadir planetas",
            "Presiona ESPACIO para alternar simulación",
            "Presiona R para reiniciar",
            "Presiona ESC para menú"
        ],
        'menu_instructions': [
            "Usa flechas ↑↓ para navegar",
            "Presiona ENTER para seleccionar",
            "Presiona ESC para salir"
        ],
        'topic_instructions': "Usa flechas ←→, ENTER para seleccionar, ESC para menú",
        'settings_instructions': "Usa flechas ↑↓, ENTER para alternar, ESC para menú",
        'descriptions': [
            "Simulación de gravedad con planetas",
            "Física del péndulo oscilante",
            "Constructor de circuitos eléctricos"
        ]
    },
    'Français': {
        'title': "Laboratoire de Physique",
        'menu_items': ["Commencer l'Apprentissage", "Sujets", "Paramètres", "Quitter"],
        'topics': ["Gravité", "Pendule", "Circuits"],
        'back': "Retour",
        'start': "Démarrer",
        'reset': "Réinitialiser",
        'language': "Langue",
        'high_contrast': "Contraste Élevé",
        'large_text': "Texte Grand",
        'sound': "Son",
        'select_topic': "Sélectionner un Sujet",
        'gravity_title': "Simulation de Gravité",
        'settings_title': "Paramètres",
        'instructions': [
            "Cliquez dans la zone noire pour ajouter des planètes",
            "Appuyez sur ESPACE pour basculer la simulation",
            "Appuyez sur R pour réinitialiser",
            "Appuyez sur ESC pour le menu"
        ],
        'menu_instructions': [
            "Utilisez les flèches ↑↓ pour naviguer",
            "Appuyez sur ENTRÉE pour sélectionner",
            "Appuyez sur ESC pour quitter"
        ],
        'topic_instructions': "Utilisez les flèches ←→, ENTRÉE pour sélectionner, ESC pour le menu",
        'settings_instructions': "Utilisez les flèches ↑↓, ENTRÉE pour basculer, ESC pour le menu",
        'descriptions': [
            "Simulation de gravité avec des planètes",
            "Physique du pendule oscillant",
            "Constructeur de circuits électriques"
        ]
    },
    'العربية': {
        'title': "مختبر تعلم الفيزياء",
        'menu_items': ["بدء التعلم", "المواضيع", "الإعدادات", "خروج"],
        'topics': ["الجاذبية", "البندول", "الدوائر"],
        'back': "رجوع",
        'start': "بدء",
        'reset': "إعادة تعيين",
        'language': "اللغة",
        'high_contrast': "تباين عالي",
        'large_text': "نص كبير",
        'sound': "صوت",
        'select_topic': "اختر موضوع",
        'gravity_title': "محاكاة الجاذبية",
        'settings_title': "الإعدادات",
        'instructions': [
            "انقر في المنطقة السوداء لإضافة كواكب",
            "اضغط على المسافة لتبديل المحاكاة",
            "اضغط على R لإعادة التعيين",
            "اضغط على ESC للقائمة"
        ],
        'menu_instructions': [
            "استخدم الأسهم ↑↓ للتنقل",
            "اضغط على ENTER للتحديد",
            "اضغط على ESC للخروج"
        ],
        'topic_instructions': "استخدم الأسهم ←→، ENTER للتحديد، ESC للقائمة",
        'settings_instructions': "استخدم الأسهم ↑↓، ENTER للتبديل، ESC للقائمة",
        'descriptions': [
            "محاكاة الجاذبية مع الكواكب",
            "فيزياء البندول المتأرجح",
            "منشئ الدوائر الكهربائية"
        ]
    }
}

# Current language
current_language = 'English'
text = LANGUAGES[current_language]

# Colors
COLORS = {
    'background': (240, 245, 250),
    'primary': (41, 128, 185),
    'secondary': (52, 152, 219),
    'accent': (46, 204, 113),
    'warning': (231, 76, 60),
    'text': (44, 62, 80),
    'light_text': (236, 240, 241),
    'border': (189, 195, 199),
    'highlight': (241, 196, 15)
}

# Fonts
fonts = {
    'large': pygame.font.Font(None, 48),
    'medium': pygame.font.Font(None, 36),
    'small': pygame.font.Font(None, 24)
}

def update_text():
    """Update text based on current language"""
    global text
    text = LANGUAGES[current_language]

# Button class
class Button:
    def __init__(self, x, y, w, h, text, color=COLORS['primary']):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = COLORS['secondary']
        self.is_hovered = False
        self.font = fonts['small']
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLORS['border'], self.rect, 2, border_radius=8)
        
        text_surf = self.font.render(self.text, True, COLORS['light_text'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event_type):
        return event_type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos)

# Menu Screen
class MenuScreen:
    def __init__(self):
        self.buttons = []
        center_x = WIDTH // 2
        for i, item in enumerate(text['menu_items']):
            y = 200 + i * 80
            color = COLORS['warning'] if item in ["Exit", "Salir", "Quitter", "خروج"] else COLORS['primary']
            self.buttons.append(Button(center_x - 150, y, 300, 60, item, color))
            
        self.selected_index = 0
        self.buttons[self.selected_index].is_hovered = True
        
    def draw(self, surface):
        surface.fill(COLORS['background'])
        
        # Title with language indicator
        title = fonts['large'].render(text['title'], True, COLORS['text'])
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Current language
        lang_text = fonts['small'].render(f"Language/Idioma: {current_language}", True, COLORS['primary'])
        surface.blit(lang_text, (WIDTH//2 - lang_text.get_width()//2, 120))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
        # Instructions
        for i, line in enumerate(text['menu_instructions']):
            text_surf = fonts['small'].render(line, True, COLORS['text'])
            surface.blit(text_surf, (WIDTH//2 - 150, 500 + i * 30))
            
    def handle_event(self, event, app):
        mouse_pos = pygame.mouse.get_pos()
        
        # Update hover states
        for button in self.buttons:
            button.check_hover(mouse_pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(mouse_pos, event.type):
                    self.handle_button_click(i, app)
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
                self.update_selection()
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
                self.update_selection()
            elif event.key == pygame.K_RETURN:
                self.handle_button_click(self.selected_index, app)
                
    def update_selection(self):
        for i, button in enumerate(self.buttons):
            button.is_hovered = (i == self.selected_index)
            
    def handle_button_click(self, index, app):
        if index == 0:  # Start Learning
            app.change_screen('gravity')
        elif index == 1:  # Topics
            app.change_screen('topics')
        elif index == 2:  # Settings
            app.change_screen('settings')
        elif index == 3:  # Exit
            pygame.quit()
            sys.exit()

# Topics Screen
class TopicsScreen:
    def __init__(self):
        self.buttons = []
        center_x = WIDTH // 2
        for i, topic in enumerate(text['topics']):
            x = center_x - 350 + i * 250
            self.buttons.append(Button(x, 200, 200, 100, topic))
            
        self.buttons.append(Button(center_x - 100, 400, 200, 50, text['back'], COLORS['border']))
        self.selected_index = 0
        self.buttons[self.selected_index].is_hovered = True
        
    def draw(self, surface):
        surface.fill(COLORS['background'])
        
        title = fonts['medium'].render(text['select_topic'], True, COLORS['text'])
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        # Current language
        lang_text = fonts['small'].render(f"{current_language}", True, COLORS['primary'])
        surface.blit(lang_text, (WIDTH - 150, 30))
        
        for button in self.buttons:
            button.draw(surface)
            
        # Descriptions
        for i, desc in enumerate(text['descriptions']):
            text_surf = fonts['small'].render(desc, True, COLORS['text'])
            x = self.buttons[i].rect.centerx - text_surf.get_width()//2
            y = self.buttons[i].rect.bottom + 10
            surface.blit(text_surf, (x, y))
            
        # Instructions
        inst = fonts['small'].render(text['topic_instructions'], True, COLORS['text'])
        surface.blit(inst, (WIDTH//2 - inst.get_width()//2, 550))
        
    def handle_event(self, event, app):
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            button.check_hover(mouse_pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(mouse_pos, event.type):
                    if i < 3:  # Topics
                        app.change_screen(['gravity', 'pendulum', 'circuit'][i])
                    elif i == 3:  # Back
                        app.change_screen('menu')
                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = max(0, self.selected_index - 1)
                self.update_selection()
            elif event.key == pygame.K_RIGHT:
                self.selected_index = min(2, self.selected_index + 1)
                self.update_selection()
            elif event.key == pygame.K_RETURN:
                if self.selected_index < 3:
                    app.change_screen(['gravity', 'pendulum', 'circuit'][self.selected_index])
            elif event.key == pygame.K_ESCAPE:
                app.change_screen('menu')
                
    def update_selection(self):
        for i, button in enumerate(self.buttons[:3]):
            button.is_hovered = (i == self.selected_index)

# Gravity Simulation
class GravitySimulation:
    def __init__(self):
        self.planets = []
        self.buttons = [
            Button(50, 50, 100, 40, text['back'], COLORS['border']),
            Button(WIDTH - 250, 600, 100, 40, text['start']),
            Button(WIDTH - 120, 600, 100, 40, text['reset'], COLORS['warning'])
        ]
        self.simulating = False
        self.selected_index = 0
        self.buttons[self.selected_index].is_hovered = True
        
    def draw(self, surface):
        surface.fill(COLORS['background'])
        
        # Title
        title = fonts['medium'].render(text['gravity_title'], True, COLORS['text'])
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        # Current language
        lang_text = fonts['small'].render(f"{current_language}", True, COLORS['primary'])
        surface.blit(lang_text, (WIDTH - 150, 30))
        
        # Simulation area
        sim_area = pygame.Rect(50, 100, 900, 450)
        pygame.draw.rect(surface, (20, 30, 40), sim_area)
        pygame.draw.rect(surface, COLORS['border'], sim_area, 2)
        
        # Sun
        pygame.draw.circle(surface, COLORS['highlight'], (WIDTH//2, 325), 30)
        
        # Planets
        for planet in self.planets:
            pygame.draw.circle(surface, (100, 200, 255), 
                              (int(planet['x']), int(planet['y'])), planet['size'])
            
            # Trail
            if len(planet['trail']) > 1:
                pygame.draw.lines(surface, (100, 200, 255, 150), False, planet['trail'], 2)
                
        # Buttons
        for button in self.buttons:
            button.draw(surface)
            
        # Instructions with color coding
        colors = [COLORS['highlight'], COLORS['accent'], COLORS['warning'], COLORS['text']]
        for i, line in enumerate(text['instructions']):
            color = colors[i]
            if i == 0:  # Pulse first instruction
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 100
                color = (min(255, color[0] + int(pulse)), 
                        min(255, color[1] + int(pulse)), 
                        min(255, color[2] + int(pulse)))
                        
            text_surf = fonts['small'].render(line, True, color)
            surface.blit(text_surf, (650, 150 + i * 30))
            
    def handle_event(self, event, app):
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            button.check_hover(mouse_pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[0].is_clicked(mouse_pos, event.type):  # Back
                app.change_screen('topics')
            elif self.buttons[1].is_clicked(mouse_pos, event.type):  # Start/Pause
                self.simulating = not self.simulating
                self.buttons[1].text = "Pause" if self.simulating else text['start']
            elif self.buttons[2].is_clicked(mouse_pos, event.type):  # Reset
                self.planets = []
                self.simulating = False
                self.buttons[1].text = text['start']
            elif 50 <= mouse_pos[0] <= 950 and 100 <= mouse_pos[1] <= 550:
                # Add planet
                self.planets.append({
                    'x': mouse_pos[0],
                    'y': mouse_pos[1],
                    'vx': random.uniform(-1, 1),
                    'vy': random.uniform(-1, 1),
                    'size': random.randint(5, 15),
                    'trail': []
                })
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app.change_screen('menu')
            elif event.key == pygame.K_SPACE:
                self.simulating = not self.simulating
                self.buttons[1].text = "Pause" if self.simulating else text['start']
            elif event.key == pygame.K_r:
                self.planets = []
                self.simulating = False
                self.buttons[1].text = text['start']
            elif event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
                self.update_selection()
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
                self.update_selection()
            elif event.key == pygame.K_RETURN:
                if self.selected_index == 0:  # Back
                    app.change_screen('topics')
                elif self.selected_index == 1:  # Start/Pause
                    self.simulating = not self.simulating
                    self.buttons[1].text = "Pause" if self.simulating else text['start']
                elif self.selected_index == 2:  # Reset
                    self.planets = []
                    self.simulating = False
                    self.buttons[1].text = text['start']
                    
        # Update simulation
        if self.simulating:
            self.update_planets()
            
    def update_selection(self):
        for i, button in enumerate(self.buttons):
            button.is_hovered = (i == self.selected_index)
            
    def update_planets(self):
        sun_x, sun_y = WIDTH//2, 325
        
        for planet in self.planets:
            # Gravity calculation
            dx = sun_x - planet['x']
            dy = sun_y - planet['y']
            dist = max(20, math.sqrt(dx*dx + dy*dy))
            
            force = 5000 / (dist * dist)
            angle = math.atan2(dy, dx)
            
            planet['vx'] += force * math.cos(angle) * 0.01
            planet['vy'] += force * math.sin(angle) * 0.01
            
            planet['x'] += planet['vx']
            planet['y'] += planet['vy']
            
            planet['trail'].append((planet['x'], planet['y']))
            if len(planet['trail']) > 30:
                planet['trail'].pop(0)

# Settings Screen with Language Selection
class SettingsScreen:
    def __init__(self):
        self.options = [
            text['language'],
            text['high_contrast'],
            text['large_text'],
            text['sound'],
            text['back']
        ]
        self.buttons = []
        center_x = WIDTH // 2
        for i, option in enumerate(self.options):
            y = 150 + i * 80
            color = COLORS['border'] if option == text['back'] else COLORS['primary']
            self.buttons.append(Button(center_x - 150, y, 300, 60, option, color))
            
        self.selected_index = 0
        self.buttons[self.selected_index].is_hovered = True
        self.states = [False, False, True]  # States for contrast, text, sound
        self.language_index = 0  # Index of current language
        self.languages = list(LANGUAGES.keys())
        
    def draw(self, surface):
        surface.fill(COLORS['background'])
        
        title = fonts['medium'].render(text['settings_title'], True, COLORS['text'])
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        for i, button in enumerate(self.buttons):
            button.draw(surface)
            
            # Show state for each option
            if i == 0:  # Language
                lang_text = fonts['small'].render(self.languages[self.language_index], True, COLORS['accent'])
                surface.blit(lang_text, (button.rect.right + 20, button.rect.centery - 10))
            elif i < 4:  # Other toggles (contrast, text, sound)
                state_text = "ON" if self.states[i-1] else "OFF"
                color = COLORS['accent'] if self.states[i-1] else COLORS['warning']
                text_surf = fonts['small'].render(state_text, True, color)
                surface.blit(text_surf, (button.rect.right + 20, button.rect.centery - 10))
                
        # Instructions
        inst = fonts['small'].render(text['settings_instructions'], True, COLORS['text'])
        surface.blit(inst, (WIDTH//2 - inst.get_width()//2, 550))
        
    def handle_event(self, event, app):
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            button.check_hover(mouse_pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(mouse_pos, event.type):
                    if i == len(self.buttons) - 1:  # Back
                        app.change_screen('menu')
                    else:
                        self.handle_option_click(i, app)
                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
                self.update_selection()
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
                self.update_selection()
            elif event.key == pygame.K_RETURN:
                if self.selected_index == len(self.buttons) - 1:  # Back
                    app.change_screen('menu')
                else:
                    self.handle_option_click(self.selected_index, app)
            elif event.key == pygame.K_ESCAPE:
                app.change_screen('menu')
            elif event.key == pygame.K_LEFT and self.selected_index == 0:
                self.change_language(-1, app)
            elif event.key == pygame.K_RIGHT and self.selected_index == 0:
                self.change_language(1, app)
                
    def update_selection(self):
        for i, button in enumerate(self.buttons):
            button.is_hovered = (i == self.selected_index)
            
    def handle_option_click(self, index, app):
        if index == 0:  # Language
            self.change_language(1, app)  # Cycle to next language
        elif index == 1:  # High Contrast
            self.states[0] = not self.states[0]
            self.apply_contrast()
        elif index == 2:  # Large Text
            self.states[1] = not self.states[1]
            self.apply_text_size()
        elif index == 3:  # Sound
            self.states[2] = not self.states[2]
            
    def change_language(self, direction, app):
        global current_language
        self.language_index = (self.language_index + direction) % len(self.languages)
        current_language = self.languages[self.language_index]
        update_text()  # Update all text
        
        # Update button texts
        self.options = [
            text['language'],
            text['high_contrast'],
            text['large_text'],
            text['sound'],
            text['back']
        ]
        
        for i, button in enumerate(self.buttons):
            button.text = self.options[i]
            
        # Refresh other screens
        app.refresh_screens()
            
    def apply_contrast(self):
        if self.states[0]:  # High contrast on
            COLORS['background'] = (255, 255, 255)
            COLORS['text'] = (0, 0, 0)
            COLORS['border'] = (100, 100, 100)
        else:  # High contrast off
            COLORS['background'] = (240, 245, 250)
            COLORS['text'] = (44, 62, 80)
            COLORS['border'] = (189, 195, 199)
            
    def apply_text_size(self):
        if self.states[1]:  # Large text
            fonts['large'] = pygame.font.Font(None, 56)
            fonts['medium'] = pygame.font.Font(None, 42)
            fonts['small'] = pygame.font.Font(None, 30)
        else:  # Normal text
            fonts['large'] = pygame.font.Font(None, 48)
            fonts['medium'] = pygame.font.Font(None, 36)
            fonts['small'] = pygame.font.Font(None, 24)

# Main Application
class PhysicsLearningApp:
    def __init__(self):
        self.current_screen = 'menu'
        self.screens = {
            'menu': MenuScreen(),
            'topics': TopicsScreen(),
            'gravity': GravitySimulation(),
            'pendulum': GravitySimulation(),  # Simplified
            'circuit': GravitySimulation(),   # Simplified
            'settings': SettingsScreen()
        }
        
    def change_screen(self, screen_name):
        self.current_screen = screen_name
        # Recreate screen to update language
        self.refresh_current_screen()
        
    def refresh_current_screen(self):
        """Refresh the current screen with updated language"""
        if self.current_screen == 'menu':
            self.screens['menu'] = MenuScreen()
        elif self.current_screen == 'topics':
            self.screens['topics'] = TopicsScreen()
        elif self.current_screen == 'gravity':
            self.screens['gravity'] = GravitySimulation()
        elif self.current_screen == 'settings':
            self.screens['settings'] = SettingsScreen()
            
    def refresh_screens(self):
        """Refresh all screens when language changes"""
        self.screens['menu'] = MenuScreen()
        self.screens['topics'] = TopicsScreen()
        self.screens['gravity'] = GravitySimulation()
        self.screens['settings'] = SettingsScreen()
        
    def run(self):
        clock = pygame.time.Clock()
        
        print("=" * 60)
        print("PHYSICS LEARNING LAB - Interactive Virtual Learning Environment")
        print("=" * 60)
        print("\nSUPPORTED LANGUAGES:")
        for lang in LANGUAGES.keys():
            print(f"  • {lang}")
        print("\nKEYBOARD CONTROLS:")
        print("↑↓ arrows - Navigate up/down")
        print("←→ arrows - Change language in settings / Navigate topics")
        print("ENTER     - Select/Activate")
        print("SPACE     - Toggle simulation (in gravity sim)")
        print("R         - Reset simulation")
        print("ESC       - Go back/Exit")
        print("=" * 60)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.current_screen == 'menu':
                        running = False
                        
                # Pass event to current screen
                if self.current_screen in self.screens:
                    self.screens[self.current_screen].handle_event(event, self)
            
            # Draw current screen
            if self.current_screen in self.screens:
                self.screens[self.current_screen].draw(screen)
                
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()
        sys.exit()

# Run the app
if __name__ == "__main__":
    app = PhysicsLearningApp()
    app.run()