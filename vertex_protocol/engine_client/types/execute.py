from typing import Optional, Type, Union
from pydantic import validator
from vertex_protocol.contracts.types import VertexExecuteType
from vertex_protocol.engine_client.types.models import ResponseStatus
from vertex_protocol.utils.execute import (
    BaseParamsSigned,
    IsolatedOrderParams,
    MarketOrderParams,
    OrderParams,
    SignatureParams,
)
from vertex_protocol.utils.model import VertexBaseModel
from vertex_protocol.utils.bytes32 import (
    bytes32_to_hex,
    hex_to_bytes32,
    subaccount_to_bytes32,
)
from vertex_protocol.utils.subaccount import Subaccount
from vertex_protocol.engine_client.types.query import OrderData


Digest = Union[str, bytes]


class PlaceOrderParams(SignatureParams):
    """
    Class for defining the parameters needed to place an order.

    Attributes:
        id (Optional[int]): An optional custom order id that is echoed back in subscription events e.g: fill orders, etc.

        product_id (int): The id of the product for which the order is being placed.

        order (OrderParams): The parameters of the order.

        digest (Optional[str]): An optional hash of the order data.

        spot_leverage (Optional[bool]): An optional flag indicating whether leverage should be used for the order. By default, leverage is assumed.
    """

    id: Optional[int]
    product_id: int
    order: OrderParams
    digest: Optional[str]
    spot_leverage: Optional[bool]


class PlaceIsolatedOrderParams(SignatureParams):
    """
    Class for defining the parameters needed to place an isolated order.

    Attributes:
        id (Optional[int]): An optional custom order id that is echoed back in subscription events e.g: fill orders, etc.

        product_id (int): The id of the product for which the order is being placed.

        isolated_order (IsolatedOrderParams): The parameters of the isolated order.

        digest (Optional[str]): An optional hash of the order data.

        borrow_margin (Optional[bool]): Whether the cross subaccount can borrow quote for the margin transfer into the isolated subaccount. If not provided, it defaults to true.
    """

    id: Optional[int]
    product_id: int
    isolated_order: IsolatedOrderParams
    digest: Optional[str]
    borrow_margin: Optional[bool]


class PlaceMarketOrderParams(SignatureParams):
    """
    Class for defining the parameters needed to place a market order.

    Attributes:
        product_id (int): The id of the product for which the order is being placed.

        slippage (Optional[float]): Optional slippage allowed in market price. Defaults to 0.005 (0.5%)

        market_order (MarketOrderParams): The parameters of the market order.

        spot_leverage (Optional[bool]): An optional flag indicating whether leverage should be used for the order. By default, leverage is assumed.

        reduce_only (Optional[bool]): When True, the order can only reduce the size of an existing position. Works only with IOC & FOK.
    """

    product_id: int
    market_order: MarketOrderParams
    slippage: Optional[float]
    spot_leverage: Optional[bool]
    reduce_only: Optional[bool]


class CancelOrdersParams(BaseParamsSigned):
    """
    Parameters to cancel specific orders.

    Args:
        productIds (list[int]): List of product IDs for the orders to be canceled.

        digests (list[Digest]): List of digests of the orders to be canceled.

        nonce (Optional[int]): A unique number used to prevent replay attacks.

    Methods:
        serialize_digests: Validates and converts a list of hex digests to bytes32.
    """

    productIds: list[int]
    digests: list[Digest]
    nonce: Optional[int]

    @validator("digests")
    def serialize_digests(cls, v: list[Digest]) -> list[bytes]:
        return [hex_to_bytes32(digest) for digest in v]


class CancelProductOrdersParams(BaseParamsSigned):
    """
    Parameters to cancel all orders for specific products.

    Args:
        productIds (list[int]): List of product IDs for the orders to be canceled.

        digest (str, optional): Optional EIP-712 digest of the CancelProductOrder request.

        nonce (Optional[int]): A unique number used to prevent replay attacks.
    """

    productIds: list[int]
    digest: Optional[str]
    nonce: Optional[int]


class CancelAndPlaceParams(VertexBaseModel):
    """
    Parameters to perform an order cancellation + order placement in the same request.

    Args:
        cancel_orders (CancelOrdersParams): Order cancellation object.
        place_order (PlaceOrderParams): Order placement object.
    """

    cancel_orders: CancelOrdersParams
    place_order: PlaceOrderParams


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

        productId (int): ID of product to liquidate.

        isEncodedSpread (bool): When set to True, productId is expected to encode a perp and spot product Ids as follows: (perp_id << 16) | spot_id

        amount (int): The amount to be liquidated.

    Methods:
        serialize_liquidatee(cls, v: Subaccount) -> bytes: Validates and converts the liquidatee subaccount to bytes32 format.
    """

    liquidatee: Subaccount
    productId: int
    isEncodedSpread: bool
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


ExecuteParams = Union[
    PlaceOrderParams,
    PlaceIsolatedOrderParams,
    CancelOrdersParams,
    CancelProductOrdersParams,
    WithdrawCollateralParams,
    LiquidateSubaccountParams,
    MintLpParams,
    BurnLpParams,
    LinkSignerParams,
    CancelAndPlaceParams,
]


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


class PlaceIsolatedOrderRequest(VertexBaseModel):
    """
    Parameters for a request to place an isolated order.

    Attributes:
        place_isolated_order (PlaceIsolatedOrderParams): The parameters for the isolated order to be placed.

    Methods:
        serialize: Validates and serializes the order parameters.
    """

    place_isolated_order: PlaceIsolatedOrderParams

    @validator("place_isolated_order")
    def serialize(cls, v: PlaceIsolatedOrderParams) -> PlaceIsolatedOrderParams:
        if v.isolated_order.nonce is None:
            raise ValueError("Missing order `nonce`")
        if v.signature is None:
            raise ValueError("Missing `signature")
        if isinstance(v.isolated_order.sender, bytes):
            v.isolated_order.serialize_dict(["sender"], bytes32_to_hex)
        v.isolated_order.serialize_dict(
            ["nonce", "priceX18", "amount", "expiration", "margin"], str
        )
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
    """
    Converts a BaseParamsSigned object to a TxRequest object.

    Args:
        cls (Type[VertexBaseModel]): The type of the model to convert.

        v (BaseParamsSigned): The signed parameters to be converted.

    Raises:
        ValueError: If the 'signature' attribute is missing in the BaseParamsSigned object.

    Returns:
        TxRequest: The converted transaction request.
    """
    if v.signature is None:
        raise ValueError("Missing `signature`")
    return TxRequest(
        tx=v.dict(exclude={"signature", "digest", "spot_leverage"}),
        signature=v.signature,
        spot_leverage=v.dict().get("spot_leverage"),
        digest=v.dict().get("digest"),
    )


class CancelOrdersRequest(VertexBaseModel):
    """
    Parameters for a cancel orders request.

    Attributes:
        cancel_orders (CancelOrdersParams): The parameters of the orders to be cancelled.

    Methods:
        serialize: Serializes 'digests' in 'cancel_orders' into their hexadecimal representation.

        to_tx_request: Validates and converts 'cancel_orders' into a transaction request.
    """

    cancel_orders: CancelOrdersParams

    @validator("cancel_orders")
    def serialize(cls, v: CancelOrdersParams) -> CancelOrdersParams:
        """
        Serializes 'digests' in 'cancel_orders' into their hexadecimal representation.

        Args:
            v (CancelOrdersParams): The parameters of the orders to be cancelled.

        Returns:
            CancelOrdersParams: The 'cancel_orders' with serialized 'digests'.
        """
        v.serialize_dict(["digests"], lambda l: [bytes32_to_hex(x) for x in l])
        return v

    _validator = validator("cancel_orders", allow_reuse=True)(to_tx_request)


class CancelAndPlaceRequest(VertexBaseModel):
    """
    Parameters for a cancel and place request.

    Attributes:
        cancel_and_place (CancelAndPlaceParams): Request parameters for engine cancel_and_place execution
    """

    cancel_and_place: CancelAndPlaceParams

    @validator("cancel_and_place")
    def serialize(cls, v: CancelAndPlaceParams) -> dict:
        cancel_tx = TxRequest.parse_obj(
            CancelOrdersRequest(cancel_orders=v.cancel_orders).cancel_orders
        )
        return {
            "cancel_tx": cancel_tx.tx,
            "place_order": PlaceOrderRequest(place_order=v.place_order).place_order,
            "cancel_signature": cancel_tx.signature,
        }


class CancelProductOrdersRequest(VertexBaseModel):
    """
    Parameters for a cancel product orders request.

    Attributes:
        cancel_product_orders (CancelProductOrdersParams): The parameters of the product orders to be cancelled.

    Methods:
        to_tx_request: Validates and converts 'cancel_product_orders' into a transaction request.
    """

    cancel_product_orders: CancelProductOrdersParams

    _validator = validator("cancel_product_orders", allow_reuse=True)(to_tx_request)


class WithdrawCollateralRequest(VertexBaseModel):
    """
    Parameters for a withdraw collateral request.

    Attributes:
        withdraw_collateral (WithdrawCollateralParams): The parameters of the collateral to be withdrawn.

    Methods:
        serialize: Validates and converts the 'amount' attribute of 'withdraw_collateral' to string.

        to_tx_request: Validates and converts 'withdraw_collateral' into a transaction request.
    """

    withdraw_collateral: WithdrawCollateralParams

    @validator("withdraw_collateral")
    def serialize(cls, v: WithdrawCollateralParams) -> WithdrawCollateralParams:
        v.serialize_dict(["amount"], str)
        return v

    _validator = validator("withdraw_collateral", allow_reuse=True)(to_tx_request)


class LiquidateSubaccountRequest(VertexBaseModel):
    """
    Parameters for a liquidate subaccount request.

    Attributes:
        liquidate_subaccount (LiquidateSubaccountParams): The parameters for the subaccount to be liquidated.

    Methods:
        serialize: Validates and converts the 'amount' attribute and the 'liquidatee' attribute
        of 'liquidate_subaccount' to their proper serialized forms.

        to_tx_request: Validates and converts 'liquidate_subaccount' into a transaction request.
    """

    liquidate_subaccount: LiquidateSubaccountParams

    @validator("liquidate_subaccount")
    def serialize(cls, v: LiquidateSubaccountParams) -> LiquidateSubaccountParams:
        v.serialize_dict(["amount"], str)
        v.serialize_dict(["liquidatee"], bytes32_to_hex)
        return v

    _validator = validator("liquidate_subaccount", allow_reuse=True)(to_tx_request)


class MintLpRequest(VertexBaseModel):
    """
    Parameters for a mint LP request.

    Attributes:
        mint_lp (MintLpParams): The parameters for minting liquidity.

    Methods:
        serialize: Validates and converts the 'amountBase', 'quoteAmountLow', and 'quoteAmountHigh'
        attributes of 'mint_lp' to their proper serialized forms.

        to_tx_request: Validates and converts 'mint_lp' into a transaction request.
    """

    mint_lp: MintLpParams

    @validator("mint_lp")
    def serialize(cls, v: MintLpParams) -> MintLpParams:
        v.serialize_dict(["amountBase", "quoteAmountLow", "quoteAmountHigh"], str)
        return v

    _validator = validator("mint_lp", allow_reuse=True)(to_tx_request)


class BurnLpRequest(VertexBaseModel):
    """
    Parameters for a burn LP request.

    Attributes:
        burn_lp (BurnLpParams): The parameters for burning liquidity.

    Methods:
        serialize: Validates and converts the 'amount' attribute of 'burn_lp' to its proper serialized form.

        to_tx_request: Validates and converts 'burn_lp' into a transaction request.
    """

    burn_lp: BurnLpParams

    @validator("burn_lp")
    def serialize(cls, v: BurnLpParams) -> BurnLpParams:
        v.serialize_dict(["amount"], str)
        return v

    _validator = validator("burn_lp", allow_reuse=True)(to_tx_request)


class LinkSignerRequest(VertexBaseModel):
    """
    Parameters for a request to link a signer to a subaccount.

    Attributes:
        link_signer (LinkSignerParams): Parameters including the subaccount to be linked.

    Methods:
        serialize: Validates and converts the 'signer' attribute of 'link_signer' into its hexadecimal representation.

        to_tx_request: Validates and converts 'link_signer' into a transaction request.
    """

    link_signer: LinkSignerParams

    @validator("link_signer")
    def serialize(cls, v: LinkSignerParams) -> LinkSignerParams:
        v.serialize_dict(["signer"], bytes32_to_hex)
        return v

    _validator = validator("link_signer", allow_reuse=True)(to_tx_request)


ExecuteRequest = Union[
    PlaceOrderRequest,
    PlaceIsolatedOrderRequest,
    CancelOrdersRequest,
    CancelProductOrdersRequest,
    CancelAndPlaceRequest,
    WithdrawCollateralRequest,
    LiquidateSubaccountRequest,
    MintLpRequest,
    BurnLpRequest,
    LinkSignerRequest,
]


class PlaceOrderResponse(VertexBaseModel):
    """
    Data model for place order response.
    """

    digest: str


class CancelOrdersResponse(VertexBaseModel):
    """
    Data model for cancelled orders response.
    """

    cancelled_orders: list[OrderData]


ExecuteResponseData = Union[PlaceOrderResponse, CancelOrdersResponse]


class ExecuteResponse(VertexBaseModel):
    """
    Represents the response returned from executing a request.

    Attributes:
        status (ResponseStatus): The status of the response.

        signature (Optional[str]): The signature of the response. Only present if the request was successfully executed.

        data (Optional[ExecuteResponseData]): Data returned from execute, not all executes currently return data.

        error_code (Optional[int]): The error code, if any error occurred during the execution of the request.

        error (Optional[str]): The error message, if any error occurred during the execution of the request.

        request_type (Optional[str]): Type of the request.

        req (Optional[dict]): The original request that was executed.

        id (Optional[id]): An optional client id provided when placing an order
    """

    status: ResponseStatus
    signature: Optional[str]
    data: Optional[ExecuteResponseData]
    error_code: Optional[int]
    error: Optional[str]
    request_type: Optional[str]
    req: Optional[dict]
    id: Optional[int]


def to_execute_request(params: ExecuteParams) -> ExecuteRequest:
    """
    Maps `ExecuteParams` to its corresponding `ExecuteRequest` object based on the parameter type.

    Args:
        params (ExecuteParams): The parameters to be executed.

    Returns:
        ExecuteRequest: The corresponding `ExecuteRequest` object.
    """
    execute_request_mapping = {
        PlaceOrderParams: (PlaceOrderRequest, VertexExecuteType.PLACE_ORDER.value),
        PlaceIsolatedOrderParams: (
            PlaceIsolatedOrderRequest,
            VertexExecuteType.PLACE_ISOLATED_ORDER.value,
        ),
        CancelOrdersParams: (
            CancelOrdersRequest,
            VertexExecuteType.CANCEL_ORDERS.value,
        ),
        CancelProductOrdersParams: (
            CancelProductOrdersRequest,
            VertexExecuteType.CANCEL_PRODUCT_ORDERS.value,
        ),
        WithdrawCollateralParams: (
            WithdrawCollateralRequest,
            VertexExecuteType.WITHDRAW_COLLATERAL.value,
        ),
        LiquidateSubaccountParams: (
            LiquidateSubaccountRequest,
            VertexExecuteType.LIQUIDATE_SUBACCOUNT.value,
        ),
        MintLpParams: (MintLpRequest, VertexExecuteType.MINT_LP.value),
        BurnLpParams: (BurnLpRequest, VertexExecuteType.BURN_LP.value),
        LinkSignerParams: (LinkSignerRequest, VertexExecuteType.LINK_SIGNER.value),
        CancelAndPlaceParams: (
            CancelAndPlaceRequest,
            VertexExecuteType.CANCEL_AND_PLACE.value,
        ),
    }

    RequestClass, field_name = execute_request_mapping[type(params)]
    return RequestClass(**{field_name: params})  # type: ignore
