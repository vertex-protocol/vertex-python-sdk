from vertex_protocol.utils.enum import StrEnum


class VertexBackendURL(StrEnum):
    """Enum representing different Vertex backend URLs."""

    SEPOLIA_TESTNET_GATEWAY = "https://gateway.sepolia-test.vertexprotocol.com/v1"
    SEPOLIA_TESTNET_INDEXER = "https://archive.sepolia-test.vertexprotocol.com/v1"

    MAINNET_GATEWAY = "https://gateway.prod.vertexprotocol.com/v1"
    MAINNET_INDEXER = "https://archive.prod.vertexprotocol.com/v1"

    BLAST_MAINNET_GATEWAY = "https://gateway.blast-prod.vertexprotocol.com/v1"
    BLAST_MAINNET_INDEXER = "https://archive.blast-prod.vertexprotocol.com/v1"

    DEVNET_GATEWAY = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
