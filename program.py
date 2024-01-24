import lzma
import pickle
import time
import numpy as np

from cell import CellModel1a, CellModel1c, CellModel2a

SIZE_Y = 320
SIZE_X = 200

# TODO maybe add CLI support?
OUTPUT_PATH = 'growth_log_2a.pkl'



def create_cell_array() -> np.array:
    x, y = SIZE_X, SIZE_Y
    arr = np.empty(shape=(x, y), dtype=object)
    for i in range(x):
        for j in range(y):
            arr[i][j] = CellModel2a((i, j))

    center_x, center_y = x // 2, y // 2
    arr[center_x, center_y].growth_stage = 1
    return arr


def save_array_state(arr, file):
    vectorized_stage = np.vectorize(lambda cell: cell.growth_stage)
    pickle.dump(vectorized_stage(arr), file)


def step(arr):
    new_arr = np.zeros(arr.shape, dtype=np.int16)
    y_size, x_size = arr.shape
    global_grow_chance = np.random.normal()

    for row in range(1, y_size-1):
        for col in range(1, x_size-1):
            window = arr[row-1:row+2, col-1:col+2]
            new_arr[row][col] = arr[row][col].grow_shroom(
                window, global_grow_chance)

    for row in range(1, y_size-1):
        for col in range(1, x_size-1):
            arr[row][col].growth_stage = new_arr[row][col]


def reroll_probabilities(arr):
    y_size, x_size = arr.shape
    new_random = np.random.normal(size=(y_size, x_size))

    for i in range(y_size):
        for j in range(x_size):
            arr[i][j].growth_chance = new_random[i][j]



def mature_unocupied_cells(arr: np.array(CellModel2a) ) -> None:
    # with each step it is obligated to mature unoccupied cells in 2a model
    y_size, x_size = arr.shape
    global_mature_chance = np.random.normal()


    for row in range(1, y_size - 1):
        for col in range(1, x_size - 1):

            if arr[row,col].growth_stage == 0:
                window = arr[row - 1:row + 2, col - 1:col + 2]
                arr[row,col].matureUnocupiedCell(window, global_mature_chance)


if __name__ == "__main__":
    cells = create_cell_array()
    with lzma.open(OUTPUT_PATH, 'wb') as output:
        generation_i = 0
        while True:
            generation_i += 1
            start = time.time()

            # with each step it is obligated to mature unoccupied cells in 2a model
            if isinstance(cells[0, 0], CellModel2a):
                mature_unocupied_cells(cells)

            reroll_probabilities(cells)
            step(cells)
            save_array_state(cells, output)

            reached_border = False

            for border in [cells[1, :], cells[-2, :], cells[:, 1], cells[:, -2]]:
                for cell in border:
                    if cell.growth_stage == 1 :
                        reached_border = True
                        break

            if reached_border:
                break

            print(f'Generation {generation_i}, took {time.time() - start}s')
