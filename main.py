# Sam Laderoute
# Emitter Project
# Apr 22 2021
#
# Create fully customizable emitters
#
# pip install numpy
# pip install pygame
# pip install pygame_widgets
#

import pygame
from pygame.locals import *
from emitter import *
import numpy as np
from pygame_widgets import *
import copy

pygame.init()
width, height = 860, 480
screen = pygame.display.set_mode((width, height))

# SETUP
# emitters = [Emitter(screen, x=1*width / 5, y=height / 2, n_particles=1000, color=(255, 255, 255), lifespan=1000, radius=15, max_r=15, min_r=0, shrink_rate=0.09, density=1, forces=[Force(0.0, np.pi/2, 0.003)]),
#             Emitter(screen, x=2*width / 5, y=height / 2, n_particles=50, color=(255, 0, 0), lifespan=3000, radius=5, max_r=40, min_r=0, shrink_rate=-0.05, density=.1, forces=[Force(0.0, np.pi/2, 0.0015)]),
#             Emitter(screen, x=3*width / 5, y=height / 2, n_particles=100, color=(0, 255, 0), lifespan=2000, radius=15, max_r=15, min_r=2, shrink_rate=0.02, density=1, forces=[Force(0.3, np.pi/2)]),
#             Emitter(screen, x=4*width / 5, y=height / 2, n_particles=100, color=(0, 0, 255), lifespan=1000, radius=8, max_r=30, min_r=0, shrink_rate=0.05, density=.8, forces=[Force(randomV=False, randomAng=True, randomAcc=True)])]

# CUSTOM EMITTERS
# e_candle_flame = Emitter(screen, x=width/2, y=height/2, n_particles=120, color=(255, 140, 0), lifespan=1000, radius=15,
#                          max_r=50, min_r=0, shrink_rate=0.12, density=1, forces=[Force(velocity=1, ang=np.pi/2)])

# emitters = [e_candle_flame]

f1 = Force(newtons=0.008, ang=np.pi/2)
f2 = Force(random_f=True, random_ang=True)
anti_grav = Force(ang=np.pi/2, acc= 0.001)
e1 = Emitter(screen, x=1*width / 4, y=height / 2, n_particles=500, color=(255, 255, 255), lifespan=250, radius=15,
             max_r=25, min_r=0, shrink_rate=0.06, density=0.01, friction=1, forces=[f1])
e2 = Emitter(screen, x=2*width / 4, y=height / 2, n_particles=500, color=(255, 255, 0), lifespan=550, radius=25,
             max_r=25, min_r=0, shrink_rate=0.05, density=0.2, friction=1, forces=[f2, anti_grav])
e3 = Emitter(screen, x=3*width / 4, y=height / 2, n_particles=500, color=(255, 0, 0), lifespan=250, radius=3,
             max_r=25, min_r=0, shrink_rate=-0.1, density=.1, friction=1, forces=[])
# emitters = [e1, e2, e3]


ScratchEmitter = Emitter(screen, 0.7*width, height/2)
emitters = [ScratchEmitter]

n_particles_slider = Slider(screen, 10, 10, 200, 16, min=0, max=1000, step=1, initial=500)
n_particles_text = TextBox(screen, 220, 10, 100, 20, fontSize=15)
lifespan_slider = Slider(screen, 10, 36, 200, 16, min=0, max=3000, step=20, initial=440)
lifespan_text = TextBox(screen, 220, 36, 100, 20, fontSize=15)
radius_slider = Slider(screen, 10, 62, 200, 16, min=1, max=30, step=1, initial=11)
radius_text = TextBox(screen, 220, 62, 100, 20, fontSize=15)
max_r_slider = Slider(screen, 10, 88, 200, 16, min=0, max=30, step=1, initial=30)
max_r_text = TextBox(screen, 220, 88, 100, 20, fontSize=15)
min_r_slider = Slider(screen, 10, 114, 200, 16, min=0, max=30, step=1, initial=0)
min_r_text = TextBox(screen, 220, 114, 100, 20, fontSize=15)
shrink_rate_slider = Slider(screen, 10, 140, 200, 16, min=0, max=0.1, step=0.005, initial=0.025)
shrink_rate_text = TextBox(screen, 220, 140, 100, 20, fontSize=15)
density_slider = Slider(screen, 10, 166, 200, 16, min=0.001, max=2, step=0.001, initial=0.57)
density_text = TextBox(screen, 220, 166, 100, 20, fontSize=15)
friction_slider = Slider(screen, 10, 192, 200, 16, min=0.01, max=2, step=0.05, initial=0.6)
friction_text = TextBox(screen, 220, 192, 100, 20, fontSize=15)

force_newtons_slider = Slider(screen, 10, 322, 200, 16, min=0, max=3, step=0.01, initial=0)
force_newtons_text = TextBox(screen, 220, 322, 100, 20, fontSize=15)
force_angle_slider = Slider(screen, 10, 348, 200, 16, min=0, max=360, step=1, initial=90)
force_angle_text = TextBox(screen, 220, 348, 100, 20, fontSize=15)
force_acc_slider = Slider(screen, 10, 374, 200, 16, min=0, max=0.003, step=0.0001, initial=0.0022)
force_acc_text = TextBox(screen, 220, 374, 100, 20, fontSize=15)

GRAV_ON = True
WIND_ON = True


def toggle_wind():
    global WIND_ON
    WIND_ON = not WIND_ON


def toggle_gravity():
    global GRAV_ON
    GRAV_ON = not GRAV_ON


grav_button = Button(screen, width-110, 10, 100, 20, text="gravity", fontSize=15, onClick=toggle_gravity)
grav_text = TextBox(screen, width-210, 10, 100, 20, fontSize=15)
wind_button = Button(screen, width-110, 36, 100, 20, text="wind", fontSize=15, onClick=toggle_wind)
wind_text = TextBox(screen, width-210, 36, 100, 20, fontSize=15)

sliders = [n_particles_slider, lifespan_slider, radius_slider, max_r_slider, min_r_slider, shrink_rate_slider, density_slider, friction_slider, force_newtons_slider, force_angle_slider, force_acc_slider]
texts = [n_particles_text, lifespan_text, radius_text, max_r_text, min_r_text, shrink_rate_text, density_text, friction_text, force_newtons_text, force_angle_text, force_acc_text, grav_text, wind_text]
buttons = [grav_button, wind_button]

theta = 0
GRAVITY = Force(ang=-np.pi / 2, acc=0.001)


# MAIN LOOP
while True:
    events = pygame.event.get()
    WIND = Force(newtons=np.cos(theta) * np.random.uniform(0, 0.005), ang=0)
    if GRAV_ON:
        if WIND_ON:
            ENVIRONMENT_FORCES = [GRAVITY, WIND]
        else:
            ENVIRONMENT_FORCES = [GRAVITY]
    else:
        if WIND_ON:
            ENVIRONMENT_FORCES = [WIND]
        else:
            ENVIRONMENT_FORCES = []

    theta += 0.01
    theta %= np.pi * 2

    # BACKGROUND
    screen.fill((30, 30, 30))

    # LISTEN FOR SLIDER EVENTS / SET TEXT
    for s in sliders:
        s.listen(events)
    for b in buttons:
        b.listen(events)
    n_particles_text.setText("n_particles: " + str(n_particles_slider.getValue()))
    lifespan_text.setText("lifespan: " + str(lifespan_slider.getValue()))
    radius_text.setText("radius: " + str(radius_slider.getValue()))
    min_r_text.setText("min_r: " + str(min_r_slider.getValue()))
    max_r_text.setText("max_r: " + str(max_r_slider.getValue()))
    shrink_rate_text.setText("shrink_rate: " + str(shrink_rate_slider.getValue()))
    density_text.setText("density: " + str(density_slider.getValue()))
    friction_text.setText("friction: " + str(friction_slider.getValue()))
    force_newtons_text.setText("force_newtons: " + str(force_newtons_slider.getValue()))
    force_angle_text.setText("force_angle: " + str(force_angle_slider.getValue()))
    force_acc_text.setText("force_acc: " + str(force_acc_slider.getValue()))
    grav_text.setText("gravity: " + str(GRAV_ON))
    wind_text.setText("wind: " + str(WIND_ON))

    # DRAW SLIDERS AND TEXT
    for s in sliders:
        s.draw()
    for t in texts:
        t.draw()
    for b in buttons:
        b.draw()

    # UPDATE FROM SLIDER EVENTS
    ScratchEmitter.n_particles = n_particles_slider.getValue()
    ScratchEmitter.lifespan = lifespan_slider.getValue()
    ScratchEmitter.radius = radius_slider.getValue()
    ScratchEmitter.min_r = min_r_slider.getValue()
    ScratchEmitter.max_r = max_r_slider.getValue()
    ScratchEmitter.shrink_rate = shrink_rate_slider.getValue()
    ScratchEmitter.density = density_slider.getValue()
    ScratchEmitter.friction = friction_slider.getValue()
    ScratchEmitter.forces = [Force(newtons=force_newtons_slider.getValue(), ang=np.deg2rad(force_angle_slider.getValue()), acc=force_acc_slider.getValue())]

    # for testing
    ScratchEmitter.apply_forces(ENVIRONMENT_FORCES)
    emitters[0] = ScratchEmitter

    # DRAW ELEMENTS
    for e in emitters:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            e.apply_forces([Force(newtons=1, random_ang=True)])
        e.apply_forces(ENVIRONMENT_FORCES)
        e.update()
        e.draw()

    # UPDATE THE SCREEN
    pygame.display.flip()

    # CHECK EVENTS
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
