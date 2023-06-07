from web3.contract import Contract
from vertex_protocol.client.apis.base import VertexBaseAPI


class BaseSpotAPI(VertexBaseAPI):
    """
    Base class for Spot operations in the Vertex Protocol.

    This class provides basic functionality for retrieving product-specific information
    from the spot market of the Vertex Protocol, such as the associated ERC20 token contract for a given spot product.

    Attributes:
        context (VertexClientContext): Provides connectivity details for accessing Vertex APIs.

    Methods:
        get_token_contract_for_product: Retrieves the associated ERC20 token contract for a given spot product.
    """

    def get_token_contract_for_product(self, product_id: int) -> Contract:
        """
        Retrieves the associated ERC20 token contract for a given spot product.

        Args:
            product_id (int): The identifier for the spot product.

        Returns:
            Contract: The associated ERC20 token contract for the specified spot product.

        Raises:
            InvalidProductId: If the provided product ID is not valid.
        """
        return self.context.contracts.get_token_contract_for_product(product_id)
