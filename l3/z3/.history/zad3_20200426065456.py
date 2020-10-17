import sys
import time
from math import e, pow
from random import choice, uniform
from moves_manager import MovesManager

from neighboor import gen_neighbour

def get_input():
    splited_input = str(input()).split(" ")

    t = float(splited_input[0])
    n = int(splited_input[1])
    m = int(splited_input[2])

    pos = []
    grid = []

    for row in range(n):
        line = str(input())
        if '5' in line:
            pos.append(row)
            pos.append(line.index('5'))
        temp = []
        for field in line:
            if field != '\n':
                temp.append(field)
        grid.append(temp)

    return (t, n, m, grid, pos)

def calculate_probability(delta, T):
    return pow(e, (-(delta/T)))

def decrease_temperature(T, c=0.99):
    T *= c
    return T

def sa(pos, grid, n, m, t, start_T=500, c=0.95):
    best_path = []
    T = start_T
    counter = 0
    moves_manager = MovesManager()

    start = time.time()
    while time.time() - start < t:
        T = start_T
        counter = 0

        cur_pos = pos.copy()
        cur_path = []
        while (not moves_manager.check_for_exit(cur_pos, grid)) and time.time() - start < t:
            cur_pos = pos.copy()
            cur_path = moves_manager.random_moves(cur_pos, grid, n, m, (n-2)*(m-2))
        
        if time.time() - start >= t:
            return best_path

        if len(best_path) == 0 or len(cur_path) < len(best_path):
            best_path = cur_path.copy()
        
        treshold = min(n, m)*len(cur_path)

        while counter < treshold and T > 0 and time.time() - start < t:
            temp_path = gen_neighbour(cur_path)
            temp_path, exit_found = moves_manager.explore(pos.copy(), temp_path, grid)

            if exit_found:
                if len(temp_path) <= len(cur_path):
                    cur_path = temp_path.copy()
                    if len(cur_path) < len(best_path):
                        best_path = cur_path.copy()
                elif uniform(0, 1) <= calculate_probability(len(temp_path) - len(cur_path), T):
                    cur_path = temp_path.copy()
                T = decrease_temperature(T, c)
            else:
                counter += 1
        
    return best_path

def main():
    t, n, m, grid, pos = get_input()

    best_path = sa(pos, grid, n, m, t)
    sys.stdout.write(str(len(best_path)))
    sys.stderr.write(str(best_path))

if __name__ == "__main__":
    main()