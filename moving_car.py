from vpython import *
import time

# --- 1. Scene Setup ---
scene = canvas(title="3D Interactive Smart City", width=1000, height=600)
scene.background = color.gray(0.1)
scene.forward = vector(-1, -1, -1)

# --- 2. Lighting ---
dist_light = distant_light(direction=vector(0, -1, 0), color=color.white)
lamp = local_light(pos=vector(0, 10, 0), color=color.yellow)

# --- 3. Modeling ---
road = box(pos=vector(0, 0, 0), size=vector(40, 0.1, 10), color=color.gray(0.2))
line1 = box(pos=vector(0, 0.05, 0), size=vector(40, 0.01, 0.2), color=color.yellow)

b1 = box(pos=vector(-10, 5, -8), size=vector(5, 10, 5), color=color.blue)
b2 = box(pos=vector(10, 7.5, -8), size=vector(6, 15, 6), color=color.cyan)

pole = cylinder(pos=vector(5, 0, 6), axis=vector(0, 8, 0), radius=0.2, color=color.gray(0.5))
signal_box = box(pos=vector(5, 8, 6), size=vector(1, 2, 1), color=color.black)
light_bulb = sphere(pos=vector(5, 8, 5.4), radius=0.4, color=color.green)

trunk = cylinder(pos=vector(-15, 0, 7), axis=vector(0, 3, 0), radius=0.3, color=vector(0.4, 0.2, 0))
foliage = sphere(pos=vector(-15, 4, 7), radius=2, color=color.green)

# Car as a Compound Object (Takay wheels sath move karein)
b = box(pos=vector(0, 0.5, 0), size=vector(3, 1, 1.5), color=color.red)
w1 = cylinder(pos=vector(-1, 0.2, 0.8), axis=vector(0,0,0.1), radius=0.3, color=color.black)
car = compound([b, w1], pos=vector(-18, 0, 2))

# --- 4. Animation & HCI Logic ---
car_speed = 0.2
turn_angle = 0
state = "DRIVING"
current_view = "default"

# Function to handle key presses (Corrected HCI Interaction)
def handle_keydown(evt):
    global state, current_view
    s = evt.key
    if s == 't': current_view = "top"
    if s == 'd': current_view = "driver"
    if s == 's':
        if state == "DRIVING":
            state = "STOPPED"
            light_bulb.color = color.red
        else:
            state = "DRIVING"
            light_bulb.color = color.green

scene.bind('keydown', handle_keydown)

def update_camera():
    if current_view == "top":
        scene.camera.pos = vector(0, 35, 0)
        scene.camera.axis = vector(0, -35, 0)
    elif current_view == "driver":
        # Camera car ke saath move karega
        scene.camera.pos = car.pos + vector(-4, 2, 0)
        scene.camera.axis = vector(10, -1, 0)

print("CONTROLS: [T] Top View | [D] Driver View | [S] Stop/Start Traffic")

# --- 5. Main Loop ---
while True:
    rate(60)
    update_camera()

    if state == "DRIVING":
        # 1. Translation (Straight)
        if car.pos.x < 5:
            car.pos.x += car_speed
        # 2. Combined Translation + Rotation (Turning)
        elif turn_angle < pi/2:
            d_theta = 0.05
            car.rotate(angle=-d_theta, axis=vector(0,1,0), origin=vector(5, 0, 5))
            turn_angle += d_theta
        # 3. New Direction
        else:
            car.pos.z += car_speed