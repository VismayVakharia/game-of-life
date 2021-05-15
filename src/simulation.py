from itertools import product
from typing import Tuple

import pyglet

from .cell_sprite import CellSprite
from .grid import Grid
from .ui import BaseWindow


class Simulation(BaseWindow):
    def __init__(
        self,
        width: int,
        height: int,
        rows: int,
        cols: int,
        frame_rate: int,
        bg_color: Tuple[float, float, float, float],
        recording_abspath: str = "",
        **kwargs,
    ):
        super().__init__(
            width=width,
            height=height,
            frame_rate=frame_rate,
            bg_color=bg_color,
            recording_abspath=recording_abspath,
        )

        self.grid = Grid(rows, cols)

        self.cell_size = min(width // cols, height // rows)
        self.x_offset = (width - cols * self.cell_size) // 2
        self.y_offset = (height - rows * self.cell_size) // 2

        self.batch = pyglet.graphics.Batch()

        cell_color_map = kwargs.get("cell_color_map", [(50, 50, 50), (200, 200, 50)])
        self.cell_sprites = []
        for i, j in product(range(rows), range(cols)):
            self.cell_sprites.append(
                CellSprite(
                    self.x_offset + j * self.cell_size,
                    height - self.y_offset - (i + 1) * self.cell_size,
                    self.cell_size,
                    self.batch,
                    self.grid.grid[i][j],
                    cell_color_map,
                )
            )

        pause_color = tuple(255 - (255 * i) for i in bg_color[:3])
        self.pause_sprites = [
            pyglet.shapes.Rectangle(
                x=width - 100,
                y=height - 100,
                width=30,
                height=90,
                color=pause_color,
                batch=self.batch,
            ),
            pyglet.shapes.Rectangle(
                x=width - 40,
                y=height - 100,
                width=30,
                height=90,
                color=pause_color,
                batch=self.batch,
            ),
        ]

    def actual_draw(self):
        self.batch.draw()

    def update(self, dt):
        self.actual_update(dt)
        if not self.is_paused:
            self.grid.update()

    def actual_update(self, dt):
        for sprite in self.pause_sprites:
            sprite.opacity = self.is_paused * 255

        for sprite in self.cell_sprites:
            sprite.update()

    def on_mouse_release(self, x, y, button, modifiers):
        j = (x - self.x_offset) // self.cell_size
        i = (self.height - y - self.y_offset) // self.cell_size
        self.grid.grid[i][j].toggle()
