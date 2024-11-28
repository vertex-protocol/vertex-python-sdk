from typing import Optional, Union
from vertex_protocol.utils.model import VertexBaseModel


class PriceAboveTrigger(VertexBaseModel):
    price_above: str


class PriceBelowTrigger(VertexBaseModel):
    price_below: str


class LastPriceAboveTrigger(VertexBaseModel):
    last_price_above: str


class LastPriceBelowTrigger(VertexBaseModel):
    last_price_below: str


TriggerCriteria = Union[
    PriceAboveTrigger, PriceBelowTrigger, LastPriceAboveTrigger, LastPriceBelowTrigger
]


class OrderData(VertexBaseModel):
    sender: str
    priceX18: str
    amount: str
    expiration: str
    nonce: str


class TriggerOrderData(VertexBaseModel):
    """
    Data model for details of a trigger order.
    """

    product_id: int
    order: OrderData
    signature: str
    spot_leverage: Optional[bool]
    digest: Optional[str]
    trigger: TriggerCriteria
