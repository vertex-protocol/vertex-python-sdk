from typing import Optional
from pydantic import BaseModel
from web3 import Web3
from web3.contract import Contract

from vertex_protocol.contracts.loader import load_abi
from vertex_protocol.contracts.types import VertexAbiName


class VertexContractsContext(BaseModel):
    endpoint_addr: str
    querier_addr: str
    spot_engine_addr: Optional[str]
    perp_engine_addr: Optional[str]
    clearinghouse_addr: Optional[str]


class VertexContracts:
    """
    Encapsulates the set of Vertex contracts required for querying and executing.
    """

    def __init__(self, node_url: str, contracts_context: VertexContractsContext):
        self.w3 = Web3(Web3.HTTPProvider(node_url))
        self.contracts_context = VertexContractsContext.parse_obj(contracts_context)
        self.querier: Contract = self.w3.eth.contract(
            address=contracts_context.querier_addr, abi=load_abi(VertexAbiName.FQUERIER)
        )
        self.endpoint: Contract = self.w3.eth.contract(
            address=self.contracts_context.endpoint_addr,
            abi=load_abi(VertexAbiName.ENDPOINT),
        )
        self.clearinghouse = None
        self.spot_engine = None
        self.perp_engine = None

        if self.contracts_context.clearinghouse_addr:
            self.clearinghouse: Contract = self.w3.eth.contract(
                address=self.contracts_context.clearinghouse_addr,
                abi=load_abi(VertexAbiName.ICLEARINGHOUSE),
            )

        if self.contracts_context.spot_engine_addr:
            self.spot_engine: Contract = self.w3.eth.contract(
                address=self.contracts_context.spot_engine_addr,
                abi=load_abi(VertexAbiName.ISPOT_ENGINE),
            )

        if self.contracts_context.perp_engine_addr:
            self.perp_engine: Contract = self.w3.eth.contract(
                address=self.contracts_context.perp_engine_addr,
                abi=load_abi(VertexAbiName.IPERP_ENGINE),
            )
