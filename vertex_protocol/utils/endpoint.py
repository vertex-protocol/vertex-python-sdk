from enum import Enum


class VertexEndpoint(str, Enum):
    TESTNET = "https://test.vertexprotocol-backend.com"
    MAINNET = "https://prod.vertexprotocol-backend.com"
    DEVNET_ENGINE = "http://localhost:80"
    DEVNET_INDEXER = "http://localhost:8000"
