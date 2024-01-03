import lzma
import pickle
import numpy as np

from cell import Cell, CellModel1

SIZE_X = 300
SIZE_Y = 200

# TODO maybe add CLI support?
OUTPUT_PATH = 'growth_log.pkl'

def create_cell_array() -> np.array:
    x, y = SIZE_X, SIZE_Y
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
    x_size, y_size = arr.shape

    for i in range(x_size):
        for j in range(y_size):
            neighbourhood = arr[max(
                0, i - 2): min(x_size - 1, i + 1), max(0, j - 2): min(y_size - 1, j + 1)]
            arr[i][j].grow_shroom(neighbourhood)

def reroll_probabilities(arr):
    x_size, y_size = arr.shape
    new_random = np.random.random(size=(x_size, y_size))

    for i in range(x_size):
        for j in range(y_size):
            arr[i][j].growth_chance = new_random[i][j]

if __name__ == "__main__":
    cells = create_cell_array()
    with lzma.open(OUTPUT_PATH, 'wb') as output:
        for r in range(150):
            #TODO deepcopy before each step may be necessary
            reroll_probabilities(cells)
            step(cells)
            save_array_state(cells, output)
