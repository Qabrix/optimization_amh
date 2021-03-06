import sys
import math 
import time
import random
import numpy as np
from operator import add 

def get_input():
    splited_line = str(input()).split()
    int_input = [int(x) for x in splited_line]
    t = int_input[0]
    x1 = int_input[1]
    x2 = int_input[2]
    x3 = int_input[3]
    x4 = int_input[4]
    x5 = int_input[5]

    e1 = int_input[6]
    e2 = int_input[7]
    e3 = int_input[8]
    e4 = int_input[9]
    e5 = int_input[10]
    return t, (x1, x2, x3, x4, x5), (e1, e2, e3, e4, e5)

def calculate_yang(x, e):
    res = 0
    for i in range(5):
        res += abs(x[i])**(i+1) * e[i]
    return 1 - math.cos(2*math.pi*sqrt_sum) + sqrt_sum/10
