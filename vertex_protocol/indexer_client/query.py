from vertex_protocol.indexer_client.types import IndexerClientOpts
from vertex_protocol.indexer_client.types.query import IndexerRequest, IndexerResponse


class IndexerQueryClient:
    def __init__(self, opts: IndexerClientOpts):
        """
        Initialize EngineQueryClient with provided options
        """
        self._opts = IndexerClientOpts.parse_obj(opts)
        self.url = self._opts.url

    def query(self, req: IndexerRequest) -> IndexerResponse:
        pass
