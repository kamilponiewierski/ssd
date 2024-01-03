import random
import numpy as np
from numpy.core.multiarray import array as array


class Cell:
    growth_probability: float
    food_source_count: int
    growth_stage: int
    position: (int, int)

    def grow_shroom(self, neighbourhood: np.array, global_grow_chance):
        pass

    def __init__(self) -> None:
        self.growth_probability = 0.0
        self.growth_stage = 0


class CellModel1(Cell):
    def __init__(self, position) -> None:
        self.position = position
        super().__init__()

    def grow_shroom(self, neighbourhood: np.array, global_grow_chance):
        growth_chance = self.calculate_growth_chance(neighbourhood)
        #TODO variable names
        if self.growth_probability > global_grow_chance:
            if  growth_chance > np.random.random():
                self.growth_stage = 1


    def calculate_growth_chance(self, neighbourhood) -> float:
        shroom_count = 0

        for cell in neighbourhood.flat:
            if cell.growth_stage > 0:
                shroom_count += 1

        if self.growth_stage > 0:
            shroom_count -= 1

        match shroom_count:
            case 0:
                return 0.0
            case 1:
                return 0.125
            case 2:
                return 0.25
            case 3:
                return 0.50
            case _:
                return 0.0
                
                        