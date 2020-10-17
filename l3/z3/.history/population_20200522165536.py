import random
import numpy as np
from utils import decision
from neighboor import gen_neighbour
from moves_manager import MovesManager



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
    def __init__(self, population_size, starter_words, moves_manager: MovesManager):
        self.moves_manager = moves_manager
        self.population_size = population_size
        self.all_puzzles = moves_manager.possible_moves
        self.generation = self._gen_generation(starter_words)

    def __iter__(self):
        for inhabitant in self.generation:
            yield inhabitant

    def _random_word(self, length):
        return [random.choice(self.all_puzzles) for _ in range(length)]

    def _random_moves(self):
        return self.moves_manager.random_moves(
            self.moves_manager.start_pos,
            self.moves_manager.grid,
            self.moves_manager.n,
            self.moves_manager.m,
            (self.moves_manager.n - 2) * (self.moves_manager.m - 2),
        )

    def _gen_generation(self, starter_words):
        generation = []
        for word in starter_words:
            generation.append(Inhabitant(list(word)))
        for _ in range(len(starter_words), self.population_size):
            word = self._random_moves()
            generation.append(Inhabitant(word))
        return generation

    def sorted_generation(self):
        return sorted(self.generation, key=lambda x: x.value, reverse=True)

    def make_selection(self, elite_percentage, percentage=0.5):
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
            if len(new_generation) < self.population_size:
                new_generation.append(Inhabitant(new_word))

            new_word = (
                selection[permutation[(i + 1) % len(permutation)]][:pivot]
                + selection[permutation[i % len(permutation)]][pivot:]
            )
            if len(new_generation) < self.population_size:
                new_generation.append(Inhabitant(new_word))

        self.generation = new_generation

    def mutate(
        self,
        min_swap_probability=0.2,
        max_swap_probability=0.7,
        inverse_probability=0.001,
        shift_probability=0.001,
        insert_probability=0.1,
    ):
        swap_probability = random.uniform(min_swap_probability, max_swap_probability)
        for inhabitant in self.generation[1:]:
            if decision(insert_probability):
                insert_amount = random.randint(1, 2)
                if decision(0.5):  # remove decision
                    possible_chars = self._random_word(insert_amount)
                    if decision(0.33):
                        inhabitant.gene += possible_chars
                    elif decision(0.5):
                        inhabitant.gene = possible_chars + inhabitant.gene
                    else:
                        insert_index = random.randint(1, len(inhabitant.gene))
                        inhabitant.gene = (
                            inhabitant.gene[:insert_index]
                            + possible_chars
                            + inhabitant.gene[insert_index:]
                        )
                else:
                    if len(inhabitant) - insert_amount > 0:
                        if decision(0.33):
                            inhabitant.gene = inhabitant.gene[insert_amount:]
                        elif decision(0.5):
                            inhabitant.gene = inhabitant.gene[:-insert_amount]
                        else:
                            remove_index = random.randint(1, len(inhabitant.gene)-insert_amount)
                            inhabitant.gene = (
                            inhabitant.gene[:remove_index]
                            + inhabitant.gene[remove_index+insert_amount:]
                        )
            else:
                if decision(shift_probability):
                    shift_range = random.randint(1, 3)
                    for _ in range(shift_range + 1):
                        inhabitant.gene = [inhabitant.gene[-1]] + inhabitant.gene[:-1]

                if decision(swap_probability):
                    inhabitant.gene = gen_neighbour(inhabitant.gene)

                if decision(inverse_probability):
                    inhabitant.gene = inhabitant.gene[::-1]
