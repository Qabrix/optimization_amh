import time
from population import Population
from hashMap.hmap import HmapStructure
from utils import get_input, calculate_value, check_time

def init_population(dic, puzzles, size = 8, inhabitant_start_size=5):
    return Population(puzzles, size, inhabitant_start_size)

def search_for_words(found_words, population, dic, puzzles, search_range):
    whole_value = 0
    for inhabitant in population:
        value = 0
        for i in range(1, search_range+1):
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
    
    search_range = 3
    fail_counter = 0
    MAX_FAILS = 10

    t, n, s, puzzles, possibile_solutions = get_input()
    start_time = time.time()
    dic = HmapStructure()
    with open('z2/dict.txt') as f:
        max_len = dic.load(f)

    population = init_population(dic, puzzles, 1000, inhabitant_start_size=max_len)
    
    while check_time(start_time, t) or True:
        prev_value = words_value
        words_value += search_for_words(found_words, population, dic, puzzles, search_range)
        if prev_value == words_value:
            fail_counter += 1
            if fail_counter == MAX_FAILS:
                search_range += 1
                fail_counter = 0
        else:
            fail_counter = 0

        population.recombinate()
        population.mutate()
        print(words_value)

if __name__ == "__main__":
    main()