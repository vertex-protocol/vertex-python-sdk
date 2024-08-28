from unittest.mock import MagicMock

from eth_account import Account
from vertex_protocol.client import VertexClientMode, create_vertex_client

from vertex_protocol.client.context import (
    VertexClientContextOpts,
    create_vertex_client_context,
)
import pytest
from vertex_protocol.contracts import VertexContractsContext

from vertex_protocol.utils.backend import VertexBackendURL


def test_create_vertex_client_context(
    mock_post: MagicMock,
    mock_web3: MagicMock,
    mock_load_abi: MagicMock,
    private_keys: list[str],
    url: str,
    endpoint_addr: str,
    book_addrs: list[str],
    chain_id: int,
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {
            "endpoint_addr": endpoint_addr,
            "book_addrs": book_addrs,
            "chain_id": chain_id,
        },
    }
    mock_post.return_value = mock_response

    full_engine_client_setup = create_vertex_client_context(
        VertexClientContextOpts(
            engine_endpoint_url=url,
            indexer_endpoint_url=url,
            rpc_node_url=url,
            contracts_context=VertexContractsContext(
                endpoint_addr=endpoint_addr, querier_addr=endpoint_addr
            ),
        ),
        signer=private_keys[0],
    )

    assert full_engine_client_setup.engine_client.chain_id == chain_id
    assert full_engine_client_setup.engine_client.endpoint_addr == endpoint_addr
    assert full_engine_client_setup.engine_client.book_addrs == book_addrs
    assert (
        full_engine_client_setup.engine_client.signer.address
        == Account.from_key(private_keys[0]).address
    )
    assert (
        full_engine_client_setup.engine_client.url
        == full_engine_client_setup.indexer_client.url
        == url
    )

    mock_response.status_code = 400
    mock_response.json.return_value = {
        "status": "failure",
        "data": "invalid request",
    }
    mock_post.return_value = mock_response

    partial_engine_client_setup = create_vertex_client_context(
        VertexClientContextOpts(
            engine_endpoint_url=url,
            indexer_endpoint_url=url,
            rpc_node_url=url,
            contracts_context=VertexContractsContext(
                endpoint_addr=endpoint_addr, querier_addr=endpoint_addr
            ),
        ),
        private_keys[0],
    )

    with pytest.raises(AttributeError, match="Endpoint address not set."):
        partial_engine_client_setup.engine_client.endpoint_addr

    with pytest.raises(AttributeError, match="Book addresses are not set."):
        partial_engine_client_setup.engine_client.book_addrs

    with pytest.raises(AttributeError, match="Chain ID is not set."):
        partial_engine_client_setup.engine_client.chain_id

    assert (
        partial_engine_client_setup.engine_client.signer.address
        == Account.from_key(private_keys[0]).address
    )
    assert (
        partial_engine_client_setup.engine_client.url
        == partial_engine_client_setup.indexer_client.url
        == url
    )


def test_create_vertex_client(
    mock_post: MagicMock,
    mock_web3: MagicMock,
    mock_load_abi: MagicMock,
    private_keys: list[str],
    url: str,
    endpoint_addr: str,
    book_addrs: list[str],
    chain_id: int,
    contracts_context: VertexContractsContext,
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {
            "endpoint_addr": endpoint_addr,
            "book_addrs": book_addrs,
            "chain_id": chain_id,
        },
    }
    mock_post.return_value = mock_response

    signer = Account.from_key(private_keys[0])
    mainnet_vertex_client = create_vertex_client(VertexClientMode.MAINNET, signer)

    assert mainnet_vertex_client.context.engine_client.chain_id == chain_id
    assert mainnet_vertex_client.context.engine_client.endpoint_addr == endpoint_addr
    assert mainnet_vertex_client.context.engine_client.book_addrs == book_addrs
    assert (
        mainnet_vertex_client.context.engine_client.url
        == VertexBackendURL.MAINNET_GATEWAY
    )
    assert (
        mainnet_vertex_client.context.indexer_client.url
        == VertexBackendURL.MAINNET_INDEXER
    )
    assert mainnet_vertex_client.context.engine_client.signer == signer

    sepolia_testnet_vertex_client = create_vertex_client(
        VertexClientMode.SEPOLIA_TESTNET, signer
    )

    assert sepolia_testnet_vertex_client.context.engine_client.chain_id == chain_id
    assert (
        sepolia_testnet_vertex_client.context.engine_client.endpoint_addr
        == endpoint_addr
    )
    assert sepolia_testnet_vertex_client.context.engine_client.book_addrs == book_addrs
    assert (
        sepolia_testnet_vertex_client.context.engine_client.url
        == VertexBackendURL.SEPOLIA_TESTNET_GATEWAY
    )
    assert (
        sepolia_testnet_vertex_client.context.indexer_client.url
        == VertexBackendURL.SEPOLIA_TESTNET_INDEXER
    )
    assert sepolia_testnet_vertex_client.context.engine_client.signer == signer

    devnet_vertex_client = create_vertex_client(VertexClientMode.TESTING, signer)

    assert devnet_vertex_client.context.engine_client.chain_id == chain_id
    assert devnet_vertex_client.context.engine_client.endpoint_addr == endpoint_addr
    assert devnet_vertex_client.context.engine_client.book_addrs == book_addrs
    assert (
        devnet_vertex_client.context.engine_client.url
        == VertexBackendURL.DEVNET_GATEWAY
    )
    assert (
        devnet_vertex_client.context.indexer_client.url
        == VertexBackendURL.DEVNET_INDEXER
    )
    assert devnet_vertex_client.context.engine_client.signer == signer

    with pytest.raises(Exception, match="Mode provided `custom` not supported!"):
        create_vertex_client("custom", signer)

    custom_vertex_client = create_vertex_client(
        VertexClientMode.TESTING,
        signer,
        VertexClientContextOpts(
            engine_endpoint_url=url,
            indexer_endpoint_url=url,
            rpc_node_url=url,
            contracts_context=contracts_context,
        ),
    )

    assert custom_vertex_client.context.engine_client.url == url
    assert custom_vertex_client.context.indexer_client.url == url
