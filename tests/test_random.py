from pyhlips._model import Layer, Layers, LayerVariant
from pyhlips._random import deal
import json


def test_deal():
    with open("examples/layers.json") as f:
        layers = Layers.parse_raw(f.read())

    shuffled = deal(layers)
    assert all((len(item) == 2 for item in shuffled))
    assert all(("background" in item for item in shuffled))
