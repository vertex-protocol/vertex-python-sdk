from typing import Optional
from pydantic import BaseModel, validator
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


class QueryStatusParams(BaseModel):
    type = VertexQuery.STATUS.value


class QueryContractsParams(BaseModel):
    type = VertexQuery.CONTRACTS.value


class QueryNoncesParams(BaseModel):
    type = VertexQuery.NONCES.value
    address: str


class QueryOrderParams(BaseModel):
    type = VertexQuery.ORDER.value
    product_id: int
    digest: str


QuerySubaccountInfoTx = MintLpTx | BurnLpTx | ApplyDeltaTx


class QuerySubaccountInfoParams(BaseModel):
    type = VertexQuery.SUBACCOUNT_INFO.value
    subaccount: str
    txs: Optional[list[QuerySubaccountInfoTx]]


class QuerySubaccountOpenOrdersParams(BaseModel):
    type = VertexQuery.SUBACCOUNT_ORDERS.value
    product_id: int
    sender: str


class QueryMarketLiquidityParams(BaseModel):
    type = VertexQuery.MARKET_LIQUIDITY.value
    product_id: int
    depth: int


class QueryAllProductsParams(BaseModel):
    type = VertexQuery.ALL_PRODUCTS.value


class QueryMarketPriceParams(BaseModel):
    type = VertexQuery.MARKET_PRICE.value
    product_id: int


class QueryMaxOrderSizeParams(BaseModel):
    type = VertexQuery.MAX_ORDER_SIZE.value
    sender: str
    product_id: int
    price_x18: str
    direction: MaxOrderSizeDirection
    spot_leverage: Optional[bool]

    @validator("direction")
    def direction_to_str(cls, v: MaxOrderSizeDirection) -> str:
        return v.value


class QueryMaxWithdrawableParams(BaseModel):
    type = VertexQuery.MAX_WITHDRAWABLE.value
    sender: str
    product_id: int
    spot_leverage: Optional[bool]


class QueryMaxLpMintableParams(BaseModel):
    type = VertexQuery.MAX_LP_MINTABLE.value
    sender: str
    product_id: int
    spot_leverage: Optional[bool]


class QueryFeeRatesParams(BaseModel):
    type = VertexQuery.FEE_RATES.value
    sender: str


class QueryHealthGroupsParams(BaseModel):
    type = VertexQuery.HEALTH_GROUPS.value


class QueryLinkedSignerParams(BaseModel):
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


class ContractsData(BaseModel):
    chain_id: str
    endpoint_addr: str
    book_addrs: list[str]


class NoncesData(BaseModel):
    tx_nonce: str
    order_nonce: str


class OrderData(BaseModel):
    product_id: int
    sender: str
    price_x18: str
    amount: str
    expiration: str
    nonce: str
    unfilled_amount: str
    digest: str
    placed_at: str


class SubaccountInfoData(BaseModel):
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


class SubaccountOpenOrdersData(BaseModel):
    sender: str
    product_id: int
    orders: list[OrderData]


class MarketLiquidityData(BaseModel):
    bids: list[Liquidity]
    asks: list[Liquidity]
    timestamp: str


class AllProductsData(BaseModel):
    spot_products: list[SpotProduct]
    perp_products: list[PerpProduct]


class MarketPriceData(BaseModel):
    product_id: int
    bid_x18: str
    ask_x18: str


class MaxOrderSizeData(BaseModel):
    max_order_size: str


class MaxWithdrawableData(BaseModel):
    max_withdrawable: str


class MaxLpMintableData(BaseModel):
    max_base_amount: str


class FeeRatesData(BaseModel):
    taker_fee_rates_x18: list[str]
    maker_fee_rates_x18: list[str]
    liquidation_sequencer_fee: str
    health_check_sequencer_fee: str
    taker_sequencer_fee: str
    withdraw_sequencer_fees: list[str]


class HealthGroupsData(BaseModel):
    health_groups: list[list[int]]


class LinkedSignerData(BaseModel):
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


class QueryResponse(BaseModel):
    status: ResponseStatus
    data: QueryResponseData | str
