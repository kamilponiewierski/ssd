from abc import ABC, abstractmethod
import numpy as np


class Cell(ABC):
    growth_probability: float
    food_source_count: int
    growth_stage: int
    position: (int, int)

    def grow_shroom(self, neighbourhood: np.array, global_growth_chance: float):
        model_growth_chance = self.calculate_growth_chance(neighbourhood)
        if self.growth_probability > global_growth_chance:
            if model_growth_chance > np.random.random():
                self.growth_stage += 1

    @abstractmethod
    def calculate_growth_chance(self, neighbourhood: np.array) -> float:
        pass

    def __init__(self, position: (int, int)) -> None:
        self.growth_probability = 0.0
        self.growth_stage = 0
        self.food_source_count = 0
        self.position = position


class CellModel1(Cell):
    def calculate_growth_chance(self, neighbourhood: np.array) -> float:
        if self.growth_stage > 0:
            return 0.0

        shroom_count = 0

        for cell in neighbourhood.flat:
            if cell.growth_stage > 0:
                shroom_count += 1

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
