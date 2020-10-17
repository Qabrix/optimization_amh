import sys
from .node import Node
from .structure import Structure
from .rbt import RbtStructure


class HmapStructure(Structure):
    def __init__(self, switch_size=50, htable_size=1000):
        super().__init__()
        self.switch_size = switch_size
        self.htable_size = htable_size
        self.htable, self.htable_sizes = self.__init_tables()

    def __init_tables(self):
        return (
            [[] for _ in range(self.htable_size)],
            [0 for _ in range(self.htable_size)],
        )

    def __get_hash_func(self, val):
        return hash(val) % self.htable_size

    def __switch(self, val_id, to_list=False):
        if to_list:
            self.htable[val_id] = list(self.htable[val_id])
        else:
            rbt = RbtStructure()
            for val in self.htable[val_id]:
                rbt.insert(val)
            self.htable[val_id] = rbt

    def insert(self, val):
        val = self.prepare_word(val)
        val_id = self.__get_hash_func(val)
        if self.htable_sizes[val_id] < self.switch_size:
            self.htable[val_id].append(val)
        elif self.htable_sizes[val_id] > self.switch_size:
            self.htable[val_id].insert(val)
        else:
            self.__switch(val_id)
            self.htable[val_id].insert(val)

        self.htable_sizes[val_id] += 1
        self.count += 1

    def __get_values(self):
        values = []
        for i in range(self.htable_size):
            if self.htable_sizes[i] > 0:
                if self.htable_sizes[i] > self.switch_size:
                    values += list(self.htable[i])
                else:
                    values += self.htable[i]
        return values

    def inorder(self):
        values = self.__get_values()
        values.sort()
        for val in values:
            sys.stdout.write(str(val) + " ")

    def successor(self, key):
        values = self.__get_values()
        values.sort()
        try:
            key_id = values.index(key)
            if key_id < len(values) - 1:
                return Node(val=values[key_id + 1])
            else:
                return None
        except:
            return None

    def min(self):
        min_val = -1
        for i in range(self.htable_size):
            if self.htable_sizes[i] > 0:
                if self.htable_sizes[i] > self.switch_size:
                    row_min = self.htable[i].min()
                    if row_min:
                        row_min = row_min.val
                    else:
                        row_min = ""
                else:
                    row_min = min(self.htable[i])

                if row_min < str(min_val) or min_val == -1:
                    min_val = row_min

        if min_val != -1:
            return Node(val=min_val)
        else:
            return None

    def max(self):
        max_val = -1
        for i in range(self.htable_size):
            if self.htable_sizes[i] > 0:
                if self.htable_sizes[i] > self.switch_size:
                    row_max = self.htable[i].max()
                    if row_max:
                        row_max = row_max.val
                    else:
                        row_max = ""
                else:
                    row_max = max(self.htable[i])

                if row_max > str(max_val) or max_val == -1:
                    max_val = row_max
        if max_val != -1:
            return Node(val=max_val)
        else:
            return None

    def find(self, key):
        self.reset_find_counter()
        key_id = self.__get_hash_func(key)
        self.find_counter+=1
        if self.htable_sizes[key_id] <= self.switch_size:
            if key in self.htable[key_id]:
                return Node(val=key)
        else:
            node = self.htable[key_id].find(key)
            self.find_counter += self.htable[key_id].find_counter
            return node

        return None

    def delete(self, key):
        key_id = self.__get_hash_func(key)
        if self.htable_sizes[key_id] <= self.switch_size:
            if key in self.htable[key_id]:
                self.htable[key_id].remove(key)
                self.htable_sizes[key_id] -= 1
                self.count -= 1
        else:
            if self.htable[key_id].delete(key):
                self.htable_sizes[key_id] -= 1
                self.count -= 1
                if self.htable_sizes[key_id] <= self.switch_size:
                    self.__switch(key_id, True)
