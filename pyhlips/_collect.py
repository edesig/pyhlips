import json
import os
import re

from ._model import Layer, Layers, LayerVariant

p_layervariant = re.compile(r"(?P<name>.*) \(?(?P<occurence>\d+)\)?\.png")
p_layer = re.compile(r"(?P<name>.*) (?P<priority>\d+)")


def get_layer(path: str):
    print(path)
    path = path.rstrip(os.path.sep)
    print(os.path.basename(path))
    layer_name, priority = p_layer.match(os.path.basename(path)).groups()
    variants = []
    for variant in os.listdir(path):
        image_path = os.path.join(path, variant)
        if os.path.isfile:
            m = p_layervariant.match(variant)
            if not m:
                raise ValueError(f"{variant} isn't meeting with our expectations")
            variants.append(
                LayerVariant(
                    name=m["name"],
                    path=image_path,
                    occurence=m["occurence"],
                    priority=priority,
                )
            )
    return Layer(id=priority, name=layer_name, variants=variants)


def get_layers(path):
    layers = [get_layer(os.path.join(path, item)) for item in os.listdir(path)]
    layers.sort(key=lambda x: x.id)
    return Layers(layers=layers)
