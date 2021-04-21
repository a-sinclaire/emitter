import pygame
from pygame.locals import *
from emitter import *
import numpy as np
import copy

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# SETUP
emitters = [Emitter(screen, x=1*width / 5, y=height / 2, n_particles=1000, color=(255, 255, 255), lifespan=1000, radius=15, max_r=15, min_r=0, shrink_rate=0.09, density=1, forces=[Force(0.0, np.pi/2, 0.003)]),
            Emitter(screen, x=2*width / 5, y=height / 2, n_particles=50, color=(255, 0, 0), lifespan=3000, radius=5, max_r=40, min_r=0, shrink_rate=-0.05, density=.1, forces=[Force(0.0, np.pi/2, 0.0015)]),
            Emitter(screen, x=3*width / 5, y=height / 2, n_particles=100, color=(0, 255, 0), lifespan=2000, radius=15, max_r=15, min_r=2, shrink_rate=0.02, density=1, forces=[Force(0.3, np.pi/2)]),
            Emitter(screen, x=4*width / 5, y=height / 2, n_particles=100, color=(0, 0, 255), lifespan=1000, radius=8, max_r=30, min_r=0, shrink_rate=0.05, density=.8, forces=[Force(randomV=False, randomAng=True, randomAcc=True)])]

# CUSTOM EMITTERS
e_candle_flame = Emitter(screen, x=width/2, y=height/2, n_particles=120, color=(255, 140, 0), lifespan=1000, radius=15,
                         max_r=50, min_r=0, shrink_rate=0.12, density=1, forces=[Force(velocity=1, ang=np.pi/2)])

# emitters = [e_candle_flame]

theta = 0
GRAVITY = Force(0.0, -np.pi / 2, 0.001)

# MAIN LOOP
while 1:
    WIND = Force(np.cos(theta) * 0.05, 0)
    ENVIRONMENT_FORCES = [WIND, GRAVITY]

    theta += 0.01

    # BACKGROUND
    screen.fill(0)

    # DRAW ELEMENTS
    for e in emitters:
        e.apply_forces(ENVIRONMENT_FORCES)
        e.update()
        e.draw()

    # UPDATE THE SCREEN
    pygame.display.flip()

    # CHECK EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
