from typing import List, Optional

from ._model import Layers, MetadataTemplate, Recipe, RecipeItem
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
        layers=[RecipeItem(item_id=i, layers=layers) for i, layers in enumerate(items)],
    )
