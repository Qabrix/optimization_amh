import time
import random

def get_input():
    splited_line = str(input()).split()
    float_input = [float(x) for x in splited_line]
    t = float_input[0]
    x1 = float_input[1]
    x2 = float_input[2]
    x3 = float_input[3]
    x4 = float_input[4]
    x5 = float_input[5]

    e1 = float_input[6]
    e2 = float_input[7]
    e3 = float_input[8]
    e4 = float_input[9]
    e5 = float_input[10]
    return t, (x1, x2, x3, x4, x5), (e1, e2, e3, e4, e5)

def check_time(start, t):
    return time.time()-start < t 

def random_int(min, max):
    return random.uniform(min, max)

def random_vector(min, max, size=5):
    return [random.uniform(min,max) for _ in range(size)]

def calculate_yang(x, e):
    return sum([abs(x[i])**(i+1) * e[i] for i in range(5)])