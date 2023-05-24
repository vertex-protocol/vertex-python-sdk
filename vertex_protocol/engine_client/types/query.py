from typing import Optional
from pydantic import BaseModel
from vertex_protocol.engine_client.types.models import (
    ApplyDeltaTx,
    BurnLpTx,
    Liquidity,
    MintLpTx,
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
)

StatusData = str


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
)


class QueryResponse(BaseModel):
    status: str
    data: QueryResponseData
