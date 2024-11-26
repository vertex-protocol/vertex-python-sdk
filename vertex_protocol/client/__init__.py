import logging
from vertex_protocol.client.apis.market import MarketAPI
from vertex_protocol.client.apis.perp import PerpAPI
from vertex_protocol.client.apis.spot import SpotAPI
from vertex_protocol.client.apis.subaccount import SubaccountAPI
from vertex_protocol.client.apis.rewards import RewardsAPI
from vertex_protocol.client.context import (
    VertexClientContext,
    VertexClientContextOpts,
    create_vertex_client_context,
)
from vertex_protocol.contracts import VertexContractsContext
from vertex_protocol.contracts.loader import load_deployment
from vertex_protocol.contracts.types import VertexNetwork
from vertex_protocol.utils.backend import VertexBackendURL, Signer
from vertex_protocol.utils.enum import StrEnum
from vertex_protocol.client.context import *

from pydantic import parse_obj_as


class VertexClientMode(StrEnum):
    """
    VertexClientMode is an enumeration representing the operational modes of the VertexClient.

    Attributes:
        MAINNET: For operating in Vertex's mainnet environment deployed on Arbitrum One.

        BLAST_MAINNET: For operating in Vertex's mainnet environment deployed on Blast Mainnet.

        MANTLE_MAINNET: For operating in Vertex's mainnet environment deployed on Mantle Mainnet.

        SEI_MAINNET: For operating in Vertex's mainnet environment deployed on Sei Mainnet.

        BASE_MAINNET: For operating in Vertex's mainnet environment deployed on Base Mainnet.

        SEPOLIA_TESTNET: For operating in Vertex's testnet environment deployed on Arbitrum Sepolia.

        BLAST_TESTNET: For operating in Vertex's testnet environment deployed on Blast Testnet.

        MANTLE_TESTNET: For operating in Vertex's testnet environment deployed on Mantle Testnet.

        SEI_TESTNET: For operating in Vertex's testnet environment deployed on Sei Testnet.

        BASE_TESTNET: For operating in Vertex's testnet environment deployed on Base Testnet.

        DEVNET: For local development.

        TESTING: For running tests.
    """

    MAINNET = "mainnet"
    BLAST_MAINNET = "blast-mainnet"
    MANTLE_MAINNET = "mantle-mainnet"
    SEI_MAINNET = "sei-mainnet"
    BASE_MAINNET = "base-mainnet"
    SEPOLIA_TESTNET = "sepolia-testnet"
    BLAST_TESTNET = "blast-testnet"
    MANTLE_TESTNET = "mantle-testnet"
    SEI_TESTNET = "sei-testnet"
    BASE_TESTNET = "base-testnet"
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
        - rewards (RewardsAPI): Sub-client for executing and querying rewards operations (e.g: staking, claiming, etc).
    """

    context: VertexClientContext
    market: MarketAPI
    subaccount: SubaccountAPI
    spot: SpotAPI
    perp: PerpAPI
    rewards: RewardsAPI

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
        self.rewards = RewardsAPI(context)


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
            VertexClientMode.MAINNET: For operating in Vertex's mainnet environment deployed on Arbitrum One.
            VertexClientMode.BLAST_MAINNET: For operating in Vertex's mainnet environment deployed on Blast Mainnet.
            VertexClientMode.SEPOLIA_TESTNET: For operating in Vertex's testnet environment deployed on Arbitrum Sepolia.
            VertexClientMode.DEVNET: For local development.

        signer (Signer, optional): An instance of LocalAccount or a private key string for signing transactions.

        context_opts (VertexClientContextOpts, optional): Options for creating the client context.
            If not provided, default options for the given mode will be used.

    Returns:
        VertexClient: The created VertexClient instance.
    """
    logging.info(f"Initializing default {mode} context")
    (
        engine_endpoint_url,
        indexer_endpoint_url,
        trigger_endpoint_url,
        network_name,
    ) = client_mode_to_setup(mode)
    try:
        network = VertexNetwork(network_name)
        deployment = load_deployment(network)
        rpc_node_url = deployment.node_url
        contracts_context = VertexContractsContext(
            network=network,
            endpoint_addr=deployment.endpoint_addr,
            querier_addr=deployment.querier_addr,
            perp_engine_addr=deployment.perp_engine_addr,
            spot_engine_addr=deployment.spot_engine_addr,
            clearinghouse_addr=deployment.clearinghouse_addr,
            vrtx_airdrop_addr=deployment.vrtx_airdrop_addr,
            vrtx_staking_addr=deployment.vrtx_staking_addr,
            foundation_rewards_airdrop_addr=deployment.foundation_rewards_airdrop_addr,
        )
    except Exception as e:
        logging.warning(
            f"Failed to load contracts for mode {mode} with error: {e}, using provided defaults."
        )
        assert context_opts is not None and context_opts.rpc_node_url is not None
        assert context_opts is not None and context_opts.contracts_context is not None

        rpc_node_url = context_opts.rpc_node_url
        contracts_context = context_opts.contracts_context

    if context_opts:
        parsed_context_opts: VertexClientContextOpts = (
            VertexClientContextOpts.parse_obj(context_opts)
        )
        engine_endpoint_url = (
            parsed_context_opts.engine_endpoint_url or engine_endpoint_url
        )
        indexer_endpoint_url = (
            parsed_context_opts.indexer_endpoint_url or indexer_endpoint_url
        )
        trigger_endpoint_url = (
            parsed_context_opts.trigger_endpoint_url or trigger_endpoint_url
        )
        rpc_node_url = parsed_context_opts.rpc_node_url or rpc_node_url
        contracts_context = parsed_context_opts.contracts_context or contracts_context

    context = create_vertex_client_context(
        VertexClientContextOpts(
            rpc_node_url=rpc_node_url,
            engine_endpoint_url=parse_obj_as(AnyUrl, engine_endpoint_url),
            indexer_endpoint_url=parse_obj_as(AnyUrl, indexer_endpoint_url),
            trigger_endpoint_url=parse_obj_as(AnyUrl, trigger_endpoint_url),
            contracts_context=contracts_context,
        ),
        signer,
    )
    return VertexClient(context)


def client_mode_to_setup(
    client_mode: VertexClientMode,
) -> tuple[str, str, str, str]:
    try:
        return {
            VertexClientMode.MAINNET: (
                VertexBackendURL.MAINNET_GATEWAY.value,
                VertexBackendURL.MAINNET_INDEXER.value,
                VertexBackendURL.MAINNET_TRIGGER.value,
                VertexNetwork.ARBITRUM_ONE.value,
            ),
            VertexClientMode.BLAST_MAINNET: (
                VertexBackendURL.BLAST_MAINNET_GATEWAY.value,
                VertexBackendURL.BLAST_MAINNET_INDEXER.value,
                VertexBackendURL.BLAST_MAINNET_TRIGGER.value,
                VertexNetwork.BLAST_MAINNET.value,
            ),
            VertexClientMode.MANTLE_MAINNET: (
                VertexBackendURL.MANTLE_MAINNET_GATEWAY.value,
                VertexBackendURL.MANTLE_MAINNET_INDEXER.value,
                VertexBackendURL.MANTLE_MAINNET_TRIGGER.value,
                VertexNetwork.MANTLE_MAINNET.value,
            ),
            VertexClientMode.SEI_MAINNET: (
                VertexBackendURL.SEI_MAINNET_GATEWAY.value,
                VertexBackendURL.SEI_MAINNET_INDEXER.value,
                VertexBackendURL.SEI_MAINNET_TRIGGER.value,
                VertexNetwork.SEI_MAINNET.value,
            ),
            VertexClientMode.BASE_MAINNET: (
                VertexBackendURL.BASE_MAINNET_GATEWAY.value,
                VertexBackendURL.BASE_MAINNET_INDEXER.value,
                VertexBackendURL.BASE_MAINNET_TRIGGER.value,
                VertexNetwork.BASE_MAINNET.value,
            ),
            VertexClientMode.SEPOLIA_TESTNET: (
                VertexBackendURL.SEPOLIA_TESTNET_GATEWAY.value,
                VertexBackendURL.SEPOLIA_TESTNET_INDEXER.value,
                VertexBackendURL.SEPOLIA_TESTNET_TRIGGER.value,
                VertexNetwork.ARBITRUM_SEPOLIA.value,
            ),
            VertexClientMode.BLAST_TESTNET: (
                VertexBackendURL.BLAST_TESTNET_GATEWAY.value,
                VertexBackendURL.BLAST_TESTNET_INDEXER.value,
                VertexBackendURL.BLAST_TESTNET_TRIGGER.value,
                VertexNetwork.BLAST_TESTNET.value,
            ),
            VertexClientMode.MANTLE_TESTNET: (
                VertexBackendURL.MANTLE_TESTNET_GATEWAY.value,
                VertexBackendURL.MANTLE_TESTNET_INDEXER.value,
                VertexBackendURL.MANTLE_TESTNET_TRIGGER.value,
                VertexNetwork.MANTLE_TESTNET.value,
            ),
            VertexClientMode.SEI_TESTNET: (
                VertexBackendURL.SEI_TESTNET_GATEWAY.value,
                VertexBackendURL.SEI_TESTNET_INDEXER.value,
                VertexBackendURL.SEI_TESTNET_TRIGGER.value,
                VertexNetwork.SEI_TESTNET.value,
            ),
            VertexClientMode.BASE_TESTNET: (
                VertexBackendURL.BASE_TESTNET_GATEWAY.value,
                VertexBackendURL.BASE_TESTNET_INDEXER.value,
                VertexBackendURL.BASE_TESTNET_TRIGGER.value,
                VertexNetwork.BASE_TESTNET.value,
            ),
            VertexClientMode.DEVNET: (
                VertexBackendURL.DEVNET_GATEWAY.value,
                VertexBackendURL.DEVNET_INDEXER.value,
                VertexBackendURL.DEVNET_TRIGGER.value,
                VertexNetwork.HARDHAT.value,
            ),
            VertexClientMode.TESTING: (
                VertexBackendURL.DEVNET_GATEWAY.value,
                VertexBackendURL.DEVNET_INDEXER.value,
                VertexBackendURL.DEVNET_TRIGGER.value,
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
