from typing import Any
from pydantic import BaseModel, validator

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


QueryRequest = (
    QueryStatusParams | QueryContractsParams | QueryNoncesParams | QueryOrderParams
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


class QueryResponse(BaseModel):
    status: str
    data: StatusData | ContractsData | NoncesData | OrderData
