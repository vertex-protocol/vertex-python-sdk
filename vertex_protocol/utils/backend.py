from vertex_protocol.utils.enum import StrEnum


class VertexBackendURL(StrEnum):
    """Enum representing different Vertex backend URLs."""

    MAINNET_GATEWAY = "https://gateway.prod.vertexprotocol.com/v1"
    MAINNET_INDEXER = "https://archive.prod.vertexprotocol.com/v1"

    BLAST_MAINNET_GATEWAY = "https://gateway.blast-prod.vertexprotocol.com/v1"
    BLAST_MAINNET_INDEXER = "https://archive.blast-prod.vertexprotocol.com/v1"

    MANTLE_MAINNET_GATEWAY = "https://gateway.mantle-prod.vertexprotocol.com/v1"
    MANTLE_MAINNET_INDEXER = "https://archive.mantle-prod.vertexprotocol.com/v1"

    SEI_MAINNET_GATEWAY = "https://gateway.sei-prod.vertexprotocol.com/v1"
    SEI_MAINNET_INDEXER = "https://archive.sei-prod.vertexprotocol.com/v1"

    BASE_MAINNET_GATEWAY = "https://gateway.base-prod.vertexprotocol.com/v1"
    BASE_MAINNET_INDEXER = "https://archive.base-prod.vertexprotocol.com/v1"

    SEPOLIA_TESTNET_GATEWAY = "https://gateway.sepolia-test.vertexprotocol.com/v1"
    SEPOLIA_TESTNET_INDEXER = "https://archive.sepolia-test.vertexprotocol.com/v1"

    BLAST_TESTNET_GATEWAY = "https://gateway.blast-test.vertexprotocol.com/v1"
    BLAST_TESTNET_INDEXER = "https://archive.blast-test.vertexprotocol.com/v1"

    MANTLE_TESTNET_GATEWAY = "https://gateway.mantle-test.vertexprotocol.com/v1"
    MANTLE_TESTNET_INDEXER = "https://archive.mantle-test.vertexprotocol.com/v1"

    SEI_TESTNET_GATEWAY = "https://gateway.sei-test.vertexprotocol.com/v1"
    SEI_TESTNET_INDEXER = "https://archive.sei-test.vertexprotocol.com/v1"

    BASE_TESTNET_GATEWAY = "https://gateway.base-test.vertexprotocol.com/v1"
    BASE_TESTNET_INDEXER = "https://archive.base-test.vertexprotocol.com/v1"

    DEVNET_GATEWAY = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
