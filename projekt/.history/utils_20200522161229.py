import time

def get_input():
    splited_input = str(input()).split(" ")

    t = float(splited_input[0])
    n = int(splited_input[1])
    m = int(splited_input[2])
    s = int(splited_input[3])
    p = int(splited_input[4])

    pos = []
    grid = []
    starters = []

    for row in range(n):
        line = str(input())
        if '5' in line:
            pos.append(row)
            pos.append(line.index('5'))
        temp = []
        for field in line:
            if field != '\n':
                temp.append(field)
        grid.append(temp)
    
    for row in range(s):
        starters.append(list(str(input())))

    return t, n, m, s, p,  grid, pos, starters

def check_time(start, t):
    return time.time()-start < t 