from typing import Optional, Type
from pydantic import BaseModel, validator
from vertex_protocol.utils.bytes32 import (
    bytes32_to_hex,
    hex_to_bytes32,
    subaccount_to_bytes32,
)


class SubaccountParams(BaseModel):
    subaccount_owner: Optional[str]
    subaccount_name: str


Subaccount = str | bytes | SubaccountParams


class BaseParams(BaseModel):
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


class SignatureParams(BaseModel):
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
    digests: list[str]


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


class PlaceOrderRequest(BaseModel):
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


class TxRequest(BaseModel):
    tx: dict
    spot_leverage: Optional[bool]
    digest: Optional[str]

    @validator("tx")
    def tx_has_nonce(cls, v: dict) -> dict:
        if v.get("nonce") is None:
            raise ValueError("Missing tx `nonce`")
        return v


def to_tx_request(cls: Type[BaseModel], v: BaseParamsSigned) -> TxRequest:
    if v.signature is None:
        raise ValueError("Missing `signature`")
    v.__dict__["sender"] = bytes32_to_hex(v.sender)
    v.__dict__["nonce"] = str(v.nonce)
    req = TxRequest(
        tx=v.dict(exclude="signature,digest,spot_leverage"), signature=v.signature
    )
    if v.dict().get("spot_leverage"):
        req.spot_leverage = v.dict().get("spot_leverage")
    if v.dict().get("digest"):
        req.digest = v.dict().get("digest")
    return req


class CancelOrdersRequest(BaseModel):
    cancel_orders: CancelOrdersParams

    _validator = validator("cancel_orders", allow_reuse=True)(to_tx_request)


class CancelProductOrdersRequest(BaseModel):
    cancel_product_orders: CancelProductOrdersParams

    _validator = validator("cancel_product_orders", allow_reuse=True)(to_tx_request)


class WithdrawCollateralRequest(BaseModel):
    withdraw_collateral: WithdrawCollateralParams

    _validator = validator("withdraw_collateral", allow_reuse=True)(to_tx_request)


class LiquidateSubaccountRequest(BaseModel):
    liquidate_subaccount: LiquidateSubaccountParams

    _validator = validator("liquidate_subaccount", allow_reuse=True)(to_tx_request)


class MintLpRequest(BaseModel):
    mint_lp: MintLpParams

    _validator = validator("mint_lp", allow_reuse=True)(to_tx_request)


class BurnLpRequest(BaseModel):
    burn_lp: BurnLpParams

    _validator = validator("burn_lp", allow_reuse=True)(to_tx_request)


class LinkSignerRequest(BaseModel):
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


class ExecuteResponse(BaseModel):
    status: str
    signature: Optional[str]
    error: Optional[str]
    req: Optional[dict]
