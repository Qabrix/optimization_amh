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
    def __init__(self, population_size, all_puzzle_keys, starter_words):
        self.all_puzzle_keys = all_puzzle_keys
        self.best_res = None
        self.population_size = population_size
        self.word_size = len(list(all_puzzle_keys))
        self.generation = self._gen_generation(starter_words)

    def __iter__(self):
        for inhabitant in self.generation:
            yield inhabitant

    def _random_word(self):
        return random.sample(self.all_puzzle_keys, len(self.all_puzzle_keys))

    def _gen_generation(self, starter_words):
        generation = []
        for word in starter_words:
            possible_chars = self._random_word()
            for char in word:
                if char in word:
                    possible_chars.remove(char)
            generation.append(Inhabitant(list(word)+possible_chars))
        for _ in range(len(starter_words), self.population_size):
            word = self._random_word()
            generation.append(Inhabitant(word))
        return generation

    def sorted_generation(self):
        return sorted(self.generation, key=lambda x: x.value, reverse=True)

    def make_selection(self, percentage=0.5, elite_percentage=0.5):
        selection = []
        sorted_generation = self.sorted_generation()
        selection_size = int(self.population_size * percentage)
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
        new_generation.append(Inhabitant(selection[0].gene))
        new_generation.append(Inhabitant(selection[-1].gene))
        for i in range(1, len(permutation)):
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

    def mutate(self, min_swap_probability=0.1, max_swap_probability=0.2, inverse_probability=0.01, random_probability=0.01, shift_probability=0.01):
        swap_probability = random.uniform(min_swap_probability, max_swap_probability)
        for inhabitant in self.generation:
            if decision(random_probability):
                inhabitant.gene = self._random_word()
            elif decision(shift_probability):
                shift_range = random.randint(1, 3)
                inhabitant.gene = [inhabitant.gene[-shift_range]] + inhabitant.gene[:-shift_range]
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
                    
