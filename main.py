#!/usr/bin/env python3

import yaml

from src.simulation import Simulation


def load_pattern(name: str):
    with open("patterns.yaml", "r") as file:
        patterns = yaml.load(file)
    return patterns[name]


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        configuration = yaml.load(f)

    config = configuration["config"]

    pattern_name = configuration["pattern"]
    if pattern_name:
        pattern = load_pattern(pattern_name)
        config["rows"], config["cols"] = pattern["size"]

        sim = Simulation(**config)
        for i, j in pattern["points"]:
            sim.grid.grid[i][j].toggle()
    else:
        sim = Simulation(**config)

    sim.run()
