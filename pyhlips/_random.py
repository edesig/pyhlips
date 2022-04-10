import random
from typing import Dict, List, Optional

from ._model import Layer, Layers

random.seed()


def shuffle_layer(layer: Layer, size: Optional[int] = None):
    instances = []
    for variant in layer.variants:
        instances += [variant] * variant.occurence
    if size != None:
        instances += [None] * (size - len(instances))
    random.shuffle(instances)
    return instances


def deal(layers: Layers, size: Optional[int] = None) -> List[Dict[str, List]]:
    n = len(layers.layers)
    size = (
        size
        if size
        else max(
            sum((variant.occurence for variant in layer.variants))
            for layer in layers.layers
        )
    )
    shuffled_layers = [shuffle_layer(layer, size) for layer in layers.layers]
    return [
        {
            layers.layers[layer].name: shuffled_layers[layer][item]
            for layer in range(n)
            if shuffled_layers[layer][item]
        }
        for item in range(size)
    ]
