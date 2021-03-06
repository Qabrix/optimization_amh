import time
import random
from population2 import Population
from hashMap.hmap import HmapStructure
from utils import get_input, calculate_value, check_time

def init_population(dic, puzzles, size, all_puzzle_keys):
    return Population(puzzles, size, all_puzzle_keys)

def search_for_words(population, dic, puzzles, search_range):
    best_word = ("", 0)
    for inhabitant in population:
        for i in range(1, search_range+1):
            word = inhabitant.get_str_gene(i)
            found = dic.find(word)
            val = calculate_value(word, puzzles)
            if found:
                if found.val != 0 and val > inhabitant.value:
                    inhabitant.value = val

    return best_word
       
def search(dic, puzzles, all_puzzle_keys, t):   
    best_word = ("", 0)
    
    search_range = 2
    fail_counter = 0
    MAX_FAILS = 25

    max_len = len(all_puzzle_keys)
    population = init_population(dic, puzzles, 100, all_puzzle_keys)

    start_time = time.time()
    while check_time(start_time, t) or True:
        prev_value = best_word[1]
        best_word = search_for_words(found_words, population, dic, puzzles, search_range)
        if prev_value == best_word[1] and search_range < max_len:
            fail_counter += 1
            if fail_counter == MAX_FAILS*search_range//2:
                search_range += 1
                fail_counter = 0
        else:
            fail_counter = 0

        population.recombinate()
        population.mutate()
        print(best_word, time.time()-start_time, search_range)

def main():
    t, _, _, puzzles, _, all_puzzle_keys = get_input()
    dic = HmapStructure()
    with open('z2/dict.txt') as f:
        dic.load(f)

    search(dic, puzzles, all_puzzle_keys, t)

if __name__ == "__main__":
    main()