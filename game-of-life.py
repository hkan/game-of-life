# -*- coding: utf-8 -*-

import numpy as np

grid_presets = {
    "3,1:2,1": np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]),
    "9,3:7,3:5": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
}

neighbor_coord_deltas = [
    (-1, -1), # top left corner
    (-1,  0), # top
    (-1, +1), # top right corner
    ( 0, +1), # right
    (+1, +1), # bottom right corner
    (+1,  0), # bottom
    (+1, -1), # bottom left corner
    ( 0, -1), # left
]

def paint_grid(grid):
    for row in grid:
        for col in row:
            if col == 0:
                print('-', end='')
            else:
                print('#', end='')
        print('')

def debug_grid_data(data):
    for row in data:
        for col in row:
            print(' ' + str(int(col)) + ' ', end='')
        print('')

def neighbor_coords(row_number, col_number, row_size, col_size):
    list_of_all_neighbor_coords = list((row_number + r, col_number + c) for (r, c) in neighbor_coord_deltas)

    # This filtering process eliminates coordinates that fall outside of the grid such as (-1, 0), (-1, -1) etc.
    list_of_coords_within_grid = filter(
        lambda coords: True if coords[0] >= 0 and coords[0] < row_size and coords[1] >= 0 and coords[1] < col_size else False,
        list_of_all_neighbor_coords
    )
    
    # Running it through `list()` because the variable is actually a iterable, not list.
    return list(list_of_coords_within_grid)

def get_neighbors_map(grid):
    (row_size, col_size) = grid.shape
    neighbors_map = np.ndarray(grid.shape)
    neighbors_map.fill(0)

    for row_number in range(row_size):
        for col_number in range(col_size):
            for (neighbor_row, neighbor_col) in neighbor_coords(row_number, col_number, row_size, col_size):
                if grid[neighbor_row, neighbor_col] == 1:
                    neighbors_map[row_number][col_number] = neighbors_map[row_number][col_number] + 1

    return neighbors_map

def calculate_new_grid(neighbors_map: np.ndarray, grid: np.ndarray):
    (row_size, col_size) = neighbors_map.shape
    new_grid = np.ndarray(neighbors_map.shape)
    new_grid.fill(0)

    for row_number in range(row_size):
        for col_number in range(col_size):
            current_state = grid[row_number, col_number]

            # For only dead cells...            
            if current_state == 0:
                # If it has exactly 3 neighbors...
                if neighbors_map[row_number, col_number] == 3:
                    # It becomes populated.
                    new_grid[row_number, col_number] = 1
                continue

            # Rest of the checks are for alive cells...

            # If the cell has 2 or 3 neighbors, it lives for another day.
            if neighbors_map[row_number, col_number] == 2 or neighbors_map[row_number, col_number] == 3:
                new_grid[row_number, col_number] = 1
                continue
            
            # If the cell has no neighbors, 1 neighbor, OR more than 3 neighbors, it dies.
            new_grid[row_number, col_number] = 0

    return new_grid


def loop(grid):
    paint_grid(grid)
    input('Press enter to calculate next iteration, or kntrl+C to exit.')
    neighbors_map = get_neighbors_map(grid)
    grid = calculate_new_grid(neighbors_map, grid)
    loop(grid)

loop(
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
)

