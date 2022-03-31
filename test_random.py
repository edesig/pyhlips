from pyhlips._model import Layer, Layers, LayerVariant
from pyhlips._random import shuffle_layers
import json

layers = Layers(
    layers=[
        Layer(
            id=i,
            variants=[
                LayerVariant(name=f"{i}{j}", path=f"{i}{j}.png", occurence=3)
                for j in "ab"
            ],
        ) for i in range(2)
    ]
)

with open("examples/layers.json") as f:
    layers = Layers.parse_raw(f.read())
print(shuffle_layers(layers))
