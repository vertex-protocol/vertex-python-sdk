from enum import StrEnum


class VertexBackendURL(StrEnum):
    """Enum representing different Vertex backend URLs.

    The enum has the following values:
    TESTNET: URL for the testnet backend.
    MAINNET: URL for the mainnet backend.
    DEVNET_ENGINE: URL for the development engine.
    DEVNET_INDEXER: URL for the development indexer.

    Each enum value is a string representing the respective backend URL.
    """

    TESTNET = "https://test.vertexprotocol-backend.com"
    MAINNET = "https://prod.vertexprotocol-backend.com"
    DEVNET_ENGINE = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
