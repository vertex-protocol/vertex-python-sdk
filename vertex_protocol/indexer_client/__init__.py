from vertex_protocol.indexer_client.query import IndexerQueryClient
from vertex_protocol.indexer_client.types import IndexerClientOpts


class IndexerClient(IndexerQueryClient):
    def __init__(self, opts: IndexerClientOpts):
        super().__init__(opts)
