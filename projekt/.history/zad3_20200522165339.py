import sys
import time
from math import e, pow
from utils import get_input
from random import choice, uniform
from population import Population
from moves_manager import MovesManager

from neighboor import gen_neighbour



def calculate_probability(delta, T):
    return pow(e, (-(delta/T)))

def decrease_temperature(T, c=0.99):
    T *= c
    return T

def sa(pos, grid, n, m, t, p, starters):
    best_path = []
    counter = 0
    moves_manager = MovesManager(grid, pos, n, m)
    p

    start = time.time()
    while time.time() - start < t:
        T = start_T
        counter = 0
        print(time.time() - start, t)
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
    t, n, m, s, p,  grid, pos, starters = get_input()

    best_path = sa(pos, grid, n, m, t)
    sys.stdout.write(str(len(best_path)))
    sys.stderr.write(str(best_path))

if __name__ == "__main__":
    main()