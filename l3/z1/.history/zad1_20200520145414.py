import sys
import math 
import time
import random
import numpy as np
from operator import add 

def calculate_yang(x, e):
    res = 0
    for i in range(5):
        res += abs(x[i])**(i+1) * e[i]
    return res

def use_swarm(t, x, e):

    start = time.time()
    while check_time(start,t):
        pass