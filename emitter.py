import pygame
import numpy as np
import copy


class Force:
    def __init__(self, velocity=np.random.uniform(0, 0.3), ang=np.random.uniform(-np.pi, np.pi), acc=0, randomV=False, randomAcc=False, randomAng=False):
        self.velocity = velocity
        self.acc = acc
        self.ang = ang % (2 * np.pi)
        self.randomV = randomV
        self.randomAcc = randomAcc
        self.randomAng = randomAng

    def print(self):
        print("ang:{a}\nvel:{v}\nacc:{ac}\n".format(a=self.ang, v=self.velocity, ac=self.acc))


class Particle:
    def __init__(self, screen, x, y, color, lifespan, radius, max_r, min_r, shrink_rate, density, forces):
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
        self.forces = forces
        self.mass = self.density * self.start_r**2*np.pi
        for f in forces:
            if f.randomAng:
                f.ang = np.random.uniform(-np.pi, np.pi)
            if f.randomV:
                f.velocity = np.random.uniform(0.0, 1.0)
            if f.randomAcc:
                f.acc = np.random.uniform(0, 0.005)

    def apply_forces(self, forces):
        area = self.radius ** 2 * np.pi
        self.mass = self.density*area
        orig_area = self.start_r ** 2 * np.pi
        x = area/orig_area
        for f in forces:
            vel = f.velocity
            vel += self.mass * f.acc
            self.x += np.cos(f.ang) * vel #* (1/self.density) * (np.pi*self.start_r**2*(x+self.start_r)**(-np.pi*0.61)+0.1)#((orig_area / area * self.start_r) + self.start_r/4)
            self.y -= np.sin(f.ang) * vel #* (1/self.density) * (np.pi*self.start_r**2*(x+self.start_r)**(-np.pi*0.61)+0.1)#((orig_area / area * self.start_r) + self.start_r/4)
            # self.x += self.vx
            # self.y -= self.vy

    def is_dead(self):
        return self.age > self.lifespan or self.radius < 1 or self.x < 0 or self.x > pygame.display.get_surface().get_width() or self.y < 0 or self.y > pygame.display.get_surface().get_height()

    def update(self):
        self.age += 1
        self.radius -= self.shrink_rate
        if self.radius > self.max_r: self.radius = self.max_r
        if self.radius < self.min_r: self.radius = self.min_r
        self.apply_forces(self.forces)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


class Emitter:
    def __init__(self, screen, x, y, n_particles, color, lifespan=100, radius=10, max_r=np.inf, min_r=0, shrink_rate=0.01, density=1, forces=[]):
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
                         copy.deepcopy(self.forces)))

    def apply_forces(self, forces):
        for p in self.particles:
            p.apply_forces(forces)

    def draw(self):
        for p in self.particles:
            p.draw()
