from utils import random_vector, calculate_yang


class Particle:
    def __init__(self, x=[], v=0):
        self.x = x
        self.best_x = x
        self.velocity = v

class Swarm:
    def __init__(self, e, size=0, lo=0, up=5):
        self.best_swarm_x = -1
        self.best_swarm_val = -1
        self.particles = []
        self.size = size
        self._gen_swarm(lo, up, size)

    def _gen_swarm(self, lo, up, size=0):
        for _ in range(size):
            x = random_vector(lo, up)
            self.particles.append(
                Particle(
                    x, random_vector(-abs(up - lo), abs(up - lo))
                )
            )
            x_val = calculate_yang(x, e)
            if x_val < self.best_swarm_val or self.best_swarm_x == -1:
                self.best_swarm_x = x
                self.best_swarm_val = x_val
