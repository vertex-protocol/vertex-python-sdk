from vertex_protocol.client.context import VertexClientContext


class VertexBaseAPI:
    """
    The base class for Vertex APIs.
    """

    def __init__(self, context: VertexClientContext):
        """
        Initialize VertexBaseAPI with provided context.
        """
        self.context = context
