from ..base import BaseVertexAPI


class MarketExecuteAPI(BaseVertexAPI):
    """
    Provides market execution APIs.
    """

    async def mint_lp(self, params):
        """
        Mint LP tokens through the engine.

        Args:
            params: Parameters required to mint LP tokens.

        Returns:
            The response from the engine client.
        """
        pass

    async def burn_lp(self, params):
        """
        Burn LP tokens through the engine.

        Args:
            params: Parameters required to burn LP tokens.

        Returns:
            The response from the engine client.
        """
        pass

    async def place_order(self, params):
        """
        Places an order through the engine.

        Args:
            params: Parameters required to place an order.

        Returns:
            The response from the engine client.
        """
        pass

    async def cancel_orders(self, params):
        """
        Cancels orders through the engine.

        Args:
            params: Parameters required to cancel orders.

        Returns:
            The response from the engine client.
        """
        pass

    async def cancel_product_orders(self, params):
        """
        Cancels all orders for provided products through the engine.

        Args:
            params: Parameters required to cancel product orders.

        Returns:
            The response from the engine client.
        """
        pass
