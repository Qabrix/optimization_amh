import time
import random
from population2 import Population
from hashMap.hmap import HmapStructure
from utils import get_input, calculate_value, check_time

def init_population(size, all_puzzle_keys, starter_words):
    return Population(size, all_puzzle_keys, starter_words)

def search_for_words(population, dic, puzzles, best_word = ("", 0)):
    for inhabitant in population:
        for i in range(len(inhabitant)//2, len(inhabitant)+1):
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
    MAX_ELITE_PERCENTAGE = 0.8
    MIN_ELITE_PERCENTAGE = 0.4
    elite_percentage = MAX_ELITE_PERCENTAGE
    fail_counter=0
    MAX_FAILS=50
    population = init_population(128, all_puzzle_keys, starter_words)

    start_time = time.time()
    while check_time(start_time, t):
        prev_word = best_word
        best_word = search_for_words(population, dic, puzzles, best_word)

        if prev_word[1] <= best_word[1]:
            fail_counter+=1
            if fail_counter == MAX_FAILS:
                fail_counter = 0
                if elite_percentage > 0.4:
                    elite_percentage /= 2
        else:
            fail_counter = 0
            elite_percentage = MAX_ELITE_PERCENTAGE

        population.recombinate(elite_percentage)
        population.mutate()
        print(best_word, time.time()-start_time)

def main():
    t, _, _, puzzles, starter_words, all_puzzle_keys = get_input()
    dic = HmapStructure()
    with open('z2/dict.txt') as f:
        dic.load(f)

    search(dic, puzzles, all_puzzle_keys, t, starter_words)

if __name__ == "__main__":
    main()