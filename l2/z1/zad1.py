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
    return t, (x1, x2, x3, x4)

def calculate_salomon(x):
    sqrt_sum = math.sqrt(sum(np.square(x)))
    return 1 - math.cos(2*math.pi*sqrt_sum) + sqrt_sum/10

def calculate_probability(T,x,y):
    fy, fx = calculate_salomon(y), calculate_salomon(x)
    result = 1/(1+np.exp((fy-fx)/T))
    return result

def decrease_temperature(T, c=0.99):
    T *= 0.99
    return T

def decision(probability):
    return random.random() < probability

def check_time(start, t):
    return time.time()-start < t 

def find_neighbor(x, radius, step,T,start,t,multiplier=10):
    changed = False
    while not changed and check_time(start,t):
        for changer in list(np.arange(step, radius, step*multiplier)):
            float_update_vector = []
            for _ in range(4):
                float_update_vector.append(random.uniform(-changer,changer))
            y = list(map(add, x, float_update_vector)) 
                
            probability = calculate_probability(T,x,y)
            if decision(probability):
                x = y
                T = decrease_temperature(T, x)
                changed = True
                break

    return x, T

def sa(t, x, start_T=100, start_step=0.1, min_step=10e-100, max_multiplier = 10, max_fails=100, step_scaler=2):
    T = start_T
    step = start_step
    start = time.time()

    cur_x = best_x = x
    best_val = calculate_salomon(x)
    fail_counter = 0

    while check_time(start,t) and T > 0:
        cur_x, T = find_neighbor(cur_x,max_multiplier*step,step,T,start,t)

        cur_val = calculate_salomon(cur_x[:1])
        if cur_val < best_val:
            best_x = cur_x
            best_val = cur_val
            fail_counter = 0
        else:
            fail_counter+=1
            if step > min_step:
                step /= step_scaler
            if fail_counter == max_fails:
                for _ in range(fail_counter):
                    y = random_vector(min(cur_x),-1*max(cur_x))
                    probability = calculate_probability(T,cur_x,y)
                    if decision(probability):
                        cur_x = y
                        T = decrease_temperature(T, x)
                fail_counter = 0
                T *=1.01
    return best_x, best_val

def random_vector(min, max):
    x = []
    for _ in range(4):
        x.append(random.uniform(min, max))
    
    return x

def main():
    t, x = get_input()
    start_T = 100
    start_step = 0.1
    best_x, best_val = sa(t,x,start_T,start_step)
    sys.stdout.write(str(best_val) + " " + str(best_x))

if __name__ == "__main__":
    main()