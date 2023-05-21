from .context import VertexClientContext


class VertexClient:
    """
    Client for querying and executing against Vertex Clearinghouse.
    Usually not instantiated directly. Instead, use `create_vertex_client` function.
    """

    def __init__(self, context: VertexClientContext):
        """
        Initialize a new instance of the VertexClient.

        Args:
            context (VertexClientContext): The client context.
        """
        pass
