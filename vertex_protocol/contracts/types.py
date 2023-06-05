from pydantic import Field
from enum import StrEnum

from vertex_protocol.utils.model import VertexBaseModel


class VertexNetwork(StrEnum):
    ARBITRUM_ONE = "arbitrumOne"
    ARBITRUM_GOERLI = "arbitrumGoerli"
    HARDHAT = "localhost"


class VertexAbiName(StrEnum):
    ENDPOINT = "Endpoint"
    FQUERIER = "FQuerier"
    ICLEARINGHOUSE = "IClearinghouse"
    IENDPOINT = "IEndpoint"
    IOFFCHAIN_BOOK = "IOffchainBook"
    IPERP_ENGINE = "IPerpEngine"
    ISPOT_ENGINE = "ISpotEngine"
    MOCK_ERC20 = "MockERC20"


class VertexDeployment(VertexBaseModel):
    node_url: str = Field(alias="nodeUrl")
    quote_addr: str = Field(alias="quote")
    querier_addr: str = Field(alias="querier")
    fee_calculator_addr: str = Field(alias="feeCalculator")
    clearinghouse_addr: str = Field(alias="clearinghouse")
    endpoint_addr: str = Field(alias="endpoint")
    spot_engine_addr: str = Field(alias="spotEngine")
    perp_engine_addr: str = Field(alias="perpEngine")


class DepositCollateralParams(VertexBaseModel):
    subaccount_name: str
    product_id: int
    amount: int


class VertexExecuteType(StrEnum):
    PLACE_ORDER = "place_order"
    CANCEL_ORDERS = "cancel_orders"
    CANCEL_PRODUCT_ORDERS = "cancel_product_orders"
    WITHDRAW_COLLATERAL = "withdraw_collateral"
    LIQUIDATE_SUBACCOUNT = "liquidate_subaccount"
    MINT_LP = "mint_lp"
    BURN_LP = "burn_lp"
    LINK_SIGNER = "link_signer"
