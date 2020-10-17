import time
import random

def get_input():
    puzzles = {}
    all_puzzle_keys = []
    possibile_solutions = []
    splited_line = str(input()).split()
    int_input = [int(x) for x in splited_line]
    t = int_input[0]
    n = int_input[1]
    s = int_input[2]

    for _ in range(n):
        splited_line = str(input()).split()
        puzzles[splited_line[0]] = splited_line[1]
        all_puzzle_keys.append(splited_line[0])

    for _ in range(s):
        word = str(input())
        possibile_solutions.append(word)

    return t, n, s, puzzles, possibile_solutions, all_puzzle_keys

def check_time(start, t):
    return time.time()-start < t 

def calculate_value(word, puzzles):
    return sum(int(puzzles[char]) for char in word)

def decision(probability):
    return random.random() < probability
