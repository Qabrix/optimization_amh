import sys
import time
from swarm import Swarm
from utils import check_time

def swarm(t, x, e, swarm_size=1000):
    swarm = Swarm(e, swarm_size)
    
    start = time.time()
    while check_time(start,t):
        for particle in S