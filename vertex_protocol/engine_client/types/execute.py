from typing import Optional, Type
from pydantic import validator
from vertex_protocol.engine_client.types.models import EngineStatus, ResponseStatus
from vertex_protocol.utils.model import VertexBaseModel
from vertex_protocol.utils.bytes32 import (
    bytes32_to_hex,
    hex_to_bytes32,
    subaccount_to_bytes32,
)


class SubaccountParams(VertexBaseModel):
    subaccount_owner: Optional[str]
    subaccount_name: str


Subaccount = str | bytes | SubaccountParams

Digest = str | bytes


class BaseParams(VertexBaseModel):
    sender: Subaccount
    nonce: Optional[int]

    class Config:
        validate_assignment = True

    @validator("sender")
    def sender_to_bytes32(cls, v: Subaccount) -> bytes:
        if isinstance(v, str):
            return hex_to_bytes32(v)
        elif isinstance(v, SubaccountParams) and v.subaccount_owner is not None:
            return subaccount_to_bytes32(v.subaccount_owner, v.subaccount_name)
        else:
            return v


class SignatureParams(VertexBaseModel):
    signature: Optional[str]


class BaseParamsSigned(BaseParams, SignatureParams):
    pass


class OrderParams(BaseParams):
    priceX18: int
    amount: int
    expiration: int


class PlaceOrderParams(SignatureParams):
    product_id: int
    order: OrderParams
    digest: Optional[str]
    spot_leverage: Optional[bool]


class CancelOrdersParams(BaseParamsSigned):
    productIds: list[int]
    digests: list[Digest]

    @validator("digests")
    def digests_to_bytes32(cls, v: list[Digest]) -> list[bytes]:
        return [
            hex_to_bytes32(digest) if isinstance(digest, str) else digest
            for digest in v
        ]


class CancelProductOrdersParams(BaseParamsSigned):
    productIds: list[int]
    digest: Optional[str]


class WithdrawCollateralParams(BaseParamsSigned):
    productId: int
    amount: int
    spot_leverage: Optional[bool]


class LiquidateSubaccountParams(BaseParamsSigned):
    liquidatee: Subaccount
    mode: int
    healthGroup: int
    amount: int


class MintLpParams(BaseParamsSigned):
    productId: int
    amountBase: int
    quoteAmountLow: int
    quoteAmountHigh: int
    spot_leverage: Optional[bool]


class BurnLpParams(BaseParamsSigned):
    productId: int
    amount: int


class LinkSignerParams(BaseParamsSigned):
    signer: Subaccount


class PlaceOrderRequest(VertexBaseModel):
    place_order: PlaceOrderParams

    @validator("place_order")
    def validate(cls, v: PlaceOrderParams) -> PlaceOrderParams:
        if v.order.nonce is None:
            raise ValueError("Missing order `nonce`")
        if v.signature is None:
            raise ValueError("Missing `signature")
        v.order.__dict__["sender"] = bytes32_to_hex(v.order.sender)
        for field in ["nonce", "priceX18", "amount", "expiration"]:
            v.order.__dict__[field] = str(getattr(v.order, field))
        return v


class TxRequest(VertexBaseModel):
    tx: dict
    signature: str
    spot_leverage: Optional[bool]
    digest: Optional[str]

    @validator("tx")
    def validate(cls, v: dict) -> dict:
        if v.get("nonce") is None:
            raise ValueError("Missing tx `nonce`")
        v["sender"] = (
            bytes32_to_hex(v["sender"])
            if isinstance(v["sender"], bytes)
            else v["sender"]
        )
        v["nonce"] = str(v["nonce"])
        return v


def to_tx_request(cls: Type[VertexBaseModel], v: BaseParamsSigned) -> TxRequest:
    if v.signature is None:
        raise ValueError("Missing `signature`")
    return TxRequest(
        tx=v.dict(exclude={"signature", "digest", "spot_leverage"}),
        signature=v.signature,
        spot_leverage=v.dict().get("spot_leverage"),
        digest=v.dict().get("digest"),
    )


class CancelOrdersRequest(VertexBaseModel):
    cancel_orders: CancelOrdersParams

    @validator("cancel_orders")
    def digests_to_hex(cls, v: CancelOrdersParams) -> CancelOrdersParams:
        v.__dict__["digests"] = [
            bytes32_to_hex(digest) if isinstance(digest, bytes) else digest
            for digest in v.digests
        ]
        return v

    _validator = validator("cancel_orders", allow_reuse=True)(to_tx_request)


class CancelProductOrdersRequest(VertexBaseModel):
    cancel_product_orders: CancelProductOrdersParams

    _validator = validator("cancel_product_orders", allow_reuse=True)(to_tx_request)


class WithdrawCollateralRequest(VertexBaseModel):
    withdraw_collateral: WithdrawCollateralParams

    _validator = validator("withdraw_collateral", allow_reuse=True)(to_tx_request)


class LiquidateSubaccountRequest(VertexBaseModel):
    liquidate_subaccount: LiquidateSubaccountParams

    _validator = validator("liquidate_subaccount", allow_reuse=True)(to_tx_request)


class MintLpRequest(VertexBaseModel):
    mint_lp: MintLpParams

    _validator = validator("mint_lp", allow_reuse=True)(to_tx_request)


class BurnLpRequest(VertexBaseModel):
    burn_lp: BurnLpParams

    _validator = validator("burn_lp", allow_reuse=True)(to_tx_request)


class LinkSignerRequest(VertexBaseModel):
    link_signer: LinkSignerParams

    _validator = validator("link_signer", allow_reuse=True)(to_tx_request)


ExecuteRequest = (
    PlaceOrderRequest
    | CancelOrdersRequest
    | CancelProductOrdersRequest
    | WithdrawCollateralRequest
    | LiquidateSubaccountRequest
    | MintLpRequest
    | BurnLpRequest
    | LinkSignerRequest
)


class ExecuteResponse(VertexBaseModel):
    status: ResponseStatus
    signature: Optional[str]
    error: Optional[str]
    req: Optional[dict]
