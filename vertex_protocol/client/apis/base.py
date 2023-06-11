from vertex_protocol.client.context import VertexClientContext


class VertexBaseAPI:
    """
    The base class for all Vertex API classes, providing the foundation for API-specific classes in the Vertex client.

    VertexBaseAPI serves as a foundation for the hierarchical structure of the Vertex API classes. This structure allows for better
    organization and separation of concerns, with each API-specific subclass handling a different aspect of the Vertex client's functionality.

    Attributes:
        context (VertexClientContext): The context in which the API operates, providing access to the client's state and services.

    Note:
        This class is not meant to be used directly. It provides base functionality for other API classes in the Vertex client.
    """

    context: VertexClientContext

    def __init__(self, context: VertexClientContext):
        """
        Initialize an instance of VertexBaseAPI.

        VertexBaseAPI requires a context during instantiation, which should be an instance of VertexClientContext. This context
        provides access to the state and services of the Vertex client and allows the API to interact with these.

        Args:
            context (VertexClientContext): The context in which this API operates. Provides access to the state and services
            of the Vertex client.
        """
        self.context = context
