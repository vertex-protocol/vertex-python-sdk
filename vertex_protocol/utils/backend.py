from vertex_protocol.utils.enum import StrEnum


class VertexBackendURL(StrEnum):
    """Enum representing different Vertex backend URLs."""

    ARBITRUM_GATEWAY = "https://gateway.prod.vertexprotocol.com/v1"
    ARBITRUM_INDEXER = "https://archive.prod.vertexprotocol.com/v1"

    ARBITRUM_SEPOLIA_GATEWAY = "https://gateway.sepolia-test.vertexprotocol.com/v1"
    ARBITRUM_SEPOLIA_INDEXER = "https://archive.sepolia-test.vertexprotocol.com/v1"

    BLAST_GATEWAY = "https://gateway.blast-prod.vertexprotocol.com/v1"
    BLAST_INDEXER = "https://archive.blast-prod.vertexprotocol.com/v1"

    BLAST_SEPOLIA_GATEWAY = "https://gateway.blast-test.vertexprotocol.com/v1"
    BLAST_SEPOLIA_INDEXER = "https://archive.blast-test.vertexprotocol.com/v1"

    MANTLE_GATEWAY = "https://gateway.mantle-prod.vertexprotocol.com/v1"
    MANTLE_INDEXER = "https://archive.mantle-prod.vertexprotocol.com/v1"

    MANTLE_SEPOLIA_GATEWAY = "https://gateway.mantle-test.vertexprotocol.com/v1"
    MANTLE_SEPOLIA_INDEXER = "https://archive.mantle-test.vertexprotocol.com/v1"

    DEVNET_GATEWAY = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
