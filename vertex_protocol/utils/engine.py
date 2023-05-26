from enum import Enum

from vertex_protocol.engine_client.types.execute import ExecuteParams, ExecuteRequest


class VertexExecute(str, Enum):
    PLACE_ORDER = "place_order"
    CANCEL_ORDERS = "cancel_orders"
    CANCEL_PRODUCT_ORDERS = "cancel_product_orders"
    WITHDRAW_COLLATERAL = "withdraw_collateral"
    LIQUIDATE_SUBACCOUNT = "liquidate_subaccount"
    MINT_LP = "mint_lp"
    BURN_LP = "burn_lp"
    LINK_SIGNER = "link_signer"


class VertexQuery(str, Enum):
    STATUS = "status"
    CONTRACTS = "contracts"
    NONCES = "nonces"
    ORDER = "order"
    ALL_PRODUCTS = "all_products"
    FEE_RATES = "fee_rates"
    HEALTH_GROUPS = "health_groups"
    LINKED_SIGNER = "linked_signer"
    MARKET_LIQUIDITY = "market_liquidity"
    MARKET_PRICE = "market_price"
    MAX_ORDER_SIZE = "max_order_size"
    MAX_WITHDRAWABLE = "max_withdrawable"
    MAX_LP_MINTABLE = "max_lp_mintable"
    SUBACCOUNT_INFO = "subaccount_info"
    SUBACCOUNT_ORDERS = "subaccount_orders"
