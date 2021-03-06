from random import randint

class MovesManager():
    def __init__(self):
        self.possible_moves = ['U', 'D', 'L', 'R']
    def validate_move(self, step, pos, grid):
        if step == 'U' and grid[pos[0]-1][pos[1]] != '1':
            return True
        elif step == 'D' and grid[pos[0]+1][pos[1]] != '1':
            return True
        elif step == 'L' and grid[pos[0]][pos[1]-1] != '1':
            return True
        elif step == 'R' and grid[pos[0]][pos[1]+1] != '1':
            return True
        else:
            return False

    def move(self, step, grid):
        if step == 'U':
            grid[0] += -1
        elif step == 'D':
            grid[0] += 1
        elif step == 'L':
            grid[1] += -1
        elif step == 'R':
            grid[1] += 1


    def explore(self, pos, path, grid):
        new_path = []
        for step in path:
            if self.validate_move(step, pos, grid):
                self.move(step, pos)
                new_path += [step]
            if self.check_for_exit(pos, grid):
                return new_path, True
        return new_path, False

    def random_moves(self, pos, grid, n, m, step_limit):
        path = []
        step = ''

        while len(path) <= step_limit:
            step = possible_moves[randint(0, 3)]
            while not self.validate_move(step, pos, grid):
                step = possible_moves[randint(0, 3)]
            
            for _ in range(randint(1, min(n, m))):
                if not self.validate_move(step, pos, grid):
                    break
                self.move(step, pos)
                path += [step]
                if self.check_for_exit(pos, grid):
                    return path
        return path

    def check_for_exit(self, pos, grid):
        return grid[pos[0]][pos[1]] == '8' or (
            grid[pos[0]][pos[1] + 1] == '8' or
            grid[pos[0] + 1][pos[1]] == '8' or
            grid[pos[0]][pos[1] - 1] == '8' or
            grid[pos[0] - 1][pos[1]] == '8'
        )
