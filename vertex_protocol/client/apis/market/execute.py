from vertex_protocol.engine_client.types.execute import (
    BurnLpParams,
    CancelOrdersParams,
    CancelProductOrdersParams,
    ExecuteResponse,
    MintLpParams,
    PlaceOrderParams,
)
from vertex_protocol.client.apis.base import BaseVertexAPI


class MarketExecuteAPI(BaseVertexAPI):
    """
    Provides market execution APIs.
    """

    async def mint_lp(self, params: MintLpParams) -> ExecuteResponse:
        """
        Mint LP tokens through the engine.

        Args:
            params: Parameters required to mint LP tokens.

        Returns:
            The response from the engine client.
        """
        return self.context.engine_client.mint_lp(params)

    async def burn_lp(self, params: BurnLpParams) -> ExecuteResponse:
        """
        Burn LP tokens through the engine.

        Args:
            params: Parameters required to burn LP tokens.

        Returns:
            The response from the engine client.
        """
        return self.context.engine_client.burn_lp(params)

    async def place_order(self, params: PlaceOrderParams) -> ExecuteResponse:
        """
        Places an order through the engine.

        Args:
            params: Parameters required to place an order.

        Returns:
            The response from the engine client.
        """
        return self.context.engine_client.place_order(params)

    async def cancel_orders(self, params: CancelOrdersParams) -> ExecuteResponse:
        """
        Cancels orders through the engine.

        Args:
            params: Parameters required to cancel orders.

        Returns:
            The response from the engine client.
        """
        return self.context.engine_client.cancel_orders(params)

    async def cancel_product_orders(
        self, params: CancelProductOrdersParams
    ) -> ExecuteResponse:
        """
        Cancels all orders for provided products through the engine.

        Args:
            params: Parameters required to cancel product orders.

        Returns:
            The response from the engine client.
        """
        return self.context.engine_client.cancel_product_orders(params)
