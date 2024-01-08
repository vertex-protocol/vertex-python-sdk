from unittest.mock import MagicMock, patch
from eth_account import Account
import pytest
import requests
from vertex_protocol.client import VertexClient, create_vertex_client
from vertex_protocol.contracts import VertexContractsContext
from vertex_protocol.engine_client import EngineClient
from vertex_protocol.engine_client.types import EngineClientOpts

from vertex_protocol.utils.bytes32 import hex_to_bytes32


@pytest.fixture
def url() -> str:
    return "http://example.com"


@pytest.fixture
def private_keys() -> list[str]:
    return [
        "0x45917429615b8a68cd372c96f63092f3d672a0bc60202b188670354b89c43ae3",
        "0x4c9ce2e6c4f38c801410a8603350108f2ac23a6f7cf6217a946c216ec0ec3bec",
    ]


@pytest.fixture
def chain_id() -> int:
    return 1337


@pytest.fixture
def endpoint_addr() -> str:
    return "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6"


@pytest.fixture
def owners() -> list[str]:
    return [
        "0xBE3faCAE76A38c3b61492E57BF65ae0628c4A808",
        "0xd1914656F48102b6eF086b4dc33f748F9D12A6F8",
    ]


@pytest.fixture
def senders() -> list[str]:
    return [
        "0xBE3faCAE76A38c3b61492E57BF65ae0628c4A80864656661756c740000000000",
        "0xd1914656F48102b6eF086b4dc33f748F9D12A6F864656661756c740000000000",
    ]


@pytest.fixture
def book_addrs() -> list[str]:
    return [
        "0x0000000000000000000000000000000000000000",
        "0x5FbDB2315678afecb367f032d93F642f64180aa3",
        "0x59b670e9fA9D0A427751Af201D676719a970857b",
        "0x610178dA211FEF7D417bC0e6FeD39F05609AD788",
        "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9",
    ]


@pytest.fixture
def engine_client(
    url: str,
    chain_id: int,
    endpoint_addr: str,
    book_addrs: list[str],
    private_keys: list[str],
) -> EngineClient:
    return EngineClient(
        opts=EngineClientOpts(
            url=url,
            chain_id=chain_id,
            endpoint_addr=endpoint_addr,
            book_addrs=book_addrs,
            signer=Account.from_key(private_keys[0]),
            linked_signer=Account.from_key(private_keys[1]),
        )
    )


@pytest.fixture
def vertex_client(
    mock_get: MagicMock,
    chain_id: int,
    endpoint_addr: str,
    book_addrs: list[str],
    private_keys: list[str],
) -> VertexClient:
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
    mock_get.return_value = mock_response
    return create_vertex_client("testing", private_keys[0])


@pytest.fixture
def order_params(senders: list[str]) -> dict:
    return {
        "sender": hex_to_bytes32(senders[0]),
        "priceX18": 28898000000000000000000,
        "amount": -10000000000000000,
        "expiration": 4611687701117784255,
        "nonce": 1764428860167815857,
    }


@pytest.fixture
def cancellation_params(senders: str) -> dict:
    return {
        "sender": hex_to_bytes32(senders[0]),
        "productIds": [4],
        "digests": [
            hex_to_bytes32(
                "0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"
            )
        ],
        "nonce": 1,
    }


@pytest.fixture
def cancellation_products_params(senders: list[str]) -> dict:
    return {
        "sender": hex_to_bytes32(senders[0]),
        "productIds": [2, 4],
        "nonce": 1,
    }


@pytest.fixture
def withdraw_collateral_params(senders: list[str]) -> dict:
    return {
        "sender": hex_to_bytes32(senders[0]),
        "productId": 2,
        "amount": 10000000000000000,
        "nonce": 1,
    }


@pytest.fixture
def liquidate_subaccount_params(senders: list[str]) -> dict:
    return {
        "sender": hex_to_bytes32(senders[0]),
        "liquidatee": hex_to_bytes32(senders[1]),
        "mode": 0,
        "healthGroup": 1,
        "amount": 10000000000000000,
        "nonce": 1,
    }


@pytest.fixture
def mint_lp_params(senders: list[str]) -> dict:
    return {
        "sender": hex_to_bytes32(senders[0]),
        "productId": 1,
        "amountBase": 1000000000000000000,
        "quoteAmountLow": 20000000000000000000000,
        "quoteAmountHigh": 40000000000000000000000,
        "nonce": 1,
    }


@pytest.fixture
def burn_lp_params(senders: list[str]) -> dict:
    return {
        "sender": hex_to_bytes32(senders[0]),
        "productId": 1,
        "amount": 1000000000000000000,
        "nonce": 1,
    }


@pytest.fixture
def link_signer_params(senders: list[str]) -> dict:
    return {
        "sender": hex_to_bytes32(senders[0]),
        "signer": hex_to_bytes32(senders[1]),
        "nonce": 1,
    }


@pytest.fixture
def mock_post() -> MagicMock:
    with patch.object(requests.Session, "post") as mock_post:
        yield mock_post


@pytest.fixture
def mock_get() -> MagicMock:
    with patch.object(requests.Session, "get") as mock_post:
        yield mock_post


@pytest.fixture
def mock_web3() -> MagicMock:
    with patch("vertex_protocol.contracts.Web3") as mock_web3:
        yield mock_web3


@pytest.fixture
def mock_load_abi() -> MagicMock:
    with patch("vertex_protocol.contracts.load_abi") as mock_load_abi:
        yield mock_load_abi


@pytest.fixture
def mock_execute_response(mock_post: MagicMock) -> MagicMock:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "error": None,
    }
    mock_post.return_value = mock_response
    return mock_post


@pytest.fixture
def mock_place_order_response(mock_post: MagicMock) -> MagicMock:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "error": None,
        "data": {"digest": "0x123"},
    }
    mock_post.return_value = mock_response
    return mock_post


@pytest.fixture
def mock_cancel_orders_response(mock_post: MagicMock) -> MagicMock:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "error": None,
        "data": {
            "cancelled_orders": [
                {
                    "product_id": 1,
                    "sender": 1,
                    "price_x18": 2.8898e22,
                    "amount": -10000000000000000,
                    "expiration": 4611687701117784000,
                    "nonce": 1,
                    "unfilled_amount": -10000000000000000,
                    "digest": "0x8efa3736d834718f755b57cee9ba75db315f66c66844150bd15efd641e62e9e6",
                    "placed_at": "1686629287",
                }
            ]
        },
    }
    mock_post.return_value = mock_response
    return mock_post


@pytest.fixture
def mock_nonces(mock_get: MagicMock) -> MagicMock:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {"tx_nonce": 1, "order_nonce": 1},
    }
    mock_get.return_value = mock_response
    return mock_get


@pytest.fixture
def contracts_context(endpoint_addr: str, book_addrs: str) -> VertexContractsContext:
    return VertexContractsContext(
        endpoint_addr=endpoint_addr, querier_addr=book_addrs[1]
    )
