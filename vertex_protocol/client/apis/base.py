from vertex_protocol.client.context import VertexClientContext


class BaseVertexAPI:
    """
    The base class for Vertex APIs.
    """

    def __init__(self, context: VertexClientContext):
        """
        Initialize BaseVertexAPI with provided context.
        """
        self.context = context
