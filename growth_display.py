from asyncio import sleep
import lzma
import os
import pickle
import sys
import time
import pygame
import numpy as np
from random import randint

INPUT_MOCK_PATH = 'growth_log.pkl'
X = 300
Y = 200

def create_array():
    start_time = time.time()
    x, y = X, Y
    arr = np.zeros((x, y))
    i, j = int(x / 2), int(y / 2)   
    arr[i, j] = 1

    with lzma.open(INPUT_MOCK_PATH, 'wb') as f:
        pickle.dump(arr, f)
        while (i >= 0 and i < x and j >= 0 and j < y):
            arr[i, j] = 1
            i, j = i + randint(-1, 1), j + randint(-1, 1)
            pickle.dump(arr, f)
    
    print(f'Generating an array took: {time.time() - start_time}s')


def recolor_array(arr):
    levels = np.max(arr)

    match levels:
        case 1:
            return arr * 255
        # TODO handle coloring of fungi in model 4 - several (4?) distinct colors
        case _:
            raise NotImplementedError


if __name__ == '__main__':
    args = sys.argv[1:]

    input_file = args[0] if len(args) > 0 else INPUT_MOCK_PATH

    if input_file == INPUT_MOCK_PATH and not os.path.exists(INPUT_MOCK_PATH):
        create_array()

    pygame.init()
    running = True
    display = None

    with lzma.open(input_file, 'rb') as input:
        while running:
            try:
                arr: np.array = recolor_array(pickle.load(input))
                time.sleep(1/480)
                if display is None:
                    display = pygame.display.set_mode(arr.shape)

                surf = pygame.surfarray.make_surface(arr)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                display.blit(surf, (0, 0))
                pygame.display.update()
            except EOFError:
                break
        pygame.quit()
