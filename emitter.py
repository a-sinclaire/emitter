import pygame
import numpy as np
import copy


class Force:
    def __init__(self, newtons=0, ang=0, acc=0, random_f=False, random_ang=False):
        self.newtons = newtons
        self.ang = ang % (2 * np.pi)
        self.acc = acc
        self.random_f = random_f
        self.random_ang = random_ang


class Particle:
    def __init__(self, screen, x, y, color, lifespan, radius, max_r, min_r, shrink_rate, density, friction, forces):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.lifespan = lifespan
        self.age = 0
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.start_r = radius
        self.max_r = max_r
        self.min_r = min_r
        self.shrink_rate = shrink_rate
        self.density = density
        self.friction = friction
        self.forces = forces
        self.mass = self.density * self.start_r**2*np.pi

    def apply_forces(self, forces):
        for f in forces:
            if f.random_ang:
                f.ang = np.random.uniform(-np.pi, np.pi)
            if f.random_f:
                f.newtons = np.random.uniform(0.0, 1.0)
            acc = f.newtons / self.mass
            acc += f.acc
            acc *= 1/self.friction
            self.vx += np.cos(f.ang) * acc
            self.vy -= np.sin(f.ang) * acc
            self.x += self.vx
            self.y += self.vy

    def is_dead(self):
        return self.age > self.lifespan or self.radius < 1 or self.x < 0 or self.x > pygame.display.get_surface().get_width() or self.y < 0 or self.y > pygame.display.get_surface().get_height()

    def update(self):
        self.age += 1
        self.radius -= self.shrink_rate
        if self.radius > self.max_r: self.radius = self.max_r
        if self.radius < self.min_r: self.radius = self.min_r
        area = self.radius ** 2 * np.pi
        self.mass = self.density*area
        self.apply_forces(self.forces)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


class Emitter:
    def __init__(self, screen, x, y, n_particles=100, color=(255,255,255), lifespan=100, radius=10, max_r=np.inf, min_r=0, shrink_rate=0.01, density=1, friction=1, forces=[]):
        self.screen = screen
        self.x = x
        self.y = y
        self.n_particles = n_particles
        self.color = color
        self.lifespan = lifespan
        self.radius = radius
        self.max_r = max_r
        self.min_r = min_r
        self.shrink_rate = shrink_rate
        self.density = density
        self.friction = friction
        self.forces = forces

        self.particles = []

    def update(self):
        temp_list = []
        for p in self.particles:
            # REMOVE DEAD PARTICLES
            if not p.is_dead():
                temp_list.append(p)
        self.particles = temp_list
        for p in self.particles:
            # UPDATE EACH PARTICLE
            p.update()

        # ADD PARTICLES IF NEEDED
        if len(self.particles) < self.n_particles:
            self.particles.append(
                Particle(self.screen, self.x, self.y, self.color, self.lifespan, self.radius, self.max_r, self.min_r, self.shrink_rate, self.density,
                         self.friction, copy.deepcopy(self.forces)))

    def apply_forces(self, forces):
        for p in self.particles:
            p.apply_forces(forces)

    def draw(self):
        for p in self.particles:
            p.draw()
