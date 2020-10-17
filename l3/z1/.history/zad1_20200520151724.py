import sys
import time
from swarm import Swarm
from utils import check_time

def swarm(t, x, e, swarm_size=1000, omega =0.5):
    swarm = Swarm(e, swarm_size)

    start = time.time()
    while check_time(start,t):
        swarm.update_velocity()
