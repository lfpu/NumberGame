def generate_random_numbers(level):
    return list(range(1, level + 1))

def is_adjacent(pos1, pos2):
    return (abs(pos1[0] - pos2[0]) == 1 and pos1[1] == pos2[1]) or (pos1[0] == pos2[0] and abs(pos1[1] - pos2[1]) == 1)

def create_grid(level):
    grid_size = level
    return [[None for _ in range(grid_size)] for _ in range(grid_size)]

def reset_grid(grid):
    for row in grid:
        for i in range(len(row)):
            row[i] = None

def display_grid(grid):
    for row in grid:
        print(" ".join(str(num) if num is not None else "." for num in row))