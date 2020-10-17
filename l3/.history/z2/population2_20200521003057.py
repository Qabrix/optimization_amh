import random
import numpy as np
from utils import calculate_value, decision


class Inhabitant:
    def __init__(self, gene, value=0):
        self.gene = gene
        self.value = 0

    def __iter__(self):
        for char in self.gene:
            yield char

    def __len__(self):
        return len(self.gene)

    def __getitem__(self, item):
         return self.gene[item]

    def get_str_gene(self, up):
        return "".join(self.gene[:up])


class Population:
    def __init__(self, puzzles, population_size, all_puzzle_keys):
        self.puzzles = puzzles
        self.all_puzzle_keys = all_puzzle_keys
        self.best_res = None
        self.population_size = population_size
        self.generation = self._gen_generation()
        self.word_size = len(list(puzzles))

    def __iter__(self):
        for inhabitant in self.generation:
            yield inhabitant

    def _gen_generation(self):
        generation = []
        for _ in range(self.population_size):
            word = self.all_puzzle_keys
            random.shuffle(word)
            generation.append(Inhabitant(word))
        return generation

    def sorted_generation(self):
        return sorted(self.generation, key=lambda x: x.value, reverse=True)

    def make_selection(self, percentage=0.5, elite_percentage=0.8):
        selection = []
        sorted_generation = self.sorted_generation()
        selection_size = int(self.population_size * 0.5)
        elite_size = int(elite_percentage * selection_size)
        for inhabitant in sorted_generation[:elite_size]:
            selection.append(inhabitant)
        if elite_size - selection_size < 0:
            for inhabitant in sorted_generation[elite_size - selection_size :]:
                selection.append(inhabitant)

        return selection
    
    def _check_if_correct(self, word):
        possible_chars = self.all_puzzle_keys.copy()
        for char in word:
            if char in possible_chars:
                possible_chars.remove(char)
            else:
                return False
        return True

    def recombinate(self):
        selection = self.make_selection()
        permutation = np.random.permutation(len(selection))
        new_generation = []
        for i in range(0, len(permutation)):
            pivot = random.randint(0, self.word_size // 2)
            new_word = selection[permutation[i%len(permutation)]][:pivot] + selection[permutation[(i + 1)%len(permutation)]][pivot:]
            new_generation.append(
                Inhabitant(
                    
                )
            )
            new_generation.append(
                Inhabitant(
                    selection[permutation[(i + 1)%len(permutation)]][:pivot]
                    + selection[permutation[i%len(permutation)]][pivot:]
                )
            )
        
        self.generation = new_generation

    def mutate(self, probability=0.05):
        for inhabitant in self.generation:
            for i in range(len(inhabitant.gene)):
                if decision(probability):
                    random_id = random.randint(0,len(inhabitant)-1)
                    inhabitant.gene[i], inhabitant.gene[random_id] = inhabitant.gene[random_id], inhabitant.gene[i]
