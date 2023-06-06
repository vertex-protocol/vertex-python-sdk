from enum import StrEnum
from typing import Optional, Type
from pydantic import validator
from vertex_protocol.contracts.types import VertexExecuteType
from vertex_protocol.engine_client.types.models import ResponseStatus
from vertex_protocol.utils.model import VertexBaseModel
from vertex_protocol.utils.bytes32 import (
    bytes32_to_hex,
    hex_to_bytes32,
    subaccount_to_bytes32,
)
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import Subaccount, SubaccountParams


Digest = str | bytes


class BaseParams(VertexBaseModel):
    """
    Base class for defining request parameters to be sent to the Vertex API.

    Attributes:
        sender (Subaccount): The sender's subaccount identifier.
        nonce (Optional[int]): An optional nonce for the request.

    Note:
        - The sender attribute is validated and serialized to bytes32 format before sending the request.
    """

    sender: Subaccount
    nonce: Optional[int]

    class Config:
        validate_assignment = True

    @validator("sender")
    def serialize_sender(cls, v: Subaccount) -> bytes:
        """
        Validates and serializes the sender to bytes32 format.

        Args:
            v (Subaccount): The sender's subaccount identifier.

        Returns:
            bytes: The serialized sender in bytes32 format.
        """
        return subaccount_to_bytes32(v)


class SignatureParams(VertexBaseModel):
    """
    Class for defining signature parameters in a request sent to the Vertex API.

    Attributes:
        signature (Optional[str]): An optional string representing the signature for the request.
    """

    signature: Optional[str]


class BaseParamsSigned(BaseParams, SignatureParams):
    """
    Class that combines the base parameters and signature parameters for a signed request
    to the Vertex API. Inherits attributes from BaseParams and SignatureParams.
    """

    pass


class OrderParams(BaseParams):
    """
    Class for defining the parameters of an order.

    Attributes:
        priceX18 (int): The price of the order with a precision of 18 decimal places.
        amount (int): The amount of the asset to be bought or sold in the order.
        expiration (int): The unix timestamp at which the order will expire.
        nonce (int): A unique number used to prevent replay attacks. By default, a new nonce is generated.
            see `gen_order_nonce` for more info.
    """

    priceX18: int
    amount: int
    expiration: int
    nonce: int = gen_order_nonce()


class PlaceOrderParams(SignatureParams):
    """
    Class for defining the parameters needed to place an order.

    Attributes:
        product_id (int): The id of the product for which the order is being placed.
        order (OrderParams): The parameters of the order.
        digest (Optional[str]): An optional hash of the order data.
        spot_leverage (Optional[bool]): An optional flag indicating whether leverage should be used for the order. By default, leverage is assumed.
    """

    product_id: int
    order: OrderParams
    digest: Optional[str]
    spot_leverage: Optional[bool]


class CancelOrdersParams(BaseParamsSigned):
    """
    Parameters to cancel specific orders.

    Args:
        productIds (list[int]): List of product IDs for the orders to be canceled.
        digests (list[Digest]): List of digests of the orders to be canceled.
        nonce (int): A unique number used to prevent replay attacks. By default, a new nonce is generated.
            see `gen_order_nonce` for more info.

    Methods:
        serialize_digests: Validates and converts a list of hex digests to bytes32.
    """

    productIds: list[int]
    digests: list[Digest]
    nonce: int = gen_order_nonce()

    @validator("digests")
    def serialize_digests(cls, v: list[Digest]) -> list[bytes]:
        return [hex_to_bytes32(digest) for digest in v]


class CancelProductOrdersParams(BaseParamsSigned):
    """
    Parameters to cancel all orders for specific products.

    Args:
        productIds (list[int]): List of product IDs for the orders to be canceled.
        digest (str, optional): Optional EIP-712 digest of the CancelProductOrder request.
        nonce (int): A unique number used to prevent replay attacks. By default, a new nonce is generated.
            see `gen_order_nonce` for more info.
    """

    productIds: list[int]
    digest: Optional[str]
    nonce: int = gen_order_nonce()


class WithdrawCollateralParams(BaseParamsSigned):
    """
    Parameters required to withdraw collateral from a specific product.

    Attributes:
        productId (int): The ID of the product to withdraw collateral from.
        amount (int): The amount of collateral to be withdrawn.
        spot_leverage (Optional[bool]): Indicates whether leverage is to be used. Defaults to True.
            If set to False, the transaction fails if it causes a borrow on the subaccount.
    """

    productId: int
    amount: int
    spot_leverage: Optional[bool]


class LiquidateSubaccountParams(BaseParamsSigned):
    """
    Parameters required to liquidate a subaccount.

    Attributes:
        liquidatee (Subaccount): The subaccount that is to be liquidated.
        mode (int): The mode of liquidation.
        healthGroup (int): The ID of the health group associated with the product being traded.
        amount (int): The amount to be liquidated.

    Methods:
        serialize_liquidatee(cls, v: Subaccount) -> bytes: Validates and converts the subaccount to bytes32 format.
    """

    liquidatee: Subaccount
    mode: int
    healthGroup: int
    amount: int

    @validator("liquidatee")
    def serialize_liquidatee(cls, v: Subaccount) -> bytes:
        return subaccount_to_bytes32(v)


class MintLpParams(BaseParamsSigned):
    """
    Parameters required for minting a liquidity provider token for a specific product in a subaccount.

    Attributes:
        productId (int): The ID of the product.
        amountBase (int): The amount of base to be consumed by minting LPs multiplied by 1e18.
        quoteAmountLow (int): The minimum amount of quote to be consumed by minting LPs multiplied by 1e18.
        quoteAmountHigh (int): The maximum amount of quote to be consumed by minting LPs multiplied by 1e18.
        spot_leverage (Optional[bool]): Indicates whether leverage is to be used. Defaults to True.
            If set to False, the transaction fails if it causes a borrow on the subaccount.
    """

    productId: int
    amountBase: int
    quoteAmountLow: int
    quoteAmountHigh: int
    spot_leverage: Optional[bool]


class BurnLpParams(BaseParamsSigned):
    """
    This class represents the parameters required to burn a liquidity provider
    token for a specific product in a subaccount.

    Attributes:
        productId (int): The ID of the product.
        amount (int): Combined amount of base + quote to burn multiplied by 1e18.
    """

    productId: int
    amount: int


class LinkSignerParams(BaseParamsSigned):
    """
    This class represents the parameters required to link a signer to a subaccount.

    Attributes:
        signer (Subaccount): The subaccount to be linked.

    Methods:
        serialize_signer(cls, v: Subaccount) -> bytes: Validates and converts the subaccount to bytes32 format.
    """

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
    """
    Parameters for a request to place an order.

    Attributes:
        place_order (PlaceOrderParams): The parameters for the order to be placed.

    Methods:
        serialize: Validates and serializes the order parameters.
    """

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
    """
    Parameters for a transaction request.

    Attributes:
        tx (dict): The transaction details.
        signature (str): The signature for the transaction.
        spot_leverage (Optional[bool]): Indicates whether leverage should be used. If set to false,
            it denotes no borrowing. Defaults to true.
        digest (Optional[str]): The digest of the transaction.

    Methods:
        serialize: Validates and serializes the transaction parameters.
    """

    tx: dict
    signature: str
    spot_leverage: Optional[bool]
    digest: Optional[str]

    @validator("tx")
    def serialize(cls, v: dict) -> dict:
        """
        Validates and serializes the transaction parameters.

        Args:
            v (dict): The transaction parameters to be validated and serialized.

        Raises:
            ValueError: If the 'nonce' attribute is missing in the transaction parameters.

        Returns:
            dict: The validated and serialized transaction parameters.
        """
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
    error_code: Optional[int]
    error: Optional[str]
    req: Optional[dict]


def to_execute_request(params: ExecuteParams) -> ExecuteRequest:
    execute_request_mapping = {
        PlaceOrderParams: (PlaceOrderRequest, VertexExecuteType.PLACE_ORDER),
        CancelOrdersParams: (CancelOrdersRequest, VertexExecuteType.CANCEL_ORDERS),
        CancelProductOrdersParams: (
            CancelProductOrdersRequest,
            VertexExecuteType.CANCEL_PRODUCT_ORDERS,
        ),
        WithdrawCollateralParams: (
            WithdrawCollateralRequest,
            VertexExecuteType.WITHDRAW_COLLATERAL,
        ),
        LiquidateSubaccountParams: (
            LiquidateSubaccountRequest,
            VertexExecuteType.LIQUIDATE_SUBACCOUNT,
        ),
        MintLpParams: (MintLpRequest, VertexExecuteType.MINT_LP),
        BurnLpParams: (BurnLpRequest, VertexExecuteType.BURN_LP),
        LinkSignerParams: (LinkSignerRequest, VertexExecuteType.LINK_SIGNER),
    }

    RequestClass, field_name = execute_request_mapping[type(params)]
    return RequestClass(**{field_name: params})
