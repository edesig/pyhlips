import random
from ._model import Layers, Layer

random.seed()

def shuffle_layer(layer: Layer):
    instances = []
    for variant in layer.variants:
        instances += [variant] * variant.occurence
    random.shuffle(instances)
    return instances


def shuffle_layers(layers: Layers):
    n = len(layers.layers)
    shuffled_layers = [shuffle_layer(layer) for layer in layers.layers]
    return [
        {
            f"Layer-{layers.layers[layer].id}": shuffled_layers[layer][item]
            for layer in range(n)
        }
        for item in range(len(shuffled_layers[0]))
    ]
