#!/usr/bin/env python3
from itertools import product

import yaml
from src.simulation import Simulation


def load_pattern(name: str):
    with open("patterns.yaml", "r") as file:
        patterns = yaml.safe_load(file)
    return patterns[name]


def main():
    with open("config.yaml", "r") as f:
        configuration = yaml.safe_load(f)

    config = configuration["config"]

    pattern_name = configuration["pattern"]
    if pattern_name:
        pattern = load_pattern(pattern_name)
        size = pattern["size"]

        config["rows"], config["cols"] = size
        sim = Simulation(**config)

        points = list(map(lambda row: row.split(" "), pattern["points"]))
        for i, j in product(range(size[0]), range(size[1])):
            if points[i][j] == "1":
                sim.grid.grid[i][j].toggle()
    else:
        sim = Simulation(**config)

    sim.run()


if __name__ == "__main__":
    main()
