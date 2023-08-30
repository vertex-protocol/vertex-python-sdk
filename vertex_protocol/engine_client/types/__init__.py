from eth_account import Account
from eth_account.signers.local import LocalAccount
from typing import Optional, Union
from pydantic import BaseModel, AnyUrl, validator, root_validator
from vertex_protocol.engine_client.types.execute import *
from vertex_protocol.engine_client.types.models import *
from vertex_protocol.engine_client.types.query import *

PrivateKey = str
Signer = Union[LocalAccount, PrivateKey]


class EngineClientOpts(BaseModel):
    """
    Model defining the configuration options for the Engine Client. It includes various parameters such as the URL,
    the signer, the linked signer, the chain ID, and others.

    Attributes:
        url (AnyUrl): The URL of the server.
        signer (Optional[Signer]): The signer for the client, if any. It can either be a `LocalAccount` or a private key.
        linked_signer (Optional[Signer]): An optional signer linked the main subaccount to perform executes on it's behalf.
        chain_id (Optional[int]): An optional network chain ID.
        endpoint_addr (Optional[str]): Vertex's endpoint address used for verifying executes.
        book_addrs (Optional[list[str]]): Vertex's book addresses used for verifying order placement.

    Notes:
        - The class also includes several methods for validating and sanitizing the input values.
        - "linked_signer" cannot be set if "signer" is not set.
    """

    url: AnyUrl
    signer: Optional[Union[LocalAccount, PrivateKey]] = None
    linked_signer: Optional[Signer] = None
    chain_id: Optional[int] = None
    endpoint_addr: Optional[str] = None
    book_addrs: Optional[list[str]] = None

    class Config:
        arbitrary_types_allowed = True

    @root_validator
    def check_linked_signer(cls, values: dict):
        """
        Validates that if a linked_signer is set, a signer must also be set.

        Args:
            values (dict): The input values to be validated.

        Raises:
            ValueError: If linked_signer is set but signer is not.

        Returns:
            dict: The validated values.
        """
        signer, linked_signer = values.get("signer"), values.get("linked_signer")
        if linked_signer and not signer:
            raise ValueError("linked_signer cannot be set if signer is not set")
        return values

    @validator("url")
    def clean_url(cls, v: AnyUrl) -> str:
        """
        Cleans the URL input by removing trailing slashes.

        Args:
            v (AnyUrl): The input URL.

        Returns:
            str: The cleaned URL.
        """
        return v.rstrip("/")

    @validator("signer")
    def signer_to_local_account(cls, v: Optional[Signer]) -> Optional[LocalAccount]:
        """
        Validates and converts the signer to a LocalAccount instance.

        Args:
            v (Optional[Signer]): The signer instance or None.

        Returns:
            Optional[LocalAccount]: The LocalAccount instance or None.
        """
        if v is None or isinstance(v, LocalAccount):
            return v
        return Account.from_key(v)

    @validator("linked_signer")
    def linked_signer_to_local_account(
        cls, v: Optional[Signer]
    ) -> Optional[LocalAccount]:
        """
        Validates and converts the linked_signer to a LocalAccount instance.

        Args:
            v (Optional[Signer]): The linked_signer instance or None.

        Returns:
            Optional[LocalAccount]: The LocalAccount instance or None.
        """
        if v is None or isinstance(v, LocalAccount):
            return v
        return Account.from_key(v)


__all__ = [
    "BaseParams",
    "SignatureParams",
    "BaseParamsSigned",
    "OrderParams",
    "PlaceOrderParams",
    "CancelOrdersParams",
    "CancelProductOrdersParams",
    "CancelAndPlaceParams",
    "WithdrawCollateralParams",
    "LiquidateSubaccountParams",
    "MintLpParams",
    "BurnLpParams",
    "LinkSignerParams",
    "ExecuteParams",
    "TxRequest",
    "PlaceOrderRequest",
    "CancelOrdersRequest",
    "CancelProductOrdersRequest",
    "CancelAndPlaceRequest",
    "WithdrawCollateralRequest",
    "LiquidateSubaccountRequest",
    "MintLpRequest",
    "BurnLpRequest",
    "LinkSignerRequest",
    "ExecuteRequest",
    "ExecuteResponse",
    "EngineQueryType",
    "QueryStatusParams",
    "QueryContractsParams",
    "QueryNoncesParams",
    "QueryOrderParams",
    "QuerySubaccountInfoTx",
    "QuerySubaccountInfoParams",
    "QuerySubaccountOpenOrdersParams",
    "QueryMarketLiquidityParams",
    "QueryAllProductsParams",
    "QueryMarketPriceParams",
    "QueryMaxOrderSizeParams",
    "QueryMaxWithdrawableParams",
    "QueryMaxLpMintableParams",
    "QueryFeeRatesParams",
    "QueryHealthGroupsParams",
    "QueryLinkedSignerParams",
    "QueryRequest",
    "StatusData",
    "ContractsData",
    "NoncesData",
    "OrderData",
    "SubaccountInfoData",
    "SubaccountOpenOrdersData",
    "MarketLiquidityData",
    "AllProductsData",
    "MarketPriceData",
    "MaxOrderSizeData",
    "MaxWithdrawableData",
    "MaxLpMintableData",
    "FeeRatesData",
    "HealthGroupsData",
    "LinkedSignerData",
    "QueryResponseData",
    "QueryResponse",
    "ResponseStatus",
    "EngineStatus",
    "MintLp",
    "BurnLp",
    "ApplyDelta",
    "MintLpTx",
    "BurnLpTx",
    "ApplyDeltaTx",
    "SubaccountHealth",
    "SpotLpBalance",
    "SpotBalance",
    "SpotProductBalance",
    "PerpLpBalance",
    "PerpBalance",
    "PerpProductBalance",
    "ProductRisk",
    "ProductBookInfo",
    "BaseProduct",
    "BaseProductLpState",
    "SpotProductConfig",
    "SpotProductState",
    "SpotProductLpAmount",
    "SpotProductLpState",
    "SpotProduct",
    "PerpProductState",
    "PerpProductLpState",
    "PerpProduct",
    "MaxOrderSizeDirection",
    "MarketLiquidity",
]
