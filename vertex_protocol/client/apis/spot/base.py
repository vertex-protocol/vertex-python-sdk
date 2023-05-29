from vertex_protocol.client.apis.base import VertexBaseAPI


class BaseSpotAPI(VertexBaseAPI):
    def get_token_contract_for_product(self, product_id: int):
        """
        Placeholder for a function to retrieve the associated token contract for a given spot product.

        Args:
            product_id (int): The identifier for the spot product.

        Raises:
            NotImplementedError: This function is not yet implemented.
        """
        raise NotImplementedError("This function is not yet implemented")
