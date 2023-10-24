from vertex_protocol.utils.enum import StrEnum


class VertexBackendURL(StrEnum):
    """Enum representing different Vertex backend URLs."""

    TESTNET = "https://api.test.vertexprotocol.com"
    MAINNET = "https://api.prod.vertexprotocol.com"
    DEVNET_ENGINE = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
