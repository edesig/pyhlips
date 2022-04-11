import json

from pyhlips._model import *


def test_metadata_template():
    with open("examples/metadata_template.json") as f:
        tmpl_dict = json.load(f)
    tmpl = MetadataTemplate(**tmpl_dict)
    expected = '{"name": "Sample collection", "symbol": "A symbol", "description": "Some description", "seller_fee_basis_points": 1000, "attributes": [], "properties": {"creators": [{"address": "Bpspdoapsdoapsoidpiaospdiapsoidpsaoidposiapd", "share": 25}, {"address": "Cpspdoapsdoapsoidpiaospdiapsoidpsaoidposiapd", "share": 25}, {"address": "Dpspdoapsdoapsoidpiaospdiapsoidpsaoidposiapd", "share": 25}, {"address": "Fpspdoapsdoapsoidpiaospdiapsoidpsaoidposiapd", "share": 25}], "files": []}, "collection": {"name": "SMArt Commemoratives", "family": "SMArt Commemoratives Family"}}'
    assert tmpl.json() == expected
    expected = '{"name": "1", "symbol": "A symbol", "description": "Some description", "seller_fee_basis_points": 1000, "image": "hehe", "attributes": [], "properties": {"creators": [{"address": "Bpspdoapsdoapsoidpiaospdiapsoidpsaoidposiapd", "share": 25}, {"address": "Cpspdoapsdoapsoidpiaospdiapsoidpsaoidposiapd", "share": 25}, {"address": "Dpspdoapsdoapsoidpiaospdiapsoidpsaoidposiapd", "share": 25}, {"address": "Fpspdoapsdoapsoidpiaospdiapsoidpsaoidposiapd", "share": 25}], "files": [{"uri": "hehe", "type": "image/png"}]}, "collection": {"name": "SMArt Commemoratives", "family": "SMArt Commemoratives Family"}}'
    metadata_json = Metadata.create_from_template(
        template=tmpl, name="1", file=File(uri="hehe")
    ).json()
    assert metadata_json == expected
