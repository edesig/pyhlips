import os
from typing import List, Optional

from ._image import merge
from ._model import (
    Attribute,
    File,
    Layers,
    Metadata,
    MetadataTemplate,
    Recipe,
    RecipeItem,
)
from ._random import deal, deal_with_layer_number_distribution


def create_recipe(
    metadata_template: MetadataTemplate,
    layers: Layers,
    distribution: Optional[List[int]] = None,
):
    if distribution:
        items = deal_with_layer_number_distribution(layers, distribution)
    else:
        items = deal(layers)
    return Recipe(
        metadata_template=metadata_template,
        items=[
            RecipeItem(item_id=i, layers=list(layers.values()))
            for i, layers in enumerate(items)
        ],
    )


def create_image(recipe: RecipeItem, out_dir: str = "assets"):
    out_file = os.path.join(out_dir, f"{recipe.item_id}.png")
    merge(
        [
            layer.path
            for layer in sorted(recipe.layers, key=lambda x: x.priority)
        ],
        out_file,
    )


def create_metadata(
    template: MetadataTemplate, recipe: RecipeItem, out_dir: str = "assets"
):
    attributes = [
        Attribute(trait_type=layer.layer, value=layer.name)
        for layer in recipe.layers
    ]
    name = f"{template.name} #{recipe.item_id+1}"
    file_name = f"{recipe.item_id}.png"
    file = File(uri=file_name)
    metadata = Metadata.create_from_template(
        template, name=name, file=file, attributes=attributes
    )
    with open(f"{out_dir}/{recipe.item_id}.json", "w") as f:
        f.write(metadata.json(indent=2))


def create_collection(recipe: Recipe, out_dir: str = "assets"):

    os.path.isdir(out_dir) or os.mkdir(out_dir)
    for item in recipe.items:
        create_metadata(recipe.metadata_template, item, out_dir)
        create_image(item, out_dir)
