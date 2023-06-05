from enum import StrEnum
from typing import Optional
from pydantic import validator
from vertex_protocol.utils.model import VertexBaseModel
from vertex_protocol.engine_client.types.models import (
    ApplyDeltaTx,
    BurnLpTx,
    EngineStatus,
    Liquidity,
    MaxOrderSizeDirection,
    MintLpTx,
    ResponseStatus,
    SpotProduct,
    SubaccountHealth,
    SpotProductBalance,
    PerpProduct,
    PerpProductBalance,
)


class EngineQueryType(StrEnum):
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


class QueryStatusParams(VertexBaseModel):
    type = EngineQueryType.STATUS.value


class QueryContractsParams(VertexBaseModel):
    type = EngineQueryType.CONTRACTS.value


class QueryNoncesParams(VertexBaseModel):
    type = EngineQueryType.NONCES.value
    address: str


class QueryOrderParams(VertexBaseModel):
    type = EngineQueryType.ORDER.value
    product_id: int
    digest: str


QuerySubaccountInfoTx = MintLpTx | BurnLpTx | ApplyDeltaTx


class QuerySubaccountInfoParams(VertexBaseModel):
    type = EngineQueryType.SUBACCOUNT_INFO.value
    subaccount: str
    txs: Optional[list[QuerySubaccountInfoTx]]


class QuerySubaccountOpenOrdersParams(VertexBaseModel):
    type = EngineQueryType.SUBACCOUNT_ORDERS.value
    product_id: int
    sender: str


class QueryMarketLiquidityParams(VertexBaseModel):
    type = EngineQueryType.MARKET_LIQUIDITY.value
    product_id: int
    depth: int


class QueryAllProductsParams(VertexBaseModel):
    type = EngineQueryType.ALL_PRODUCTS.value


class QueryMarketPriceParams(VertexBaseModel):
    type = EngineQueryType.MARKET_PRICE.value
    product_id: int


class QueryMaxOrderSizeParams(VertexBaseModel):
    type = EngineQueryType.MAX_ORDER_SIZE.value
    sender: str
    product_id: int
    price_x18: str
    direction: MaxOrderSizeDirection
    spot_leverage: Optional[bool]

    @validator("direction")
    def direction_to_str(cls, v: MaxOrderSizeDirection) -> str:
        return v.value


class QueryMaxWithdrawableParams(VertexBaseModel):
    type = EngineQueryType.MAX_WITHDRAWABLE.value
    sender: str
    product_id: int
    spot_leverage: Optional[bool]


class QueryMaxLpMintableParams(VertexBaseModel):
    type = EngineQueryType.MAX_LP_MINTABLE.value
    sender: str
    product_id: int
    spot_leverage: Optional[bool]


class QueryFeeRatesParams(VertexBaseModel):
    type = EngineQueryType.FEE_RATES.value
    sender: str


class QueryHealthGroupsParams(VertexBaseModel):
    type = EngineQueryType.HEALTH_GROUPS.value


class QueryLinkedSignerParams(VertexBaseModel):
    type = EngineQueryType.LINKED_SIGNER.value
    subaccount: str


QueryRequest = (
    QueryStatusParams
    | QueryContractsParams
    | QueryNoncesParams
    | QueryOrderParams
    | QuerySubaccountInfoParams
    | QuerySubaccountOpenOrdersParams
    | QueryMarketLiquidityParams
    | QueryAllProductsParams
    | QueryMarketPriceParams
    | QueryMaxOrderSizeParams
    | QueryMaxWithdrawableParams
    | QueryMaxLpMintableParams
    | QueryFeeRatesParams
    | QueryHealthGroupsParams
    | QueryLinkedSignerParams
)

StatusData = EngineStatus


class ContractsData(VertexBaseModel):
    chain_id: str
    endpoint_addr: str
    book_addrs: list[str]


class NoncesData(VertexBaseModel):
    tx_nonce: str
    order_nonce: str


class OrderData(VertexBaseModel):
    product_id: int
    sender: str
    price_x18: str
    amount: str
    expiration: str
    nonce: str
    unfilled_amount: str
    digest: str
    placed_at: str


class SubaccountInfoData(VertexBaseModel):
    subaccount: str
    exists: bool
    healths: list[SubaccountHealth]
    health_contributions: list[list[str]]
    spot_count: int
    perp_count: int
    spot_balances: list[SpotProductBalance]
    perp_balances: list[PerpProductBalance]
    spot_products: list[SpotProduct]
    perp_products: list[PerpProduct]


class SubaccountOpenOrdersData(VertexBaseModel):
    sender: str
    product_id: int
    orders: list[OrderData]


class MarketLiquidityData(VertexBaseModel):
    bids: list[Liquidity]
    asks: list[Liquidity]
    timestamp: str


class AllProductsData(VertexBaseModel):
    spot_products: list[SpotProduct]
    perp_products: list[PerpProduct]


class MarketPriceData(VertexBaseModel):
    product_id: int
    bid_x18: str
    ask_x18: str


class MaxOrderSizeData(VertexBaseModel):
    max_order_size: str


class MaxWithdrawableData(VertexBaseModel):
    max_withdrawable: str


class MaxLpMintableData(VertexBaseModel):
    max_base_amount: str


class FeeRatesData(VertexBaseModel):
    taker_fee_rates_x18: list[str]
    maker_fee_rates_x18: list[str]
    liquidation_sequencer_fee: str
    health_check_sequencer_fee: str
    taker_sequencer_fee: str
    withdraw_sequencer_fees: list[str]


class HealthGroupsData(VertexBaseModel):
    health_groups: list[list[int]]


class LinkedSignerData(VertexBaseModel):
    linked_signer: str


QueryResponseData = (
    StatusData
    | ContractsData
    | NoncesData
    | OrderData
    | SubaccountInfoData
    | SubaccountOpenOrdersData
    | MarketLiquidityData
    | AllProductsData
    | MarketPriceData
    | MaxOrderSizeData
    | MaxWithdrawableData
    | MaxLpMintableData
    | FeeRatesData
    | HealthGroupsData
    | LinkedSignerData
)


class QueryResponse(VertexBaseModel):
    status: ResponseStatus
    data: QueryResponseData | str
