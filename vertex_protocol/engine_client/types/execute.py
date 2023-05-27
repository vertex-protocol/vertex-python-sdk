from typing import Optional, Type
from pydantic import validator
from vertex_protocol.engine_client.types.models import EngineStatus, ResponseStatus
from vertex_protocol.utils.engine import VertexExecute
from vertex_protocol.utils.model import VertexBaseModel
from vertex_protocol.utils.bytes32 import (
    bytes32_to_hex,
    hex_to_bytes32,
    subaccount_to_bytes32,
)
from vertex_protocol.utils.nonce import gen_order_nonce


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
    def serialize_sender(cls, v: Subaccount) -> bytes:
        return subaccount_to_bytes32(v)


class SignatureParams(VertexBaseModel):
    signature: Optional[str]


class BaseParamsSigned(BaseParams, SignatureParams):
    pass


class OrderParams(BaseParams):
    priceX18: int
    amount: int
    expiration: int
    nonce: int = gen_order_nonce()


class PlaceOrderParams(SignatureParams):
    product_id: int
    order: OrderParams
    digest: Optional[str]
    spot_leverage: Optional[bool]


class CancelOrdersParams(BaseParamsSigned):
    productIds: list[int]
    digests: list[Digest]
    nonce: int = gen_order_nonce()

    @validator("digests")
    def serialize_digests(cls, v: list[Digest]) -> list[bytes]:
        return [hex_to_bytes32(digest) for digest in v]


class CancelProductOrdersParams(BaseParamsSigned):
    productIds: list[int]
    digest: Optional[str]
    nonce: int = gen_order_nonce()


class WithdrawCollateralParams(BaseParamsSigned):
    productId: int
    amount: int
    spot_leverage: Optional[bool]


class LiquidateSubaccountParams(BaseParamsSigned):
    liquidatee: Subaccount
    mode: int
    healthGroup: int
    amount: int

    @validator("liquidatee")
    def serialize_liquidatee(cls, v: Subaccount) -> bytes:
        return subaccount_to_bytes32(v)


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

    @validator("signer")
    def serialize_signer(cls, v: Subaccount) -> bytes:
        return subaccount_to_bytes32(v)


ExecuteParams = (
    PlaceOrderParams
    | CancelOrdersParams
    | CancelProductOrdersParams
    | WithdrawCollateralParams
    | LiquidateSubaccountParams
    | MintLpParams
    | BurnLpParams
    | LinkSignerParams
)


class PlaceOrderRequest(VertexBaseModel):
    place_order: PlaceOrderParams

    @validator("place_order")
    def serialize(cls, v: PlaceOrderParams) -> PlaceOrderParams:
        if v.order.nonce is None:
            raise ValueError("Missing order `nonce`")
        if v.signature is None:
            raise ValueError("Missing `signature")
        if isinstance(v.order.sender, bytes):
            v.order.serialize_dict(["sender"], bytes32_to_hex)
        v.order.serialize_dict(["nonce", "priceX18", "amount", "expiration"], str)
        return v


class TxRequest(VertexBaseModel):
    tx: dict
    signature: str
    spot_leverage: Optional[bool]
    digest: Optional[str]

    @validator("tx")
    def serialize(cls, v: dict) -> dict:
        if v.get("nonce") is None:
            raise ValueError("Missing tx `nonce`")
        v["sender"] = bytes32_to_hex(v["sender"])
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
    def serialize(cls, v: CancelOrdersParams) -> CancelOrdersParams:
        v.serialize_dict(["digests"], lambda l: [bytes32_to_hex(x) for x in l])
        return v

    _validator = validator("cancel_orders", allow_reuse=True)(to_tx_request)


class CancelProductOrdersRequest(VertexBaseModel):
    cancel_product_orders: CancelProductOrdersParams

    _validator = validator("cancel_product_orders", allow_reuse=True)(to_tx_request)


class WithdrawCollateralRequest(VertexBaseModel):
    withdraw_collateral: WithdrawCollateralParams

    @validator("withdraw_collateral")
    def serialize(cls, v: WithdrawCollateralParams) -> WithdrawCollateralParams:
        v.serialize_dict(["amount"], str)
        return v

    _validator = validator("withdraw_collateral", allow_reuse=True)(to_tx_request)


class LiquidateSubaccountRequest(VertexBaseModel):
    liquidate_subaccount: LiquidateSubaccountParams

    @validator("liquidate_subaccount")
    def serialize(cls, v: LiquidateSubaccountParams) -> LiquidateSubaccountParams:
        v.serialize_dict(["amount"], str)
        v.serialize_dict(["liquidatee"], bytes32_to_hex)
        return v

    _validator = validator("liquidate_subaccount", allow_reuse=True)(to_tx_request)


class MintLpRequest(VertexBaseModel):
    mint_lp: MintLpParams

    @validator("mint_lp")
    def serialize(cls, v: MintLpParams) -> MintLpParams:
        v.serialize_dict(["amountBase", "quoteAmountLow", "quoteAmountHigh"], str)
        return v

    _validator = validator("mint_lp", allow_reuse=True)(to_tx_request)


class BurnLpRequest(VertexBaseModel):
    burn_lp: BurnLpParams

    @validator("burn_lp")
    def serialize(cls, v: BurnLpParams) -> BurnLpParams:
        v.serialize_dict(["amount"], str)
        return v

    _validator = validator("burn_lp", allow_reuse=True)(to_tx_request)


class LinkSignerRequest(VertexBaseModel):
    link_signer: LinkSignerParams

    @validator("link_signer")
    def serialize(cls, v: LinkSignerParams) -> LinkSignerParams:
        v.serialize_dict(["signer"], bytes32_to_hex)
        return v

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


def to_execute_request(params: ExecuteParams) -> ExecuteRequest:
    execute_request_mapping = {
        PlaceOrderParams: (PlaceOrderRequest, VertexExecute.PLACE_ORDER),
        CancelOrdersParams: (CancelOrdersRequest, VertexExecute.CANCEL_ORDERS),
        CancelProductOrdersParams: (
            CancelProductOrdersRequest,
            VertexExecute.CANCEL_PRODUCT_ORDERS,
        ),
        WithdrawCollateralParams: (
            WithdrawCollateralRequest,
            VertexExecute.WITHDRAW_COLLATERAL,
        ),
        LiquidateSubaccountParams: (
            LiquidateSubaccountRequest,
            VertexExecute.LIQUIDATE_SUBACCOUNT,
        ),
        MintLpParams: (MintLpRequest, VertexExecute.MINT_LP),
        BurnLpParams: (BurnLpRequest, VertexExecute.BURN_LP),
        LinkSignerParams: (LinkSignerRequest, VertexExecute.LINK_SIGNER),
    }

    RequestClass, field_name = execute_request_mapping[type(params)]
    return RequestClass(**{field_name: params})
