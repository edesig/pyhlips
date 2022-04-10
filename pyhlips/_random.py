import random
from typing import Dict, List, Optional

from ._model import Layer, Layers, LayerVariant
from ._counted_labels import create_labeling

random.seed()


def _layer_size(layer: Layer):
    return sum((variant.occurence for variant in layer.variants))


def shuffle_layer(layer: Layer, size: Optional[int] = None):
    instances = []
    for variant in layer.variants:
        instances += [variant] * variant.occurence
    if size != None:
        instances += [None] * (size - len(instances))
    random.shuffle(instances)
    return instances


def deal(
    layers: Layers, size: Optional[int] = None
) -> List[Dict[str, List[LayerVariant]]]:
    n = len(layers.layers)
    size = size if size else max(_layer_size(layer) for layer in layers.layers)
    shuffled_layers = [shuffle_layer(layer, size) for layer in layers.layers]
    return [
        {
            layers.layers[layer].name: shuffled_layers[layer][item]
            for layer in range(n)
            if shuffled_layers[layer][item]
        }
        for item in range(size)
    ]


def deal_with_layer_number_distribution(
    layers: Layers, distribution: List[int]
):
    size = sum(distribution)
    optional_layers = {
        layer.name: _layer_size(layer)
        for layer in layers
        if _layer_size(layer) < size
    }
    mandatory_layers = [
        layer.name for layer in layers if _layer_size(layer) >= size
    ]
    prelabeled = create_labeling(optional_layers, distribution[1:])
    labeled = [item + mandatory_layers for item in prelabeled]
    shuffled_layers = {layer.name: shuffle_layer(layer) for layer in layers}
    return [
        {layer: shuffled_layers[layer].pop() for layer in item}
        for item in labeled
    ]
