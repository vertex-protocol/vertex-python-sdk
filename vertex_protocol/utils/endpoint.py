from enum import Enum


class VertexEndpoint(str, Enum):
    TESTNET = "https://test.vertexprotocol-backend.com"
    MAINNET = "https://prod.vertexprotocol-backend.com"
