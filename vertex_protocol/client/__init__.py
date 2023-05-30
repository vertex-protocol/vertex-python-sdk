from enum import Enum
import logging
from vertex_protocol.client.apis.market import MarketAPI
from vertex_protocol.client.apis.perp import PerpAPI
from vertex_protocol.client.apis.spot import SpotAPI
from vertex_protocol.client.apis.subaccount import SubaccountAPI
from vertex_protocol.client.context import (
    VertexClientContext,
    VertexClientContextOpts,
    create_vertex_client_context,
)
from vertex_protocol.engine_client.types import Signer
from vertex_protocol.utils.endpoint import VertexEndpoint


class VertexClientMode(str, Enum):
    MAINNET = "mainnet"
    TESTNET = "testnet"
    DEVNET = "devnet"


class VertexClient:
    """
    Client for querying and executing against Vertex Clearinghouse.
    Use `create_vertex_client` for initialization.
    """

    def __init__(self, context: VertexClientContext):
        """
        Initialize a new instance of the VertexClient.

        Args:
            context (VertexClientContext): The client context.

        Note:
            Use `create_vertex_client` for creating instances.
        """
        self.context = context
        self.market = MarketAPI(context)
        self.subaccount = SubaccountAPI(context)
        self.spot = SpotAPI(context)
        self.perp = PerpAPI(context)


def create_vertex_client(
    mode: VertexClientMode, signer: Signer, context_opts: VertexClientContextOpts = None
) -> VertexClient:
    """
    Create a new VertexClient based on the given mode and signer.

    This function will create a new VertexClientContext based on the provided mode, and then
    initialize a new VertexClient with that context.

    If `context_opts` are provided, they will be used to create the client context. Otherwise,
    default context options for the given mode will be used.

    Args:
        mode (VertexClientMode): The mode in which to operate the client. Can be one of the following:
            VertexClientMode.MAINNET: For operating in Vertex's mainnet environment.
            VertexClientMode.TESTNET: For operating in Vertex's testnet environment.
            VertexClientMode.DEVNET: For local development.

        signer (Signer): An instance of LocalAccount or a private key string for signing transactions.

        context_opts (VertexClientContextOpts, optional): Options for creating the client context.
            If not provided, default options for the given mode will be used.

    Returns:
        VertexClient: The created VertexClient instance.
    """
    mode_to_endpoints = {
        VertexClientMode.MAINNET: (VertexEndpoint.MAINNET, VertexEndpoint.MAINNET),
        VertexClientMode.TESTNET: (VertexEndpoint.TESTNET, VertexEndpoint.TESTNET),
        VertexClientMode.DEVNET: (
            VertexEndpoint.DEVNET_ENGINE,
            VertexEndpoint.DEVNET_INDEXER,
        ),
    }

    context: VertexClientContext
    if context_opts:
        context = create_vertex_client_context(signer, context_opts)
    else:
        logging.warning(f"Initializing default {mode} context")
        try:
            engine_endpoint, indexer_endpoint = mode_to_endpoints[mode]
        except KeyError:
            raise Exception(f"Mode provided `{mode}` not supported!")
        context = create_vertex_client_context(
            signer,
            VertexClientContextOpts(
                engine_endpoint=engine_endpoint,
                indexer_endpoint=indexer_endpoint,
            ),
        )
    return VertexClient(context)
