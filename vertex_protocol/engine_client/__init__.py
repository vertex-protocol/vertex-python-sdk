from vertex_protocol.engine_client.types import EngineClientOpts
from vertex_protocol.engine_client.execute import EngineExecuteClient
from vertex_protocol.engine_client.query import EngineQueryClient


class EngineClient(EngineQueryClient, EngineExecuteClient):
    def __init__(self, opts: EngineClientOpts):
        """
        Initialize EngineClient with provided options
        """
        EngineQueryClient.__init__(self, opts)
        EngineExecuteClient.__init__(self, opts)
