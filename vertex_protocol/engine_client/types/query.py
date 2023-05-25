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

from vertex_protocol.utils.engine import VertexQuery


class QueryStatusParams(VertexBaseModel):
    type = VertexQuery.STATUS.value


class QueryContractsParams(VertexBaseModel):
    type = VertexQuery.CONTRACTS.value


class QueryNoncesParams(VertexBaseModel):
    type = VertexQuery.NONCES.value
    address: str


class QueryOrderParams(VertexBaseModel):
    type = VertexQuery.ORDER.value
    product_id: int
    digest: str


QuerySubaccountInfoTx = MintLpTx | BurnLpTx | ApplyDeltaTx


class QuerySubaccountInfoParams(VertexBaseModel):
    type = VertexQuery.SUBACCOUNT_INFO.value
    subaccount: str
    txs: Optional[list[QuerySubaccountInfoTx]]


class QuerySubaccountOpenOrdersParams(VertexBaseModel):
    type = VertexQuery.SUBACCOUNT_ORDERS.value
    product_id: int
    sender: str


class QueryMarketLiquidityParams(VertexBaseModel):
    type = VertexQuery.MARKET_LIQUIDITY.value
    product_id: int
    depth: int


class QueryAllProductsParams(VertexBaseModel):
    type = VertexQuery.ALL_PRODUCTS.value


class QueryMarketPriceParams(VertexBaseModel):
    type = VertexQuery.MARKET_PRICE.value
    product_id: int


class QueryMaxOrderSizeParams(VertexBaseModel):
    type = VertexQuery.MAX_ORDER_SIZE.value
    sender: str
    product_id: int
    price_x18: str
    direction: MaxOrderSizeDirection
    spot_leverage: Optional[bool]

    @validator("direction")
    def direction_to_str(cls, v: MaxOrderSizeDirection) -> str:
        return v.value


class QueryMaxWithdrawableParams(VertexBaseModel):
    type = VertexQuery.MAX_WITHDRAWABLE.value
    sender: str
    product_id: int
    spot_leverage: Optional[bool]


class QueryMaxLpMintableParams(VertexBaseModel):
    type = VertexQuery.MAX_LP_MINTABLE.value
    sender: str
    product_id: int
    spot_leverage: Optional[bool]


class QueryFeeRatesParams(VertexBaseModel):
    type = VertexQuery.FEE_RATES.value
    sender: str


class QueryHealthGroupsParams(VertexBaseModel):
    type = VertexQuery.HEALTH_GROUPS.value


class QueryLinkedSignerParams(VertexBaseModel):
    type = VertexQuery.LINKED_SIGNER.value
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
