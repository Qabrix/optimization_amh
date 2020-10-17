import sys
import time
from swarm import Swarm
from utils import check_time, random_vector

def swarm(t, x, e, swarm_size=1000, omega =0.5):
    swarm = Swarm(e, swarm_size)
    omega, fip, fig = 0.5, 0.5, 0.5

    start = time.time()
    while check_time(start,t):
        swarm.update_particles_velocity(e, omega, fip, fig)
        print(swarm.best_swarm_x, swarm.best_swarm_val)

def main():
    x, e = random_vector(0, 5), random_vector(0, 1)

if __name__ == "__main__":
    main()