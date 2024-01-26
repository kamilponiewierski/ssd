from asyncio import sleep
import lzma
import os
import pickle
import sys
import time
import Xlib.display
import pygame
import numpy as np
from random import randint

INPUT_MOCK_PATH = "growth_log_1a.pkl"
X = 320
Y = 200


def create_mock_array():
    start_time = time.time()
    x, y = X, Y
    arr = np.zeros((x, y))
    i, j = int(x / 2), int(y / 2)
    arr[i, j] = 1

    with lzma.open(INPUT_MOCK_PATH, "wb") as f:
        pickle.dump(arr, f)
        while i >= 0 and i < x and j >= 0 and j < y:
            arr[i, j] = 1
            i, j = i + randint(-1, 1), j + randint(-1, 1)
            pickle.dump(arr, f)

    print(f"Generating an array took: {time.time() - start_time}s")


def recolor_array(arr):
    levels = np.max(arr)

    match levels:
        case 1:
            return arr * 255
        # TODO handle coloring of fungi in model 4 - several (4?) distinct colors
        case _:
            raise NotImplementedError


def get_screen_resolution():
    screen = Xlib.display.Display().screen()
    return screen._data['width_in_pixels'], screen._data['height_in_pixels']


if __name__ == "__main__":

    args = sys.argv[1:]

    screen_width, screen_height = get_screen_resolution()

    input_file = args[0] if len(args) > 0 else INPUT_MOCK_PATH

    if input_file == INPUT_MOCK_PATH and not os.path.exists(INPUT_MOCK_PATH):
        create_mock_array()

    pygame.init()
    is_paused = True
    is_running = True

    with lzma.open(input_file, "rb") as input:
        arr: np.array = recolor_array(pickle.load(input))
        arr = np.transpose(arr)
        display = pygame.display.set_mode(
            (screen_width, screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Display Grid")

        while is_running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        is_running = False
                    elif event.type == pygame.VIDEORESIZE:
                        display = pygame.display.set_mode(
                            (event.w, event.h), pygame.RESIZABLE
                        )
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        is_paused = not is_paused

                if not is_paused:
                    arr: np.array = recolor_array(pickle.load(input))
                    arr = np.transpose(arr)
                    time.sleep(1 / 15)

                surf = pygame.surfarray.make_surface(arr)
                surf = pygame.transform.scale(surf, display.get_size())
                display.blit(surf, (0, 0))
                pygame.display.update()

            except EOFError:
                break
