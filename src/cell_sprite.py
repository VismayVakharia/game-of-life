from typing import Tuple, List

import pyglet

from .cell import Cell


class CellSprite(pyglet.shapes.BorderedRectangle):
    def __init__(
        self,
        x: float,
        y: float,
        size: int,
        batch: pyglet.graphics.Batch,
        cell: Cell,
        cell_color_map: List[Tuple[int]],
    ):
        self.cell = cell
        self.color_map = cell_color_map
        super().__init__(
            x=x,
            y=y,
            width=size,
            height=size,
            color=self.color_map[cell.state],
            batch=batch,
        )

    def update(self):
        self.color = self.color_map[self.cell.state]
