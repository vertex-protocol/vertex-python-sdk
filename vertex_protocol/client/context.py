import logging
from dataclasses import dataclass
from typing import Optional
from eth_account import Account

from pydantic import BaseModel
from vertex_protocol.contracts import VertexContracts, VertexContractsContext
from eth_account.signers.local import LocalAccount
from vertex_protocol.engine_client import EngineClient
from vertex_protocol.engine_client.types import Signer
from vertex_protocol.indexer_client import IndexerClient


@dataclass
class VertexClientContext:
    """
    Context required to use the Vertex client.
    """

    signer: Optional[LocalAccount]
    engine_client: EngineClient
    indexer_client: IndexerClient
    contracts: VertexContracts


class VertexClientContextOpts(BaseModel):
    contracts_context: VertexContractsContext
    rpc_node_url: str
    engine_endpoint: str
    indexer_endpoint: str


def create_vertex_client_context(
    opts: VertexClientContextOpts, signer: Signer = None
) -> VertexClientContext:
    """
    Initializes a VertexClientContext instance with the provided signer and options.

    Args:
        opts (VertexClientContextOpts): Options including endpoints for the engine and indexer clients.
        signer (Signer, optional): An instance of LocalAccount or a private key string for signing transactions.

    Returns:
        VertexClientContext: The initialized Vertex client context.

    Note:
        This helper attempts to fully set up the engine client, including the necessary verifying contracts
        to correctly sign executes. If this step fails, it is skipped and can be set up later, while logging the error.
    """
    engine_client = EngineClient({"url": opts.engine_endpoint, "signer": signer})
    try:
        contracts = engine_client.get_contracts()
        engine_client.endpoint_addr = contracts.endpoint_addr
        engine_client.book_addrs = contracts.book_addrs
        engine_client.chain_id = contracts.chain_id
    except Exception as e:
        logging.warning(
            f"Failed to setup engine client verifying contracts with error: {e}"
        )
    signer = Account.from_key(signer) if isinstance(signer, str) else signer
    return VertexClientContext(
        signer=signer,
        engine_client=engine_client,
        indexer_client=IndexerClient({"url": opts.indexer_endpoint}),
        contracts=VertexContracts(opts.rpc_node_url, opts.contracts_context),
    )
