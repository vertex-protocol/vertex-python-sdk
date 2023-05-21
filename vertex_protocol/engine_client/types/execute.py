import binascii
from typing import Optional
from pydantic import BaseModel, validator
from vertex_protocol.utils.bytes32 import hex_to_bytes32


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
        elif isinstance(v, bytes):
            return v
        elif isinstance(v, Subaccount) and v.subaccount_owner is not None:
            return hex_to_bytes32(
                f"{v.subaccount_owner}{binascii.hexlify(v.subaccount_name.encode()).decode()}"
            )
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


class CancelOrdersParams(BaseParamsSigned):
    productIds: list[int]
    digests: list[str]


class CancelProductOrdersParams(BaseParamsSigned):
    productIds: list[int]
    digest: Optional[str]


class WithdrawCollateralParams(BaseParamsSigned):
    productId: int
    amount: int


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


class BurnLpParams(BaseParamsSigned):
    productId: int
    amount: int


class LinkSignerParams(BaseParamsSigned):
    signer: Subaccount
