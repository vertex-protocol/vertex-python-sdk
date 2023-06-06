from typing import Optional
from vertex_protocol.engine_client.types.models import (
    PerpProductBalance,
    SpotProductBalance,
)
from vertex_protocol.engine_client.types.query import SubaccountInfoData
from vertex_protocol.utils.model import VertexBaseModel


class SubaccountParams(VertexBaseModel):
    subaccount_owner: Optional[str]
    subaccount_name: str


Subaccount = str | bytes | SubaccountParams


def parse_subaccount_balance(
    subaccount_info: SubaccountInfoData, product_id: int
) -> SpotProductBalance | PerpProductBalance:
    """
    Parses the balance of a subaccount for a given product.

    Args:
        subaccount_info (SubaccountInfoData): The subaccount summary data.
        product_id (int): The ID of the product to lookup.

    Returns:
        Union[SpotProductBalance, PerpProductBalance]: The balance of the product in the subaccount.

    Raises:
        ValueError: If the product ID provided is not found.
    """
    for spot_balance in subaccount_info.spot_balances:
        if spot_balance.product_id == product_id:
            return spot_balance

    for perp_balance in subaccount_info.perp_balances:
        if perp_balance.product_id == product_id:
            return perp_balance

    raise ValueError(f"Invalid product id provided: {product_id}")
