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
        self.generation = self._gen_generation(starter_words)

    def __iter__(self):
        for inhabitant in self.generation:
            yield inhabitant

    def _random_word(self):
        return random.sample(self.all_puzzle_keys, len(self.all_puzzle_keys))

    def _gen_generation(self, starter_words):
        min_size = min([len(word) for word in starter_words])
        max_size = max([len(word) for word in starter_words])
        generation = []
        for word in starter_words:
            generation.append(Inhabitant(list(word)))
        for _ in range(len(starter_words), self.population_size):
            word = self._random_word()[: random.randint(min_size, max_size)]
            generation.append(Inhabitant(word))
        return generation

    def sorted_generation(self):
        return sorted(self.generation, key=lambda x: x.value, reverse=True)

    def make_selection(self, elite_percentage, percentage=0.75):
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

    def recombinate(self, elite_percentage=0.6):
        selection = self.make_selection(elite_percentage)
        permutation = np.random.permutation(len(selection))
        new_generation = []
        new_generation.append(Inhabitant(selection[0].gene.copy()))
        new_generation.append(Inhabitant(selection[1].gene.copy()))
        for i in range(1, len(permutation)):
            pivot = random.randint(
                0,
                min(
                    len(selection[permutation[i % len(permutation)]]),
                    len(selection[permutation[(i + 1) % len(permutation)]]),
                )
                // 2,
            )

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

    def mutate(
        self,
        min_swap_probability=0.2,
        max_swap_probability=0.8,
        inverse_probability=0.001,
        random_probability=0.005,
        shift_probability=0.001,
        insert_probability=0.8,
    ):
        swap_probability = random.uniform(min_swap_probability, max_swap_probability)
        for inhabitant in self.generation[1:]:
            if decision(insert_probability):
                insert_amount = random.randint(1, 2)
                if decision(0.5): # remove decision
                    if(len(inhabitant)+insert_amount < len(self.all_puzzle_keys)):
                        possible_chars = self._random_word()
                        for char in inhabitant.gene:
                            if char in possible_chars:
                                possible_chars.remove(char)
                        if decision(0.33):  
                            inhabitant.gene += possible_chars[:insert_amount]
                        elif decision(0.5):
                            inhabitant.gene = possible_chars[:insert_amount] + inhabitant.gene
                        else:
                            insert_index = random.randint(1, len(inhabitant.gene)) 
                            inhabitant.gene = inhabitant.gene[:insert_index] + possible_chars[:insert_amount] + inhabitant.gene[insert_index:]
                else:
                    if(len(inhabitant)-insert_amount > 0):
                        if decision(0.5):  
                            inhabitant.gene = inhabitant.gene[insert_amount:]
                        else:
                            inhabitant.gene = inhabitant.gene[:-insert_amount]
                            
            elif decision(random_probability):
                inhabitant.gene = self._random_word()
            else:
                if decision(shift_probability):
                    shift_range = random.randint(1, 3)
                    for _ in range(shift_range + 1):
                        inhabitant.gene = [inhabitant.gene[-1]] + inhabitant.gene[:-1]

                for i in range(len(inhabitant.gene) // 2):
                    if decision(swap_probability):
                        random_id = random.randint(0, len(inhabitant) - 1)
                        inhabitant.gene[i], inhabitant.gene[random_id] = (
                            inhabitant.gene[random_id],
                            inhabitant.gene[i],
                        )

                if decision(inverse_probability):
                    inhabitant.gene = inhabitant.gene[::-1]