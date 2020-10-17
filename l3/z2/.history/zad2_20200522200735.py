import sys
import time
import random

from hashMap.hmap import HmapStructure
from population import Population
from utils import calculate_value, check_time, get_input


def init_population(size, all_puzzle_keys, starter_words):
    return Population(size, all_puzzle_keys, starter_words)


def search_for_words(population, dic, puzzles, best_word=("", 0)):
    for inhabitant in population:
        for i in range(len(inhabitant) // 2, len(inhabitant) + 1):
            word = inhabitant.get_str_gene(i)
            found = dic.find(word)
            val = calculate_value(word, puzzles)
            if found:
                if found.val != 0 and val > inhabitant.value:
                    inhabitant.value = val
                    if val >= best_word[1]:
                        best_word = (word, val)

    return best_word


def search(dic, puzzles, all_puzzle_keys, t, starter_words):
    best_word = ("", 0)
    MAX_ELITE_PERCENTAGE = 0.85
    MIN_ELITE_PERCENTAGE = 0.55
    elite_percentage = MAX_ELITE_PERCENTAGE
    fail_counter = 0
    MAX_FAILS = 55
    population = init_population(100, all_puzzle_keys, starter_words)

    start_time = time.time()
    while check_time(start_time, t):
        prev_word = best_word
        best_word = search_for_words(population, dic, puzzles, best_word)

        if prev_word[1] <= best_word[1]:
            fail_counter += 1
            if fail_counter == MAX_FAILS:
                if elite_percentage > MIN_ELITE_PERCENTAGE:
                    elite_percentage -= 0.1
        else:
            fail_counter = 0
            elite_percentage = MAX_ELITE_PERCENTAGE

        if fail_counter == MAX_FAILS ** 2:
            population = init_population(500, all_puzzle_keys, starter_words)
            fail_counter = 0

        population.recombinate(elite_percentage)
        population.mutate()
        print(best_word, time.time() - start_time, fail_counter)
    sys.stdout.write(str(best_word[1]))
    sys.stderr.write(str(best_word[0]))

def main():
    t, _, _, puzzles, starter_words, all_puzzle_keys = get_input()
    dic = HmapStructure()
    with open("dict.txt") as f:
        dic.load(f)

    search(dic, puzzles, all_puzzle_keys, t, starter_words)


if __name__ == "__main__":
    main()
