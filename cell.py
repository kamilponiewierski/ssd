from abc import ABC, abstractmethod
import numpy as np
import random


class Cell(ABC):
    growth_probability: float
    food_source_count: int
    growth_stage: int
    position: (int, int)

    def grow_shroom(
        self, neighbourhood: np.array, global_growth_chance: float, direction: int
    ) -> int:
        new_growth_stage = self.growth_stage

        model_growth_chance = self.calculate_growth_chance(neighbourhood, direction)
        if self.growth_probability > global_growth_chance:
            if model_growth_chance > np.random.random():
                new_growth_stage += 1

        return new_growth_stage

    @abstractmethod
    def calculate_growth_chance(self, neighbourhood: np.array, direction: int) -> float:
        pass

    def __init__(self, position: (int, int)) -> None:
        self.growth_probability = 0.0
        self.growth_stage = 0
        self.food_source_count = 0
        self.position = position


class CellModel1a(Cell):
    def _calculate_growth_chance(self, neighbour_count):
        match neighbour_count:
            case 1:
                return 0.125
            case 2:
                return 0.25
            case 3:
                return 0.50
            case _:
                return 0.0

    def calculate_growth_chance(self, neighbourhood: np.array, direction: int) -> float:
        if self.growth_stage > 0:
            return 0.0

        shroom_count = sum(1 for cell in neighbourhood.flat if cell.growth_stage > 0)

        return self._calculate_growth_chance(shroom_count)


class CellModel1b(CellModel1a):
    def _calculate_growth_chance(self, neighbour_count):
        match neighbour_count:
            case 1:
                return 0.500
            case 2:
                return 0.250
            case 3:
                return 0.125
            case _:
                return 0.000


class CellModel1c(CellModel1a):
    def _calculate_growth_chance(self, neighbour_count):
        match neighbour_count:
            case 1:
                return 0.125
            case _:
                return 0.000


class CellModel2a(CellModel1c):
    def __init__(self, position: (int, int)) -> None:
        super().__init__(position)
        self.maturity_phase = 0

    def grow_shroom(
        self, neighbourhood: np.array, global_growth_chance: float, direction: int = -1
    ) -> int:
        new_growth_stage = self.growth_stage

        model_growth_chance = self.calculate_growth_chance(neighbourhood, direction)
        if self.growth_probability > global_growth_chance:
            if model_growth_chance > np.random.random():
                if self.maturity_phase < 4:
                    new_growth_stage += 1

        return new_growth_stage

    def matureUnocupiedCell(
        self, window: np.array(Cell), global_mature_chance: float
    ) -> None:
        ocupiedCellsNumber = 0

        for cell in window.flatten():
            if cell.growth_stage > 0:
                ocupiedCellsNumber += 1

        matureChance = self.calculateMatureChance(ocupiedCellsNumber)
        if self.growth_probability > global_mature_chance:
            if random.random() < matureChance:
                self.maturity_phase += 1

    def calculateMatureChance(self, ocupiedCellsNumber: int):
        match ocupiedCellsNumber:
            case 0:
                return 0.0
            case 1:
                return 0.5
            case 2:
                return 0.75
            case _:
                return 1.0


class CellModel3a(Cell):
    def calculate_growth_chance(self, neighbourhood: np.array, direction: int) -> float:
        if self.growth_stage > 0:
            return 0.0

        shroom_count = sum(1 for cell in neighbourhood.flat if cell.growth_stage > 0)

        def neighbour_in_direction_stage() -> int:
            match direction:
                case 0:
                    return neighbourhood[0, 1].growth_stage
                case 1:
                    return neighbourhood[0, 2].growth_stage
                case 2:
                    return neighbourhood[1, 2].growth_stage
                case 3:
                    return neighbourhood[2, 2].growth_stage
                case 4:
                    return neighbourhood[2, 1].growth_stage
                case 5:
                    return neighbourhood[2, 0].growth_stage
                case 6:
                    return neighbourhood[1, 0].growth_stage
                case 7:
                    return neighbourhood[0, 0].growth_stage
                case _:
                    raise ValueError(f"Invalid direction {direction}")

        if neighbour_in_direction_stage() < 1:
            return 0.0

        return self._calculate_growth_chance(shroom_count)

    def _calculate_growth_chance(self, neighbour_count):
        match neighbour_count:
            case 1:
                return 0.5
            case _:
                return 0.0


class CellModel3b(CellModel3a):
    def _calculate_growth_chance(self, neighbour_count):
        match neighbour_count:
            case 1:
                return 0.500
            case 2:
                return 0.250
            case 3:
                return 0.125
            case _:
                return 0.000
