from operator import add
from utils import random_vector, calculate_yang


class Particle:
    def __init__(self, x=[], v=0):
        self.x = x
        self.best_x = x
        self.velocity = v

    def update_velocity(self, omega, fip, fig, g):
        r = random_vector(0, 1, 2)
        self.velocity = [
            omega * self.velocity[i]
            + fip * r[0] * (self.best_x[i] - self.x[i])
            + fig * r[1] * (g[i] - self.x[i])
            for i in range(len(self.velocity))
        ]

    def update_x(self):
        self.x = list(map(add, self.x, self.velocity))

class Swarm:
    def __init__(self, e, size=0, lo=0, up=5):
        self.best_swarm_x = -1
        self.best_swarm_val = -1
        self.particles = []
        self.size = size
        self._gen_swarm(lo, up, e, size)

    def _gen_swarm(self, lo, up, e, size=0):
        for _ in range(size):
            x = random_vector(lo, up)
            self.particles.append(
                Particle(x, random_vector(-abs(up - lo), abs(up - lo)))
            )
            x_val = calculate_yang(x, e)
            if x_val < self.best_swarm_val or self.best_swarm_x == -1:
                self.best_swarm_x = x
                self.best_swarm_val = x_val

    def update_particles_velocity(self, e, omega=1, fip=1, fig=1):
        for particle in self.particles:
            particle.update_velocity(omega, fip, fig, self.best_swarm_x)
            particle.update_x()

            particle_x_val = calculate_yang(particle.x, e)
            particle_best_x_val = calculate_yang(particle.best_x, e)
            if particle_x_val < particle_best_x_val:
                particle.best_x = particle.x_val
                if particle_x_val < self.best_swarm_val:
                    self.best_swarm_x = particle.x
                    self.best_swarm_val = particle_x_val
