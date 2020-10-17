import time
import random
from population2 import Population
from hashMap.hmap import HmapStructure
from utils import get_input, calculate_value, check_time

def init_population(size, all_puzzle_keys, starter_words):
    return Population(size, all_puzzle_keys, starter_words)

def search_for_words(population, dic, puzzles, search_range, best_word = ("", 0)):
    cur_best_word = ("", 0)
    for inhabitant in population:
        for i in range(1, search_range+1):
            word = inhabitant.get_str_gene(i)
            found = dic.find(word)
            val = calculate_value(word, puzzles)
            if found:
                if found.val != 0 and val > inhabitant.value:
                    inhabitant.value = val
                    if val >= cur_best_word[1]:
                        cur_best_word = (word, val)
                        if cur_best_word[1] >= best_word[1]:
                            best_word = cur_best_word

    return best_word, cur_best_word

def search(dic, puzzles, all_puzzle_keys, t, starter_words):   
    best_word = ("", 0)
    res = best_word

    search_range = 5
    fail_counter = 0
    MAX_FAILS = 5

    max_len = len(all_puzzle_keys)
    population = init_population(50, all_puzzle_keys, starter_words)

    start_time = time.time()
    while check_time(start_time, t) or True:
        prev_value = best_word[1]
        best_word, cur_best_word = search_for_words(population, dic, puzzles, search_range, best_word)
        if prev_value == best_word[1]:
            fail_counter += 1
            if fail_counter == MAX_FAILS*search_range//2:
                if cur_best_word[1] > 15:
                    best_word = cur_best_word
                if search_range < max_len:
                    search_range += 1

                fail_counter = 0
        else:
            fail_counter = 0

        if best_word[1] > res[1]:
            res = best_word

        population.recombinate()
        population.mutate()
        print(res, best_word, time.time()-start_time, search_range)

def main():
    t, _, _, puzzles, starter_words, all_puzzle_keys = get_input()
    dic = HmapStructure()
    with open('z2/dict.txt') as f:
        dic.load(f)

    search(dic, puzzles, all_puzzle_keys, t, starter_words)

if __name__ == "__main__":
    main()