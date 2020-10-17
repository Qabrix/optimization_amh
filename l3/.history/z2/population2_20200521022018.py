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
    def __init__(self, puzzles, population_size, all_puzzle_keys, word_size):
        self.puzzles = puzzles
        self.all_puzzle_keys = all_puzzle_keys
        self.best_res = None
        self.population_size = population_size
        self.word_size = word_size
        self.generation = self._gen_generation(word_size)

    def __iter__(self):
        for inhabitant in self.generation:
            yield inhabitant

    def _random_word(self):
        return random.sample(self.all_puzzle_keys, len(self.all_puzzle_keys))

    def _gen_generation(self, word_size):
        generation = []
        for _ in range(self.population_size):
            word = self._random_word()[:word_size]
            generation.append(Inhabitant(word))
        return generation

    def sorted_generation(self):
        return sorted(self.generation, key=lambda x: x.value, reverse=True)

    def make_selection(self, percentage=0.95, elite_percentage=0.3):
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

    def expanse(self):
        self.word_size+=1
        for inhabitant in self.generation:
            possible_chars = self.all_puzzle_keys.copy()
            for char in inhabitant.gene:
                if char in possible_chars:
                    possible_chars.remove(char)
            inhabitant.gene = inhabitant.gene + [random.choice(possible_chars)]
            print("")

    def recombinate(self):
        selection = self.make_selection()
        permutation = np.random.permutation(len(selection))
        new_generation = []
        for i in range(0, len(permutation)):
            pivot = random.randint(0, self.word_size // 2)
           
            new_word = (
                selection[permutation[i % len(permutation)]][:pivot]
                + selection[permutation[(i + 1) % len(permutation)]][pivot:]
            )
            if self._check_if_correct(new_word):
                new_generation.append(Inhabitant(new_word))
            else:
                new_generation.append(
                    Inhabitant(selection[permutation[i % len(permutation)]].gene)
                )

            new_word = (
                selection[permutation[(i + 1) % len(permutation)]][:pivot]
                + selection[permutation[i % len(permutation)]][pivot:]
            )
            if self._check_if_correct(new_word):
                new_generation.append(Inhabitant(new_word))
            else:
                new_generation.append(
                    Inhabitant(selection[permutation[(i + 1) % len(permutation)]].gene)
                )

        self.generation = new_generation

    def mutate(self, min_swap_probability=0.2, max_swap_probability=0.8, inverse_probability=0.05, random_probability=0.05, shift_probability=0.1):
        swap_probability = random.uniform(min_swap_probability, max_swap_probability)
        for inhabitant in self.generation:
            if decision(random_probability):
                inhabitant.gene = self._random_word()[:self.word_size]
            elif decision(shift_probability):
                inhabitant.gene = [inhabitant.gene[-1]] + inhabitant.gene[:-1]
            else:
                for i in range(len(inhabitant.gene)//2):
                    if decision(swap_probability):
                        random_id = random.randint(0, len(inhabitant) - 1)
                        inhabitant.gene[i], inhabitant.gene[random_id] = (
                            inhabitant.gene[random_id],
                            inhabitant.gene[i],
                        )

                if decision(inverse_probability):
                    inhabitant.gene = inhabitant.gene[::-1]
                    
