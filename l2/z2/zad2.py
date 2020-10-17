import sys
import time
import math
import random
import numpy as np

from puzzle import Puzzle
from utils import decision
from puzzle_placer import PuzzleShuffler

def get_input():
    matrix = []
    splited_line = str(input()).split()
    int_input = [int(x) for x in splited_line]
    t = int_input[0]
    n = int_input[1]
    m = int_input[2]
    k = int_input[3]
    for i in range(1,n+1):
        row = []
        splited_line = str(input()).split()
        for i in range(m):
            row.append(int(splited_line[i]))
        matrix.append(row)
    return t,n,m,k,matrix

def calculate_mse(n,m,matrix,matrixp):
    result = 0.0
    for i in range(n):
        for j in range(m):
            result += np.square(matrix[i][j] - matrixp[i][j])
        
    result /= n*m
    return result

def calculate_probability(T,n,m,matrix,matrixx,matrixy):
    fy, fx = calculate_mse(n,m,matrix,matrixy), calculate_mse(n,m,matrix,matrixx)
    result = 1/(1+np.exp((fy-fx)/T))
    return result

def decrease_temperature(T, c=0.99):
    T *= c
    return T

def check_time(start,t):
    return time.time()-start < t 

def calculate_matrixp(puzzles, matrix, n, m):
    matrixp = [ [ 0 for _ in range(m) ] for _ in range(n) ]  
    for puzzle in puzzles:
        puzzle_mean = puzzle.calculate_mean(matrix)
        for i in range(puzzle.point1[0],puzzle.point2[0]):
            for j in range(puzzle.point1[1],puzzle.point2[1]):
                matrixp[i][j] = puzzle_mean
    return matrixp

def calc_square_number(puzzles):
    result = 0
    for puzzle in puzzles:
        if puzzle.is_square:
            result += 1

    return result 

def sa(t, n, m, k, matrix, start_T, multiplier=2):
    start = time.time()
    T = start_T
    puzzle_shuffler = PuzzleShuffler()

    puzzles = puzzle_shuffler.random_puzzles(n, m, k, matrix)
    matrixp = calculate_matrixp(puzzles, matrix, n, m)    
    best_matrixp = matrixp
    best_puzzles = puzzles.copy()
    shuffle_puzzles = puzzles.copy()

    square_number = calc_square_number(puzzles)
    
    best_min = calculate_mse(n, m, matrix, matrixp)
    fail_counter = 0

    while check_time(start,t) and T > 0:  
        puzzles = puzzle_shuffler.random_puzzles(n, m, k, matrix)
        matrixp = calculate_matrixp(puzzles, matrix, n, m)
        cur_min = calculate_mse(n, m, matrix, matrixp)
        if cur_min < best_min:
            best_matrixp = matrixp.copy()
            best_puzzles = puzzles.copy()
            fail_counter = 0
            best_min = cur_min
        else:
            fail_counter += 1

        probability = calculate_probability(T,n,m,matrix,best_matrixp,matrixp)
        if decision(probability) and cur_min != best_min:
            T = decrease_temperature(T)
            shuffle_puzzles = puzzles.copy()

        if fail_counter == square_number*multiplier:
            fail_counter = 0
            puzzle_shuffler.set_T(best_puzzles, int(random.uniform(0,square_number//2)))
            puzzle_shuffler.set_starters(best_puzzles,  int(random.uniform(0,square_number//2)))
            shuffle_puzzles = puzzle_shuffler.random_puzzles(n, m, k, matrix)
        elif fail_counter >= square_number*multiplier//2:
            if fail_counter == square_number*multiplier//2:
                puzzle_shuffler.set_T(best_puzzles, 0)
                puzzle_shuffler.set_starters(best_puzzles, 8)
            else:
                puzzle_shuffler.set_starters(best_puzzles,square_number-int(random.uniform(2,square_number//2)))
        else:
            puzzle_shuffler.set_starters(shuffle_puzzles, int(random.uniform(0,square_number//2)))
        

    return best_min, best_matrixp

def main():
    T = 1000
    t,n,m,k,matrix = get_input()
    
    best_min, best_matrixp = sa(t,n,m,k,matrix,T)
    sys.stdout.write(str(best_min))
    for row in best_matrixp:
        sys.stderr.write(str(row)+"\n")
    
if __name__ == "__main__":
    main()