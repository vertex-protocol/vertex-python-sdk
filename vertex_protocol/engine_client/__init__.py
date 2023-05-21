from .types import EngineClientOpts
from .execute import EngineExecuteClient
from .query import EngineQueryClient


class EngineClient(EngineQueryClient, EngineExecuteClient):
    def __init__(self, opts: EngineClientOpts):
        """
        Initialize EngineClient with provided options
        """
        EngineQueryClient.__init__(self, opts)
        EngineExecuteClient.__init__(self, opts)
