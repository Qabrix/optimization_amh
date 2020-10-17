from random import randint, choice

def two_swap(path):
    i,  j = randint(0, len(path)-1), randint(0, len(path)-1)
    path[i], path[j] = path[j], path[i]

def rotate(path):
    i, j, k = randint(0, len(path)-1), randint(0, len(path)-1), randint(0, len(path)-1)
    path[i], path[j],  path[k] = path[j], path[k], path[i]

def four_two_swap(path):
    i, j = randint(0, len(path)-2), randint(0, len(path)-2)
    path[j], path[i] = path[i], path[j]
    path[j+1], path[i+1] = path[i+1], path[j+1]

def gen_neighbour(path):
    modified_path = path.copy()
    modify_option = randint(0, 2)

    if modify_option == 0:
        two_swap(modified_path)
    elif modify_option == 1:
        rotate(modified_path)
    elif modify_option == 2 and len(modified_path) > 4:
        four_two_swap(modified_path)
    return modified_path
