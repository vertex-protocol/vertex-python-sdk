import requests
from vertex_protocol.trigger_client.types import TriggerClientOpts


class TriggerQueryClient:
    """
    Client class for querying the trigger service.
    """

    def __init__(self, opts: TriggerClientOpts):
        self._opts: TriggerClientOpts = TriggerClientOpts.parse_obj(opts)
        self.url: str = self._opts.url
        self.session = requests.Session()  # type: ignore
