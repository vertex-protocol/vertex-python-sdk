import os
from dotenv import load_dotenv
from vertex_protocol.client import VertexClientMode

from vertex_protocol.contracts.types import VertexNetwork
from vertex_protocol.utils.backend import VertexBackendURL

load_dotenv()

NETWORK = VertexNetwork.ARBITRUM_GOERLI
ENGINE_BACKEND_URL = VertexBackendURL.TESTNET
INDEXER_BACKEND_URL = VertexBackendURL.TESTNET
CLIENT_MODE = VertexClientMode.TESTNET

SIGNER_PRIVATE_KEY = os.getenv("SIGNER_PRIVATE_KEY")
LINKED_SIGNER_PRIVATE_KEY = os.getenv("LINKED_SIGNER_PRIVATE_KEY")
