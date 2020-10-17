import sys
import time
from swarm import Swarm
from utils import check_time, random_vector

def swarm(t, x, e, swarm_size=500, omega=0.8, fip=0.8, fig=1):
    swarm = Swarm(e, swarm_size)

    start = time.time()
    while check_time(start,t):
        swarm.update_particles_velocity(e, omega, fip, fig)
        print(swarm.best_swarm_x, swarm.best_swarm_val)

def main():
    t = 1
    x, e = random_vector(-5, 5), random_vector(0, 1)
    swarm(t, x, e)

if __name__ == "__main__":
    main()