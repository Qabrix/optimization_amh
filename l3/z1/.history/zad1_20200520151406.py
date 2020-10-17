import sys
import time
from utils import check_time
from swarm import Swarm

def use_swarm(t, x, e):

    start = time.time()
    while check_time(start,t):
        pass