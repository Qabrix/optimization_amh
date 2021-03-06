import sys
import time
from swarm import Swarm
from utils import check_time

def swarm(t, x, e, swarm_size=1000, omega =0.5):
    swarm = Swarm(e, swarm_size)
    omega, fip, fig = 0.5, 0.5, 0.5

    start = time.time()
    while check_time(start,t):
        swarm.update_particles_velocity(e, omega, fip, fig)
        print(swarm.best_swarm_x, swarm.best_swarm_val)

def main():

if __name__ == "__main__":
    main()