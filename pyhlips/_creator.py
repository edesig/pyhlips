from ._model import LayerVariant, MetadataTemplate, Metadata, Attribute, File
from typing import Dict


def create_metadata(
    template: MetadataTemplate,
    layers: Dict[str, LayerVariant],
    name,
    number,
    path="assets",
):
    attributes = [
        Attribute(trait_type=layer_name, value=layer.name)
        for layer_name, layer in layers.items()
    ]
    name = f"{name} #{number+1}"
    file_name = f"{number}.png"
    file = File(uri=file_name)
    metadata = Metadata.create_from_template(
        template, name=name, file=file, attributes=attributes
    )
    with open(f"{path}/{number}.json", "w") as f:
        f.write(metadata.json(indent=2))
