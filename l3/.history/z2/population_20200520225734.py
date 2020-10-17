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

    def get_str_gene(self, up):
        return "".join(self.gene[:up])


class Population:
    def __init__(self, puzzles, population_size, word_size):
        self.puzzles = puzzles
        self.best_res = None
        self.population_size = population_size
        self.word_size = word_size
        self.generation = self._gen_generation(word_size)

    def __iter__(self):
        for inhabitant in self.generation:
            yield inhabitant

    def _random_char(self):
        return random.choice(list(self.puzzles))

    def _gen_generation(self, inhabitant_size):
        return [
            Inhabitant([self._random_char() for _ in range(inhabitant_size)])
            for _ in range(self.population_size)
        ]

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

    def recombinate(self):
        selection = self.make_selection()
        permutation = np.random.permutation(len(selection))
        new_generation = []
        for i in range(0, len(permutation), 2):
            pivot1 = random.randint(0, self.word_size // 2)
            pivot2 = random.randint(0, self.word_size // 2 + 1)
            new_generation.append(
                Inhabitant(
                    selection[permutation[i]][:pivot1]
                    + selection[permutation[i + 1]][pivot1:pivot2]
                    + selection[permutation[i]][pivot2:]
                )
            )
            new_generation.append(
                Inhabitant(
                    selection[permutation[i + 1]][:pivot1]
                    + selection[permutation[i]][pivot1:pivot2]
                    + selection[permutation[i + 1]][pivot2:]
                )
            )
        
        self.generation = new_generation

    def mutate(self, probability=0.01):
        for inhabitant in self.generation:
            for i in range(len(inhabitant.gene)):
                if decision(probability):
                    inhabitant.gene[i] = self._random_char()
