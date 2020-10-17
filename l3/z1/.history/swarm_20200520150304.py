from utils import random_vector, calculate_yang


class Particle:
    def __init__(self, x=[], v=0):
        self.x = x
        self.best_x = x
        self.velocity = v

class Swarm:
    def __init__(self, size=0, lo=0, up=5):
        self.particles = []
        self.size = size
        self._gen_swarm(lo, up, size)

    def _gen_swarm(self, lo, up, size=0):
        for _ in range(size):
            self.particles.append(
                Particle(
                    random_vector(lo, up), random_vector(-abs(up - lo), abs(up - lo))
                )
            )
