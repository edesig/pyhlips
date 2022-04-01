import random
from typing import Optional
from ._model import Layers, Layer

random.seed()


def shuffle_layer(layer: Layer, size: int):
    instances = []
    for variant in layer.variants:
        instances += [variant] * variant.occurence
    instances += [None] * (size - len(instances))
    random.shuffle(instances)
    return instances


def shuffle_layers(layers: Layers, size: Optional[int] = None):
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
        for item in range(len(shuffled_layers[0]))
    ]
