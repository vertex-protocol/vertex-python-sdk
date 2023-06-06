from pydantic import Field
from enum import StrEnum

from vertex_protocol.utils.model import VertexBaseModel


class VertexNetwork(StrEnum):
    """
    Enumeration representing various network environments for the Vertex protocol.
    """

    ARBITRUM_ONE = "arbitrumOne"
    ARBITRUM_GOERLI = "arbitrumGoerli"
    HARDHAT = "localhost"


class VertexAbiName(StrEnum):
    """
    Enumeration representing various contract names for which the ABI can be loaded in the Vertex protocol.
    """

    ENDPOINT = "Endpoint"
    FQUERIER = "FQuerier"
    ICLEARINGHOUSE = "IClearinghouse"
    IENDPOINT = "IEndpoint"
    IOFFCHAIN_BOOK = "IOffchainBook"
    IPERP_ENGINE = "IPerpEngine"
    ISPOT_ENGINE = "ISpotEngine"
    MOCK_ERC20 = "MockERC20"


class VertexDeployment(VertexBaseModel):
    """
    Class representing deployment data for Vertex protocol contracts.

    Attributes:
        node_url (str): The URL of the node.
        quote_addr (str): The address of the quote contract.
        querier_addr (str): The address of the querier contract.
        fee_calculator_addr (str): The address of the fee calculator contract.
        clearinghouse_addr (str): The address of the clearinghouse contract.
        endpoint_addr (str): The address of the endpoint contract.
        spot_engine_addr (str): The address of the spot engine contract.
        perp_engine_addr (str): The address of the perpetual engine contract.
    """

    node_url: str = Field(alias="nodeUrl")
    quote_addr: str = Field(alias="quote")
    querier_addr: str = Field(alias="querier")
    fee_calculator_addr: str = Field(alias="feeCalculator")
    clearinghouse_addr: str = Field(alias="clearinghouse")
    endpoint_addr: str = Field(alias="endpoint")
    spot_engine_addr: str = Field(alias="spotEngine")
    perp_engine_addr: str = Field(alias="perpEngine")


class DepositCollateralParams(VertexBaseModel):
    """
    Class representing parameters for depositing collateral in the Vertex protocol.

    Attributes:
        subaccount_name (str): The name of the subaccount.
        product_id (int): The ID of the spot product to deposit collateral for.
        amount (int): The amount of collateral to be deposited.
    """

    subaccount_name: str
    product_id: int
    amount: int


class VertexExecuteType(StrEnum):
    """
    Enumeration of possible actions to execute in Vertex.
    """

    PLACE_ORDER = "place_order"
    CANCEL_ORDERS = "cancel_orders"
    CANCEL_PRODUCT_ORDERS = "cancel_product_orders"
    WITHDRAW_COLLATERAL = "withdraw_collateral"
    LIQUIDATE_SUBACCOUNT = "liquidate_subaccount"
    MINT_LP = "mint_lp"
    BURN_LP = "burn_lp"
    LINK_SIGNER = "link_signer"
