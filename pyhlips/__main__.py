from ._model import Layers, MetadataTemplate, Metadata
from ._random import deal
from ._creator import create_metadata


metadata_template_json = "examples/metadata_template.json"
layers_json = "examples/layers.json"
name = "Test"

if __name__ == "__main__":
    metadata_template = MetadataTemplate.parse_file(metadata_template_json)
    layers = Layers.parse_file(layers_json)
    shuffled = deal(layers)
    for i, item in enumerate(shuffled):
        create_metadata(metadata_template, item, name, i)
