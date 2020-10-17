import sys
import time
from swarm import Swarm
from utils import check_time

def use_swarm(t, x, e):

    start = time.time()
    while check_time(start,t):
        pass