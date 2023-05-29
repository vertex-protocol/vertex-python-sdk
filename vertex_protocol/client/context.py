from dataclasses import dataclass
from vertex_protocol.contracts import VertexContracts

from vertex_protocol.engine_client import EngineClient
from vertex_protocol.indexer_client import IndexerClient


@dataclass
class VertexClientContext:
    """
    Context required to use the Vertex client.
    """

    engine_client: EngineClient
    indexer_client: IndexerClient
    contracts: VertexContracts
