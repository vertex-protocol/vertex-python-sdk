from vertex_protocol.utils.enum import StrEnum


class VertexBackendURL(StrEnum):
    """Enum representing different Vertex backend URLs."""

    MANTLET_TESTNET = "https://api.mantle-test.vertexprotocol.com"
    SEPOLIA_TESTNET = "https://api.sepolia-test.vertexprotocol.com"
    MAINNET = "https://api.prod.vertexprotocol.com"
    DEVNET_ENGINE = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
