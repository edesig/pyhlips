from pyhlips._model import *
import json

with open("examples/metadata_template.json") as f:
    tmpl_dict = json.load(f)
tmpl =  MetadataTemplate(**tmpl_dict)
print(Metadata.create_from_template(template=tmpl, name="1", file=File(uri='hehe')).json(indent=2))
