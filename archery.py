from vpython import *
import random
import math
import time
# === 3D ARCHERY - WORKING VERSION ===

# Setup scene
scene = canvas(title='3D Archery Range', width=1200, height=800,
               center=vector(0, 5, 0), background=vector(0.1, 0.1, 0.1))
scene.lights = []

# Game variables
score = 0
arrows = []
targets = []
wind = vector(0, 0, 0)
game_active = True
arrows_left = 15
power = 50
max_power = 100

# === CREATE RANGE ===

# Ground
ground = box(pos=vector(0, -1, 0), size=vector(60, 1, 60),
             color=vector(0, 0.5, 0))

# Shooting position
shooter_pos = vector(0, 1.5, -5)

# Bow (simplified)
bow = box(pos=shooter_pos, size=vector(0.5, 0.2, 0.1),
          color=vector(0.4, 0.2, 0))

# Distance markers
for dist in [10, 20, 30, 40]:
    d = dist
    marker = cylinder(pos=vector(-1, 0.1, d), axis=vector(2, 0, 0),
                     radius=0.05, color=vector(1, 1, 1))
    label(pos=vector(3, 0.5, d), text=f'{dist}m', 
          height=12, color=vector(1, 1, 1))

# === TARGETS ===
class Target:
    def __init__(self, pos, distance):
        self.pos = pos
        self.distance = distance
        self.type = random.choice(['static', 'moving', 'rotating'])
        self.speed = random.uniform(0.5, 2) if self.type == 'moving' else 0
        self.dir = vector(random.choice([-1, 1]), 0, 0) if self.type == 'moving' else vector(0,0,0)
        self.rotate_speed = random.uniform(0.5, 2) if self.type == 'rotating' else 0
        self.angle = 0
        
        # Create target
        self.rings = []
        colors = [vector(1,0,0), vector(1,1,0), vector(0,0,1), vector(0,1,0), vector(1,0.5,0)]
        
        for i in range(5):
            r = 1.5 - i * 0.25
            ring = cylinder(pos=pos, axis=vector(0, 0.1, 0),
                           radius=r, color=colors[i], opacity=0.8)
            self.rings.append(ring)
        
        # Center
        self.center = sphere(pos=pos, radius=0.2, 
                            color=vector(1, 0, 0), opacity=0.9)
        
        # Pole
        self.pole = cylinder(pos=pos - vector(0, 3, 0), axis=vector(0, 3, 0),
                            radius=0.1, color=vector(0.5, 0.5, 0.5))
        
        # Label
        self.label = label(pos=pos + vector(0, 2.5, 0),
                          text=f'{int(distance)}m\n{self.type.title()}',
                          height=10, color=vector(1, 1, 1))
    
    def update(self, dt):
        if self.type == 'moving':
            self.pos += self.dir * self.speed * dt
            if abs(self.pos.x) > 8:
                self.dir.x *= -1
            
            # Update visuals
            for ring in self.rings:
                ring.pos = self.pos
            self.center.pos = self.pos
            self.pole.pos = self.pos - vector(0, 3, 0)
            self.label.pos = self.pos + vector(0, 2.5, 0)
            
        elif self.type == 'rotating':
            self.angle += self.rotate_speed * dt
            for ring in self.rings:
                ring.rotate(angle=self.rotate_speed*dt, axis=vector(0,1,0), origin=self.pos)
    
    def check_hit(self, arrow_pos):
        dist = mag(arrow_pos - self.pos)
        scores = [10, 8, 6, 4, 2]  # Center to outer
        
        for i, ring in enumerate(self.rings):
            if dist <= ring.radius:
                # Visual feedback
                ring.color = vector(1, 1, 1)
                return scores[i]
        return 0

# Create initial targets
def create_targets():
    global targets
    targets = []
    
    # Different distances and types
    positions = [
        (vector(0, 1.5, 15), 15),
        (vector(3, 1.5, 25), 25),
        (vector(-3, 1.5, 35), 35),
        (vector(0, 1.5, 45), 45)
    ]
    
    for pos, dist in positions:
        targets.append(Target(pos, dist))

# === ARROW ===
class Arrow:
    def __init__(self, start_pos, direction, power_level):
        self.pos = start_pos
        self.vel = direction * (20 + power_level * 0.5)  # Speed based on power
        self.active = True
        self.trail = []
        
        # Create arrow
        self.shaft = cylinder(pos=self.pos, axis=self.vel.norm()*0.5,
                             radius=0.03, color=vector(0.7, 0.7, 0.7))
        self.head = cone(pos=self.pos + self.vel.norm()*0.5,
                        axis=self.vel.norm()*0.2,
                        radius=0.06, color=vector(0.3, 0.3, 0.3))
    
    def update(self, dt):
        if not self.active:
            return False
        
        # Physics: gravity + wind
        gravity = vector(0, -9.8, 0)
        self.vel += (gravity + wind) * dt
        
        # Update position
        self.pos += self.vel * dt
        
        # Update visuals
        self.shaft.pos = self.pos
        self.shaft.axis = self.vel.norm() * 0.5
        self.head.pos = self.pos + self.vel.norm() * 0.5
        self.head.axis = self.vel.norm() * 0.2
        
        # Add trail
        if len(self.trail) < 20:
            trail_pt = sphere(pos=self.pos, radius=0.02,
                             color=vector(1, 1, 0), opacity=0.3)
            self.trail.append(trail_pt)
        
        # Check bounds
        if (self.pos.y < 0 or abs(self.pos.x) > 30 or 
            self.pos.z > 60 or self.pos.z < -10):
            self.active = False
            return False
        
        return True

# === UI ===
score_display = label(pos=vector(-15, 12, 0), text=f'SCORE: {score}',
                     height=24, color=vector(0, 1, 0))
arrows_display = label(pos=vector(-15, 10, 0), text=f'ARROWS: {arrows_left}',
                       height=20, color=vector(1, 1, 0))
power_display = label(pos=vector(-15, 8, 0), text=f'POWER: {power}%',
                      height=18, color=vector(1, 0.5, 0))
wind_display = label(pos=vector(-15, 6, 0), text='WIND: Calm',
                     height=16, color=vector(0, 1, 1))

instructions = label(pos=vector(15, 12, 0),
                    text='CONTROLS:\nW/S: Aim Up/Down\nA/D: Aim Left/Right\n\nSPACE: Charge & Shoot\nR: Reset Game\nT: New Targets',
                    height=16, color=vector(1, 1, 1))

# Aim indicator
aim_dir = vector(0, 0, 1)
aim_indicator = arrow(pos=shooter_pos, axis=aim_dir*3,
                      shaftwidth=0.05, color=vector(1, 0, 0))

# === GAME FUNCTIONS ===
def update_wind():
    global wind
    if random.random() < 0.01:  # 1% chance to change wind
        wind = vector(random.uniform(-3, 3), 0, random.uniform(-3, 3))
        
        speed = mag(wind)
        if speed < 0.5:
            desc = 'Calm'
        elif speed < 2:
            desc = 'Breeze'
        else:
            desc = 'Windy'
        
        wind_display.text = f'WIND: {desc}\n({wind.x:.1f}, {wind.z:.1f})'

def shoot():
    global arrows_left, power, arrows
    
    if arrows_left <= 0 or not game_active:
        return
    
    arrows_left -= 1
    
    # Calculate direction
    direction = vector(math.sin(aim_yaw) * math.cos(aim_pitch),
                      math.sin(aim_pitch),
                      math.cos(aim_yaw) * math.cos(aim_pitch))
    direction = direction.norm()
    
    # Create arrow
    start_pos = shooter_pos + direction * 0.5
    arrow = Arrow(start_pos, direction, power)
    arrows.append(arrow)
    
    # Reset power
    power = 50
    update_display()

def update_display():
    score_display.text = f'SCORE: {score}'
    arrows_display.text = f'ARROWS: {arrows_left}'
    power_display.text = f'POWER: {power}%'
    
    # Update aim indicator color based on power
    if power < 33:
        aim_indicator.color = vector(0, 1, 0)  # Green
    elif power < 66:
        aim_indicator.color = vector(1, 1, 0)  # Yellow
    else:
        aim_indicator.color = vector(1, 0, 0)  # Red

def reset_game():
    global score, arrows_left, power, game_active, arrows
    
    score = 0
    arrows_left = 15
    power = 50
    game_active = True
    wind = vector(0, 0, 0)
    
    # Clear arrows
    for arrow in arrows:
        arrow.shaft.visible = False
        arrow.head.visible = False
        for pt in arrow.trail:
            pt.visible = False
    arrows = []
    
    # Create new targets
    create_targets()
    
    update_display()
    wind_display.text = 'WIND: Calm'

# === AIMING ===
aim_pitch = 0  # Up/down (in radians)
aim_yaw = 0    # Left/right (in radians)
max_angle = math.pi/6  # 30 degrees
charging = False

def update_aim():
    # Calculate direction
    direction = vector(math.sin(aim_yaw) * math.cos(aim_pitch),
                      math.sin(aim_pitch),
                      math.cos(aim_yaw) * math.cos(aim_pitch))
    direction = direction.norm()
    
    # Update indicator
    aim_indicator.axis = direction * (2 + power/50)

# === KEYBOARD CONTROLS ===
keys_pressed = set()

def key_down(evt):
    keys_pressed.add(evt.key)
    
    if evt.key == 'r' or evt.key == 'R':
        reset_game()
    elif evt.key == 't' or evt.key == 'T':
        create_targets()
    elif evt.key == ' ':
        global charging
        charging = True

def key_up(evt):
    if evt.key in keys_pressed:
        keys_pressed.remove(evt.key)
    
    if evt.key == ' ':
        global charging
        if charging:
            shoot()
            charging = False

# Bind keys
scene.bind('keydown', key_down)
scene.bind('keyup', key_up)

# === INITIALIZE ===
create_targets()
reset_game()
last_time = time.time()

# === MAIN LOOP ===
while True:
    rate(60)
    
    # Delta time
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    
    # Handle continuous keys
    if 'w' in keys_pressed or 'W' in keys_pressed:
        aim_pitch = min(aim_pitch + 0.03, max_angle)
    if 's' in keys_pressed or 'S' in keys_pressed:
        aim_pitch = max(aim_pitch - 0.03, -max_angle)
    if 'a' in keys_pressed or 'A' in keys_pressed:
        aim_yaw = min(aim_yaw + 0.03, max_angle)
    if 'd' in keys_pressed or 'D' in keys_pressed:
        aim_yaw = max(aim_yaw - 0.03, -max_angle)
    
    # Charge power while space held
    if charging:
        power = min(power + 0.8, max_power)
        update_display()
    
    # Update aim
    update_aim()
    
    # Update wind
    update_wind()
    
    # Update targets
    for target in targets:
        target.update(dt)
    
    # Update arrows
    arrows_to_remove = []
    for i, arrow in enumerate(arrows):
        if arrow.update(dt):
            # Check for hits
            for target in targets:
                hit_score = target.check_hit(arrow.pos)
                if hit_score > 0:
                    score += hit_score
                    arrow.active = False
                    update_display()
                    break
        else:
            arrows_to_remove.append(i)
    
    # Remove inactive arrows
    for i in sorted(arrows_to_remove, reverse=True):
        del arrows[i]
    
    # Game over check
    if arrows_left <= 0 and len(arrows) == 0 and game_active:
        game_active = False
        game_over = label(pos=vector(0, 8, 0),
                         text=f'GAME OVER\nFinal Score: {score}\nPress R to restart',
                         height=30, color=vector(1, 1, 0))