import csv

from ._model import Recipe, RecipeItem


def export_recipe(recipe: Recipe, out: str = "recipe.csv"):
    layer_names = list(
        {layer.layer for item in recipe.items for layer in item.layers}
    )
    with open(out, "w") as f:
        writer = csv.writer(f, dialect="excel")
        writer.writerow(["id"] + layer_names + ["number of layers"])
        for item in recipe.items:
            layers = {layer.layer: layer.name for layer in item.layers}
            row = (
                [item.item_id]
                + [
                    layers[layer] if layer in layers else "-"
                    for layer in layer_names
                ]
                + [len(layers)]
            )
            writer.writerow(row)
