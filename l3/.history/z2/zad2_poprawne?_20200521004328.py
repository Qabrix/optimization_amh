import time
import random
from population2 import Population
from hashMap.hmap import HmapStructure
from utils import get_input, calculate_value, check_time

def init_population(dic, puzzles, size, all_puzzle_keys):
    return Population(puzzles, size, all_puzzle_keys)

def search_for_words(found_words, population, dic, puzzles, search_range):
    whole_value = 0
    for inhabitant in population:
        value = 0
        for i in range(random.randint(1,search_range//2), search_range+1):
            word = inhabitant.get_str_gene(i)
            found = dic.find(word)
            if found:
                if found.val != 0 and word not in found_words:
                    found_words.append(word)
                    value += calculate_value(word, puzzles)
        
        if value > 0:
            inhabitant.value = value
        whole_value += value

    return whole_value

def main():
    found_words = []
    words_value = 0
    
    search_range = 2
    fail_counter = 0
    MAX_FAILS = 20

    t, n, s, puzzles, possibile_solutions, all_puzzle_keys = get_input()
    start_time = time.time()
    dic = HmapStructure()
    with open('z2/dict.txt') as f:
        dic.load(f)
        
    max_len = len(all_puzzle_keys)
    population = init_population(dic, puzzles, 100, all_puzzle_keys)
    
    while check_time(start_time, t) or True:
        prev_value = words_value
        words_value += search_for_words(found_words, population, dic, puzzles, search_range)
        if prev_value == words_value and search_range <= max_len:
            fail_counter += 1
            if fail_counter == MAX_FAILS:
                search_range += 1
                fail_counter = 0
        else:
            fail_counter = 0

        population.recombinate()
        population.mutate()
        print(words_value, time.time()-start_time)

if __name__ == "__main__":
    main()