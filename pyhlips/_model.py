import os
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class LayerVariant(BaseModel):
    name: str
    path: str
    occurence: int
    priority: int


class Layer(BaseModel):
    id: int
    name: str
    variants: List[LayerVariant]


class Layers(BaseModel):
    layers: List[Layer]


class Attribute(BaseModel):
    trait_type: str
    value: str


class Creator(BaseModel):
    address: str
    share: Decimal


class File(BaseModel):
    uri: str
    type: str = "image/png"


class Collection(BaseModel):
    name: str
    family: str


class Properties(BaseModel):
    creators: List[Creator]
    files: List[File] = []


class MetadataTemplate(BaseModel):
    symbol: str = ""
    description: str = ""
    seller_fee_basis_points: int
    attributes: List[Attribute] = []
    properties: Properties
    collection: Collection


class Metadata(BaseModel):
    name: str
    symbol: str
    description: str
    seller_fee_basis_points: int
    image: str
    attributes: List[Attribute]
    properties: Properties
    collection: Collection

    @staticmethod
    def create_from_template(
        template: MetadataTemplate,
        name: str,
        file: File,
        attributes: Optional[List[Attribute]] = [],
        description: Optional[str] = None,
        properties: Optional[Properties] = None,
        seller_fee_basis_points: Optional[int] = None,
        symbol: Optional[str] = None,
    ):
        if not properties:
            properties = template.properties
        if not template.attributes:
            template.attributes = []
        attributes = template.attributes + attributes
        properties.files = [file]
        return Metadata(
            name=name,
            symbol=symbol if symbol else template.symbol,
            description=description if description else template.description,
            seller_fee_basis_points=seller_fee_basis_points
            if seller_fee_basis_points
            else template.seller_fee_basis_points,
            image=file.uri,
            attributes=attributes,
            properties=properties,
            collection=template.collection,
        )
