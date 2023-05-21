from vertex_protocol.engine_client import EngineClientOpts


class EngineQueryClient:
    def __init__(self, opts: EngineClientOpts):
        """
        Initialize EngineQueryClient with provided options
        """
        self._opts = EngineClientOpts.parse_obj(opts)
        self.url = self._opts.url
