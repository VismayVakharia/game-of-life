from enum import IntEnum


class CellState(IntEnum):
    DEAD = 0
    ALIVE = 1


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._state: CellState = CellState.DEAD

    @property
    def state(self):
        return self._state

    def toggle(self):
        if self._state is CellState.ALIVE:
            self._state = CellState.DEAD
        else:
            self._state = CellState.ALIVE
