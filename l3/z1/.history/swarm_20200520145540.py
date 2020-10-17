from utils import random_vector

class Particle():
    def __init__(self, x=[]):
        self.x = x

class Swarm():
    def __init__(self, size=0):
        self.size = size
        self._gen_swarm(size)


    def _gen_swarm(self.)