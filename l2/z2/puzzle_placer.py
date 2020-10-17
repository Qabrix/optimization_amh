import math
import random
import numpy as np
from puzzle import Puzzle
from utils import decision

class PuzzleShuffler():
    def __init__(self):
        self.T = []
        self.starters = []

    def set_starters(self, puzzles, amount):
        self.starters = []
        random.shuffle(puzzles)

        while amount > 0:
            for puzzle in puzzles:
                if puzzle.is_square and puzzle.point1 not in self.T:
                    amount -= 1
                    self.starters.append(puzzle.point1)   
                if amount == 0:
                    break  

    def set_T(self, puzzles, amount):
        self.T = []
        random.shuffle(puzzles)

        while amount > 0:
            for puzzle in puzzles:
                if puzzle.is_square:
                    amount -= 1
                    self.T.append(puzzle.point1)   
                if amount == 0:
                    break   


    def check_if_can_place_square(self, index, n, m, k, ocupied_fields, puzzles):
        puzzle = Puzzle(point1=(index[0],index[1]),point2=(index[0]+k,index[1]+k))
        for p in puzzles:
            dist1, dist2 = puzzle.calc_distance(p)
            if dist1 == -1:
                if dist2 == -1:
                    return False
                if dist2 != 0 and dist2 < k:
                    return False
            if dist2 == -1:
                if dist1 != 0 and dist1 < k:
                    return False
            if dist1 < k and dist2 < k and dist1 > 0 and dist2 > 0:
                return False
            
        horizontal_left = m - sum(ocupied_fields[index[0]])
        vertical_left = n - sum(row[index[1]] for row in ocupied_fields)

        return ((horizontal_left-k == 0 or horizontal_left-k>=k) and (vertical_left-k == 0 or vertical_left-k>=k))

    def initialize_square_indexes(self, n, m, k):
        l_indexes = [ (i,j) for i in range(0,n,k) for j in range(0,m,k) if (i+2*k <= n or i+k == n) and (j+2*k<=m or j+k == m)]  
        d_indexes = [ (i,j) for i in range(n-k,-1,-1*k) for j in range(0,m,k) if (i >=k or i==0) and (j+2*k<=m or j+k == m)]
        r_indexes = [ (i,j) for i in range(0,n,k) for j in range(m-k,-1,-1*k) if (i+2*k <= n or i+k == n) and (j >=k or j==0)]
        u_indexes = [ (i,j) for i in range(n-k,-1,-1*k) for j in range(m-k,-1,-1*k) if (i >=k or i==0) and (j >=k or j==0)]

        return l_indexes, r_indexes, u_indexes, d_indexes

    def place_squares(self, free_indexes, puzzles, k, n, m):
        left_squares = m//k if m%k == 0 else m//k-1
        left_squares = n//k * left_squares if n%k == 0 else (n//k-1) * left_squares
        ocupied_fields = [ [ 0 for _ in range(m) ] for _ in range(n) ]  
        random.shuffle(free_indexes)

        for index in self.starters:
            left_squares -= 1
            self.set_puzzle(ocupied_fields,puzzles, index, (k, k))

        for index in free_indexes :
            if left_squares == 0:
                break
            
            if self.check_if_can_place_square(index, n, m, k, ocupied_fields, puzzles) and index not in self.T:
                left_squares -= 1
                self.set_puzzle(ocupied_fields,puzzles, index, (k, k))


        return ocupied_fields, puzzles

    def check_if_rectangle_fits(self, ocupied_fields, rect_type, k, i, j, n, m):
        if i + rect_type[0] > n or j + rect_type[1] > m:
            return False

        uph_sum, downh_sum, leftv_sum, rightv_sum = 0, 0, 0, 0
        for val in ocupied_fields[i][j:]:
            if val == 1:
                break
            uph_sum += 1
        
        for val in ocupied_fields[i+rect_type[0]-1][j:]:
            if val == 1:
                break
            downh_sum += 1
        
        for row in ocupied_fields[i:]:
            if row[j] == 1:
                break
            leftv_sum += 1
        
        for row in ocupied_fields[i:]:
            if row[j+rect_type[1]-1] == 1:
                break
            rightv_sum += 1

        uph_sum -= rect_type[1]
        downh_sum -= rect_type[1]
        leftv_sum -= rect_type[0]
        rightv_sum -= rect_type[0]

        if rect_type[2] == 2 and (uph_sum%k != 0 or downh_sum%k != 0):
            return False

        return (uph_sum >= k or uph_sum == 0) and (downh_sum  >= k or downh_sum == 0) and (leftv_sum  >= k or leftv_sum == 0) and (rightv_sum  >= k or rightv_sum == 0) 

    def set_puzzle(self, ocupied_fields, puzzles, point, size, mark=1, is_square=True):
        puzzles.append(Puzzle(point1=(point[0], point[1]),point2=(point[0]+size[0],point[1]+size[1]),is_square=is_square))
        for i in range(size[0]):
            for j in range(size[1]):
                ocupied_fields[point[0]+i][point[1]+j] = mark

    def fill_rectangles(self, ocupied_fields, puzzles, k, n, m):
        size_x1, size_x2, size_y1, size_y2 = k, k+m%k, k+n%k, k
        rectangle_types = [(size_y1, size_x1, 0), (size_y2, size_x2, 1), (size_y1, size_x2, 2)]
        max_n = n-n%k+1 if n%k != 0 else n
        max_m = m-m%k+1 if m%k != 0 else m

        for i in range(max_n):
            j = 0
            while j < max_m:
                if ocupied_fields[i][j] == 0:
                    random.shuffle(rectangle_types)
                    for random_type in rectangle_types:
                        if self.check_if_rectangle_fits(ocupied_fields, random_type, k, i, j, n, m):
                            if random_type[2] == 0:
                                self.set_puzzle(ocupied_fields, puzzles, (i,j), random_type, 2, False)
                            elif random_type[2] == 1:
                                self.set_puzzle(ocupied_fields, puzzles, (i,j), random_type, 8, False)
                            elif random_type[2] == 2:
                                self.set_puzzle(ocupied_fields, puzzles, (i,j), random_type, 7, False)
                                rectangle_types.remove(random_type)
                            j+=random_type[1]-1
                            break
                j+=1     

        return ocupied_fields, puzzles

    def random_puzzles(self, n, m, k, matrix):
        l_indexes, r_indexes, u_indexes, d_indexes = self.initialize_square_indexes(n, m, k)
        free_indexes = r_indexes + u_indexes + d_indexes + l_indexes
        ocupied_fields, puzzles = self.place_squares(free_indexes, [], k, n, m)
        ocupied_fields, puzzles = self.fill_rectangles(ocupied_fields, puzzles, k, n, m) 
        return puzzles