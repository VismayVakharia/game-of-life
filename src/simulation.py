from itertools import product
from typing import Tuple

import pyglet

from .cell_sprite import CellSprite
from .grid import Grid
from .ui import BaseWindow


class Simulation(BaseWindow):  # pylint: disable=too-many-ancestors, abstract-method
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

        ui_height = 30
        grid_width = width
        grid_height = height - ui_height

        cell_size = min(grid_width // cols, grid_height // rows)
        x_offset = (grid_width - cols * cell_size) // 2
        y_offset = (grid_height - rows * cell_size) // 2

        self.batch = pyglet.graphics.Batch()

        self.button_color = tuple(255 - (255 * i) for i in bg_color[:3])
        self.ui_sprites = {}
        play = self.batch.add(
            3,
            pyglet.gl.GL_TRIANGLES,
            None,
            (
                "v2f",
                (
                    x_offset + ui_height / 2,
                    height - ui_height * 0.2,
                    x_offset + ui_height / 2,
                    height - ui_height * 0.8,
                    x_offset + ui_height * 11 / 10,
                    height - ui_height * 0.5,
                ),
            ),
            ("c3B", self.bg_color[:3] * 3),
        )
        pause = [
            pyglet.shapes.Rectangle(
                x=x_offset + ui_height / 2,
                y=height - ui_height * 0.8,
                width=ui_height * 0.2,
                height=ui_height * 0.6,
                color=self.button_color,
                batch=self.batch,
            ),
            pyglet.shapes.Rectangle(
                x=x_offset + ui_height / 2 + ui_height * 0.4,
                y=height - ui_height * 0.8,
                width=ui_height * 0.2,
                height=ui_height * 0.6,
                color=self.button_color,
                batch=self.batch,
            ),
        ]
        step = [
            self.batch.add(
                3,
                pyglet.gl.GL_TRIANGLES,
                None,
                (
                    "v2f",
                    (
                        x_offset + ui_height * 3 / 2,
                        height - ui_height * 0.2,
                        x_offset + ui_height * 3 / 2,
                        height - ui_height * 0.8,
                        x_offset + ui_height * 20 / 10,
                        height - ui_height * 0.5,
                    ),
                ),
                ("c3B", self.bg_color[:3] * 3),
            ),
            pyglet.shapes.Line(
                x=x_offset + ui_height * 21 / 10,
                y=height - ui_height * 0.8,
                x2=x_offset + ui_height * 21 / 10,
                y2=height - ui_height * 0.2,
                width=ui_height * 0.1,
                color=self.bg_color[:3],
                batch=self.batch,
            ),
        ]
        text = pyglet.text.Label(
            text=f"Generations: {self.grid.generations }",
            x=width / 2,
            y=height - ui_height / 2,
            font_name="Ubuntu",
            font_size=12,
            anchor_x="center",
            anchor_y="center",
            color=self.button_color + (255,),
            batch=self.batch,
        )
        indicator = pyglet.shapes.Circle(
            x=width - x_offset - ui_height * 8 / 10,
            y=height - ui_height / 2,
            radius=ui_height * 0.3,
            color=(0, 0, 0),
            batch=self.batch,
        )
        self.ui_sprites["play"] = play
        self.ui_sprites["pause"] = pause
        self.ui_sprites["step"] = step
        self.ui_sprites["text"] = text
        self.ui_sprites["indicator"] = indicator

        cell_color_map = kwargs.get("cell_color_map", [(50, 50, 50), (200, 200, 50)])
        self.cell_sprites = []
        for i, j in product(range(rows), range(cols)):
            self.cell_sprites.append(
                CellSprite(
                    x_offset + j * cell_size,
                    height - y_offset - ui_height - (i + 1) * cell_size,
                    cell_size,
                    self.batch,
                    self.grid.grid[i][j],
                    cell_color_map,
                )
            )

        self.ui_height = ui_height
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.update(0)

    def actual_draw(self):
        self.batch.draw()

    def update(self, dt):
        self.actual_update(dt)
        if not self.paused:
            self.grid.update()

    def actual_update(self, dt):
        if self.paused:
            self.ui_sprites["play"].colors = self.button_color * 3
            for shape in self.ui_sprites["pause"]:
                shape.opacity = 0
            self.ui_sprites["step"][0].colors = self.button_color * 3
            self.ui_sprites["step"][1].color = self.button_color
            self.ui_sprites["indicator"].color = (255, 0, 0)
        else:
            self.ui_sprites["play"].colors = self.bg_color[:3] * 3
            for shape in self.ui_sprites["pause"]:
                shape.opacity = 255
            self.ui_sprites["step"][0].colors = self.bg_color[:3] * 3
            self.ui_sprites["step"][1].color = self.bg_color[:3]
            self.ui_sprites["indicator"].color = (0, 255, 0)

        self.ui_sprites["text"].text = f"Generations: {self.grid.generations}"

        for sprite in self.cell_sprites:
            sprite.update()

    def on_mouse_release(self, x, y, button, modifiers):
        if (
            self.x_offset < x < self.width - self.x_offset
            and self.y_offset < y < self.height - self.ui_height - self.y_offset
        ):
            j = (x - self.x_offset) // self.cell_size
            i = (self.height - y - self.y_offset - self.ui_height) // self.cell_size
            self.grid.grid[i][j].toggle()
        elif (
            self.ui_height / 2 < x - self.x_offset < self.ui_height * 11 / 10
            and self.ui_height * 0.2 < self.height - y < self.ui_height * 0.8
        ):
            self.paused = not self.paused
        elif (
            self.ui_height * 3 / 2 < x - self.x_offset < self.ui_height * 21 / 10
            and self.ui_height * 0.2 < self.height - y < self.ui_height * 0.8
        ):
            self.grid.update()

    def on_key_release(self, symbol, modifiers):
        super().on_key_release(symbol, modifiers)
        if self.paused and symbol == pyglet.window.key.N:
            self.grid.update()
        if symbol == pyglet.window.key.P:
            self.grid.print_pattern()
