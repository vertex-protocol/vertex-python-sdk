from web3.contract import Contract
from vertex_protocol.client.apis.base import VertexBaseAPI


class BaseSpotAPI(VertexBaseAPI):
    def get_token_contract_for_product(self, product_id: int) -> Contract:
        """
        Retrieves the associated ERC20 token contract for a given spot product.

        Args:
            product_id (int): The identifier for the spot product.

        Returns:
            Contract: The associated ERC20 token contract for the specified spot product.
        """
        return self.context.contracts.get_token_contract_for_product(product_id)
