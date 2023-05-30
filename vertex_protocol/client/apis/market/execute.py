from vertex_protocol.engine_client.types.execute import (
    BurnLpParams,
    CancelOrdersParams,
    CancelProductOrdersParams,
    ExecuteResponse,
    MintLpParams,
    PlaceOrderParams,
)
from vertex_protocol.client.apis.base import VertexBaseAPI


class MarketExecuteAPI(VertexBaseAPI):
    """
    Provides market execution APIs.
    """

    def mint_lp(self, params: MintLpParams) -> ExecuteResponse:
        """
        Mint LP tokens through the engine.

        Args:
            params (MintLpParams): Parameters required to mint LP tokens.

        Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.mint_lp(params)

    def burn_lp(self, params: BurnLpParams) -> ExecuteResponse:
        """
        Burn LP tokens through the engine.

        Args:
            params (BurnLpParams): Parameters required to burn LP tokens.

        Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.burn_lp(params)

    def place_order(self, params: PlaceOrderParams) -> ExecuteResponse:
        """
        Places an order through the engine.

        Args:
            params (PlaceOrderParams): Parameters required to place an order.

        Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.place_order(params)

    def cancel_orders(self, params: CancelOrdersParams) -> ExecuteResponse:
        """
        Cancels orders through the engine.

        Args:
            params (CancelOrdersParams): Parameters required to cancel orders.

        Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.cancel_orders(params)

    def cancel_product_orders(
        self, params: CancelProductOrdersParams
    ) -> ExecuteResponse:
        """
        Cancels all orders for provided products through the engine.

        Args:
            params (CancelProductOrdersParams): Parameters required to cancel product orders.

                Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.cancel_product_orders(params)
