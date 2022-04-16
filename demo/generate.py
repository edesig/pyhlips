#!/usr/bin/env python
import logging
import os
import random
from typing import Tuple

import numpy as np
from PIL import Image

from pyhlips._collect import get_layers
from pyhlips._csv import export_recipe
from pyhlips._model import MetadataTemplate
from pyhlips._recipe import create_collection, create_recipe

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("PIL").setLevel(logging.WARNING)
DEMO_DIR = os.path.abspath(os.path.dirname(__file__))
METADATA_TEMPLATE = os.path.join(DEMO_DIR, "metadata_template.json")
WORK_DIR = os.path.join(DEMO_DIR, "work")
os.path.exists(WORK_DIR) or os.mkdir(WORK_DIR)


class LayerFactory:
    def __init__(self, size: Tuple[int, int]):
        self.size = size

    def create_rectangle(self, color, topleft, rightbottom, out):
        color = np.array(color + (255,), dtype="uint8")
        empty = np.array((0, 0, 0, 0), dtype="uint8")
        raw = np.array(
            [
                [
                    color
                    if i >= topleft[0]
                    and i < rightbottom[0]
                    and j >= topleft[1]
                    and j < rightbottom[1]
                    else empty
                    for j in range(self.size[1])
                ]
                for i in range(self.size[0])
            ]
        )
        image = Image.fromarray(raw, "RGBA")
        image.save(out)


def generate_layers():
    os.chdir(WORK_DIR)
    os.path.exists("Layers") or os.mkdir("Layers")
    os.chdir("Layers")
    factory = LayerFactory((200, 200))
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "magenta": (255, 0, 255),
        "cyan": (0, 255, 255),
    }
    layers = {
        "L1 1": ((10, 10), (100, 100), 20),
        "R1 2": ((10, 100), (100, 190), 20),
        "L2 3": ((100, 10), (190, 100), 20),
        "R2 4": ((100, 100), (190, 190), 20),
        "Middle 5": ((40, 60), (150, 130), 10),
    }
    os.path.exists("Background 0") or os.mkdir("Background 0")
    factory.create_rectangle(
        (72, 72, 72),
        (0, 0),
        (200, 200),
        os.path.join("Background 0", "gray 24.png"),
    )
    for layer, coords in layers.items():
        os.path.exists(layer) or os.mkdir(layer)
        occurence = coords[2]  # occurence of layer
        remaining = occurence - len(colors)
        for name, color in colors.items():
            amount = random.randint(0, remaining)
            remaining -= (
                amount  # TODO: it may happen, that we don't use all occurence
            )
            factory.create_rectangle(
                color,
                coords[0],
                coords[1],
                os.path.join(layer, f"{name} {amount + 1}.png"),
            )


def collect_layers():
    os.chdir(WORK_DIR)
    with open("layers.json", "w") as layers_json:
        layers = get_layers("Layers")
        layers_json.write(layers.json(indent=2))
    return layers


def prepare_recipe(layers):
    os.chdir(WORK_DIR)
    recipe = create_recipe(
        MetadataTemplate.parse_file(METADATA_TEMPLATE),
        layers,
        [0, 0, 3, 5, 11, 5],
    )
    with open("recipe.json", "w") as recipe_json:
        recipe_json.write(recipe.json(indent=2))
    return recipe


if __name__ == "__main__":
    generate_layers()
    layers = collect_layers()
    recipe = prepare_recipe(layers)
    create_collection(recipe)
    export_recipe(recipe)
