import sys
import time
from math import e, pow
from utils import get_input, check_time
from random import choice, uniform

from population import Population
from neighboor import gen_neighbour
from moves_manager import MovesManager

def sa(pos, grid, n, m, t, p, starters):
    best_path = []
    counter = 0
    elite_percentage = 0.5
    moves_manager = MovesManager(grid, pos, n, m)
    population = Population(p, starters, moves_manager)

    start_time = time.time()
    while check_time(start_time, t):
        best_path = get_best_path(population)

        population.recombinate(elite_percentage)
        population.mutate()
        print(best_path, len(best_path) time.time()-start_time)
        
    return best_path

def main():
    t, n, m, s, p,  grid, pos, starters = get_input()

    best_path = sa(pos, grid, n, m, t)
    sys.stdout.write(str(len(best_path)))
    sys.stderr.write(str(best_path))

if __name__ == "__main__":
    main()