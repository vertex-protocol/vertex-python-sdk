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
from vertex_protocol.contracts import VertexContractsContext
from vertex_protocol.contracts.loader import load_deployment
from vertex_protocol.contracts.types import VertexNetwork
from vertex_protocol.engine_client.types import Signer
from vertex_protocol.utils.backend import VertexBackendURL
from vertex_protocol.utils.enum import StrEnum
from vertex_protocol.client.context import *

from pydantic import parse_obj_as


class VertexClientMode(StrEnum):
    """
    VertexClientMode is an enumeration representing the operational modes of the VertexClient.

    Attributes:
        MAINNET: For operating in Vertex's mainnet environment.

        TESTNET: For operating in Vertex's testnet environment.

        DEVNET: For local development.

        TESTING: For running tests.
    """

    MAINNET = "mainnet"
    TESTNET = "testnet"
    DEVNET = "devnet"
    TESTING = "testing"


class VertexClient:
    """
    The primary client interface for interacting with Vertex Protocol.

    This client consolidates the functionality of various aspects of Vertex such as spot, market,
    subaccount, and perpetual (perp) operations.

    To initialize an instance of this client, use the `create_vertex_client` utility.

    Attributes:
        - context (VertexClientContext): The client context containing configuration for interacting with Vertex.
        - market (MarketAPI): Sub-client for executing and querying market operations.
        - subaccount (SubaccountAPI): Sub-client for executing and querying subaccount operations.
        - spot (SpotAPI): Sub-client for executing and querying spot operations.
        - perp (PerpAPI): Sub-client for executing and querying perpetual operations.
    """

    context: VertexClientContext
    market: MarketAPI
    subaccount: SubaccountAPI
    spot: SpotAPI
    perp: PerpAPI

    def __init__(self, context: VertexClientContext):
        """
        Initialize a new instance of the VertexClient.

        This constructor should not be called directly. Instead, use the `create_vertex_client` utility to
        create a new VertexClient. This is because the `create_vertex_client` utility includes important
        additional setup steps that aren't included in this constructor.

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
    mode: VertexClientMode,
    signer: Optional[Signer] = None,
    context_opts: Optional[VertexClientContextOpts] = None,
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

        signer (Signer, optional): An instance of LocalAccount or a private key string for signing transactions.

        context_opts (VertexClientContextOpts, optional): Options for creating the client context.
            If not provided, default options for the given mode will be used.

    Returns:
        VertexClient: The created VertexClient instance.
    """
    context: VertexClientContext
    if context_opts:
        context = create_vertex_client_context(context_opts, signer)
    else:
        logging.warning(f"Initializing default {mode} context")
        engine_endpoint_url, indexer_endpoint_url, network_name = client_mode_to_setup(
            mode
        )
        deployment = load_deployment(VertexNetwork(network_name))
        context = create_vertex_client_context(
            VertexClientContextOpts(
                rpc_node_url=deployment.node_url,
                engine_endpoint_url=parse_obj_as(AnyUrl, engine_endpoint_url),
                indexer_endpoint_url=parse_obj_as(AnyUrl, indexer_endpoint_url),
                contracts_context=VertexContractsContext(
                    endpoint_addr=deployment.endpoint_addr,
                    querier_addr=deployment.querier_addr,
                    perp_engine_addr=deployment.perp_engine_addr,
                    spot_engine_addr=deployment.spot_engine_addr,
                    clearinghouse_addr=deployment.clearinghouse_addr,
                ),
            ),
            signer,
        )
    return VertexClient(context)


def client_mode_to_setup(
    client_mode: VertexClientMode,
) -> tuple[str, str, str]:
    try:
        return {
            VertexClientMode.MAINNET: (
                VertexBackendURL.MAINNET.value,
                VertexBackendURL.MAINNET.value,
                VertexNetwork.ARBITRUM_ONE.value,
            ),
            VertexClientMode.TESTNET: (
                VertexBackendURL.TESTNET.value,
                VertexBackendURL.TESTNET.value,
                VertexNetwork.ARBITRUM_GOERLI.value,
            ),
            VertexClientMode.DEVNET: (
                VertexBackendURL.DEVNET_ENGINE.value,
                VertexBackendURL.DEVNET_INDEXER.value,
                VertexNetwork.HARDHAT.value,
            ),
            VertexClientMode.TESTING: (
                VertexBackendURL.DEVNET_ENGINE.value,
                VertexBackendURL.DEVNET_INDEXER.value,
                VertexNetwork.TESTING.value,
            ),
        }[client_mode]
    except KeyError:
        raise Exception(f"Mode provided `{client_mode}` not supported!")


__all__ = [
    "VertexClient",
    "VertexClientMode",
    "create_vertex_client",
    "VertexClientContext",
    "VertexClientContextOpts",
    "create_vertex_client_context",
]
