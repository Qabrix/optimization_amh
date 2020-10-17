import sys
from abc import ABC, abstractmethod


class Structure(ABC):
    def __init__(self, root=None):
        self.root = root
        self.count = 0
        self.find_counter = 0

    def __len__(self):
        return self.count

    def reset_find_counter(self):
        self.find_counter = 0
    @abstractmethod
    def insert(self, node):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def find(self, key):
        pass

    @abstractmethod
    def min(self):
        pass

    @abstractmethod
    def max(self):
        pass

    @abstractmethod
    def successor(self, key):
        pass

    @abstractmethod
    def inorder(self):
        pass

    def prepare_word(self, val):
        if val == None:
            return
        if len(val) > 0 and val[0] < "a" and val[0] < "A":
            val = val[1:]
        elif len(val) > 0 and val[0] > "z" and val[0] > "Z":
            val = val[1:]
        if len(val) > 0 and val[-1] < "a" and val[-1] < "A":
            val = val[:-1]
        elif len(val) > 0 and val[-1] > "z" and val[-1] > "Z":
            val = val[:-1]

        return val

    def load(self, file):
        max_len = 0
        for line in file:
            for word in line.split():
                word_len = len(word)
                if word_len > max_len:
                    max_len = word_len
                self.insert(word.lower())
        return max_len