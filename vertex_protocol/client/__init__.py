from vertex_protocol.client.apis.market import MarketAPI
from vertex_protocol.client.apis.perp import PerpAPI
from vertex_protocol.client.apis.spot import SpotAPI
from vertex_protocol.client.apis.subaccount import SubaccountAPI
from vertex_protocol.client.context import VertexClientContext


class VertexClient:
    """
    Client for querying and executing against Vertex Clearinghouse.
    """

    def __init__(self, context: VertexClientContext):
        """
        Initialize a new instance of the VertexClient.

        Args:
            context (VertexClientContext): The client context.
        """
        self.context = context
        self.market = MarketAPI(context)
        self.subaccount = SubaccountAPI(context)
        self.spot = SpotAPI(context)
        self.perp = PerpAPI(context)
