from vertex_protocol.trigger_client.types import TriggerClientOpts
from vertex_protocol.utils.execute import BaseExecuteClient


class TriggerExecuteClient(BaseExecuteClient):
    def __init__(self, opts: TriggerClientOpts):
        super().__init__(opts)
        self._opts: TriggerClientOpts = TriggerClientOpts.parse_obj(opts)
