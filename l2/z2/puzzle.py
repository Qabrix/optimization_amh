from dataclasses import dataclass
from numpy import mean

@dataclass
class Puzzle:
    point1: tuple
    point2: tuple
    is_square: bool = True

    def calc_distance(self, other):
        dist1, dist2 = -1, -1
        if self.point1[1] >= other.point2[1]:
            dist2 = self.point1[1] - other.point2[1]
        elif self.point2[1] <= other.point1[1]:
            dist2 = other.point1[1] - self.point2[1]

        if self.point2[0] <= other.point1[0]:
            dist1 =  other.point1[0] - self.point2[0]
        elif self.point1[0] >= other.point2[0]:
            dist1 = self.point1[0] - other.point2[0]
        
        return dist1, dist2
    
    def calculate_mean(self, matrix, values = [0, 32, 64, 128, 160, 192, 223, 255]):
        matrix_values = []
        for i in range(self.point1[0], self.point2[0]):
            for j in range(self.point1[1], self.point2[1]):
                matrix_values.append(matrix[i][j])
        return min(values, key=lambda x:abs(x-mean(matrix_values)))
