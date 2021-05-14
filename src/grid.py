from itertools import product
from typing import List, Tuple

from .cell import Cell, CellState


class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        self.grid: List[List[Cell]] = []
        for i in range(rows):
            self.grid.append([])
            for j in range(cols):
                self.grid[i].append(Cell(i, j))

    @staticmethod
    def get_neighbours(
        x: int, y: int, x_limits: Tuple[int, int], y_limits: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        neighbours = []
        for i, j in product([-1, 0, 1], repeat=2):
            if not (i == j == 0):
                neighbour = (x + i, y + j)
                if (
                    x_limits[0] <= neighbour[0] <= x_limits[1]
                    and y_limits[0] <= neighbour[1] <= y_limits[1]
                ):
                    neighbours.append(neighbour)
        return neighbours

    def update(self):
        changes = []
        for i, j in product(range(self.rows), range(self.cols)):
            neighbours = self.get_neighbours(
                i, j, (0, self.rows - 1), (0, self.cols - 1)
            )
            count = 0
            for neighbour in neighbours:
                count += self.grid[neighbour[0]][neighbour[1]].state
            cell = self.grid[i][j]
            if cell.state is CellState.ALIVE:
                if not (2 <= count <= 3):
                    changes.append(cell)
            else:
                if count == 3:
                    changes.append(cell)

        for cell in changes:
            cell.toggle()

    def print_grid_plain(self):
        unicode_map = {CellState.DEAD: " ", CellState.ALIVE: "\u25cf"}
        for row in self.grid:
            string = ("{} " * self.cols).format(
                *map(lambda cell: unicode_map[cell.state], row)
            )
            print(string)

    def print_grid_small(self):
        unicode_map = {CellState.DEAD: " ", CellState.ALIVE: "o"}
        print("-" * (4 * self.cols + 1))
        for row in self.grid:
            string = ("|" + " {} |" * self.cols).format(
                *map(lambda cell: unicode_map[cell.state], row)
            )
            print(string)
            print("-" * (4 * self.cols + 1))

    def print_grid_big(self):
        unicode_map = {CellState.DEAD: " ", CellState.ALIVE: "\u25cf"}
        print("_" * (6 * self.cols))
        for row in self.grid:
            print("|" + "     |" * self.cols)
            string = ("|" + "  {}  |" * self.cols).format(
                *map(lambda cell: unicode_map[cell.state], row)
            )
            print(string)
            print("|" + "_____|" * self.cols)
