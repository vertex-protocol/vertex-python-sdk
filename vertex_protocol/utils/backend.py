from vertex_protocol.utils.enum import StrEnum


class VertexBackendURL(StrEnum):
    """Enum representing different Vertex backend URLs."""

    TESTNET = "https://test.vertexprotocol-backend.com"
    MAINNET = "https://prod.vertexprotocol-backend.com"
    DEVNET_ENGINE = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
