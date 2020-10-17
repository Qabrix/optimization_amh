import sys
import time
from math import e, pow
from utils import get_input, check_time
from random import choice, uniform

from population import Population
from neighboor import gen_neighbour
from moves_manager import MovesManager

def get_best_path(population, best_path, grid, moves_manager, pos):
    for inhabitant in population:
        temp_path, exit_found = moves_manager.explore(pos.copy(), inhabitant.gene, grid)
        if exit_found:
            path = temp_path
            if len(path) < inhabitant.value or inhabitant.value == 0:
                    inhabitant.value = len(path)
                    if len(path) <= len(best_path) or len(best_path) == 0:
                        best_path = path

    return best_path

def search(pos, grid, n, m, t, starters, p=35):
    best_path = []
    elite_percentage = 0.5
    moves_manager = MovesManager(grid, pos, n, m)
    population = Population(p, starters, moves_manager)

    start_time = time.time()
    while check_time(start_time, t):
        best_path = get_best_path(population, best_path, grid, moves_manager, pos)

        population.recombinate(elite_percentage)
        population.mutate()
        print(best_path, len(best_path), time.time()-start_time)
        
    return best_path

def main():
    t, n, m, grid, pos, starters = get_input()

    best_path = search(pos, grid, n, m, t, starters)
    sys.stdout.write(str(len(best_path)))
    sys.stderr.write(str(best_path))

if __name__ == "__main__":
    main()