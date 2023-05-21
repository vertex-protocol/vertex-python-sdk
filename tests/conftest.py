import pytest

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
def chain_id() -> str:
    return 1337


@pytest.fixture
def endpoint_addr() -> str:
    return "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6"


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
def order_params() -> dict:
    return {
        "sender": hex_to_bytes32(
            "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000"
        ),
        "priceX18": 28898000000000000000000,
        "amount": -10000000000000000,
        "expiration": 4611687701117784255,
        "nonce": 1764428860167815857,
    }


@pytest.fixture
def cancellation_params() -> dict:
    return {
        "sender": hex_to_bytes32(
            "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000"
        ),
        "productIds": [4],
        "digests": [
            hex_to_bytes32(
                "0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"
            )
        ],
        "nonce": 1,
    }


@pytest.fixture
def cancellation_products_params() -> dict:
    return {
        "sender": hex_to_bytes32(
            "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000"
        ),
        "productIds": [2, 4],
        "nonce": 1,
    }


@pytest.fixture
def withdraw_collateral_params() -> dict:
    return {
        "sender": hex_to_bytes32(
            "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000"
        ),
        "productId": 2,
        "amount": 10000000000000000,
        "nonce": 1,
    }


@pytest.fixture
def liquidate_subaccount_params() -> dict:
    return {
        "sender": hex_to_bytes32(
            "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000"
        ),
        "liquidatee": hex_to_bytes32(
            "0x12a0b4888021576eb10a67616dd3dd3d9ce206b664656661756c740000000000"
        ),
        "mode": 0,
        "healthGroup": 1,
        "amount": 10000000000000000,
        "nonce": 1,
    }


@pytest.fixture
def mint_lp_params() -> dict:
    return {
        "sender": hex_to_bytes32(
            "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000"
        ),
        "productId": 1,
        "amountBase": 1000000000000000000,
        "quoteAmountLow": 20000000000000000000000,
        "quoteAmountHigh": 40000000000000000000000,
        "nonce": 1,
    }


@pytest.fixture
def burn_lp_params() -> dict:
    return {
        "sender": hex_to_bytes32(
            "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000"
        ),
        "productId": 1,
        "amount": 1000000000000000000,
        "nonce": 1,
    }


@pytest.fixture
def link_signer_params() -> dict:
    return {
        "sender": hex_to_bytes32(
            "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000"
        ),
        "signer": hex_to_bytes32(
            "0x12a0b4888021576eb10a67616dd3dd3d9ce206b664656661756c740000000000"
        ),
        "nonce": 1,
    }
