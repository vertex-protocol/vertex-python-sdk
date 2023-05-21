import pytest


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
