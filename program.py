import lzma
import pickle
import time
import numpy as np

from cell import Cell, CellModel1

SIZE_Y = 720
SIZE_X = 1280

# TODO maybe add CLI support?
OUTPUT_PATH = 'growth_log.pkl'

def create_cell_array() -> np.array:
    x, y = SIZE_Y, SIZE_X
    arr = np.empty(shape=(x, y), dtype=object)
    for i in range(x):
        for j in range(y):
            arr[i][j] = CellModel1((i, j))

    center_x, center_y = x // 2, y // 2
    arr[center_x, center_y].growth_stage = 1
    return arr


def save_array_state(arr, file):
    vectorized_stage = np.vectorize(lambda cell: cell.growth_stage)
    pickle.dump(vectorized_stage(arr), file)


def step(arr):
    y_size, x_size = arr.shape
    global_grow_chance = np.random.normal()

    for row in range(1,y_size-1):
        for col in range(1,x_size-1):
            window = arr[row-1:row+2, col-1:col+2]
            arr[row][col].grow_shroom(window, global_grow_chance)
    

def reroll_probabilities(arr):
    y_size, x_size = arr.shape
    new_random = np.random.normal(size=(y_size, x_size))

    for i in range(y_size):
        for j in range(x_size):
            arr[i][j].growth_chance = new_random[i][j]

if __name__ == "__main__":
    cells = create_cell_array()
    with lzma.open(OUTPUT_PATH, 'wb') as output:
        generation_i = 0
        while True:
            generation_i += 1
            start = time.time()
            #TODO deepcopy before each step may be necessary
            reroll_probabilities(cells)
            step(cells)
            save_array_state(cells, output)

            reached_border = False

            for border in [cells[1, :], cells[-2, :], cells[:, 1], cells[:, -2]]:
                for cell in border:
                    if cell.growth_stage == 1:
                        reached_border = True
                        break

            if reached_border:
                break

            print(f'Generation {generation_i}, took {time.time() - start}s')
            