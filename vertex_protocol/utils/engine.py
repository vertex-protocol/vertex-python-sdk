from enum import Enum


class VertexExecute(str, Enum):
    PLACE_ORDER = "place_order"
    CANCEL_ORDERS = "cancel_orders"
    CANCEL_PRODUCT_ORDERS = "cancel_product_orders"
    WITHDRAW_COLLATERAL = "withdraw_collateral"
    LIQUIDATE_SUBACCOUNT = "liquidate_subaccount"
    MINT_LP = "mint_lp"
    BURN_LP = "burn_lp"
    LINK_SIGNER = "link_signer"
