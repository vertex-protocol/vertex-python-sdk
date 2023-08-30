from vertex_protocol.engine_client.types.execute import (
    BurnLpParams,
    CancelAndPlaceParams,
    CancelOrdersParams,
    CancelProductOrdersParams,
    ExecuteResponse,
    MintLpParams,
    PlaceMarketOrderParams,
    PlaceOrderParams,
)
from vertex_protocol.client.apis.base import VertexBaseAPI
from vertex_protocol.utils.subaccount import Subaccount


class MarketExecuteAPI(VertexBaseAPI):
    """
    Provides functionality to interact with the Vertex's market execution APIs.
    This class contains methods that allow clients to execute operations such as minting LP tokens, burning LP tokens,
    placing and cancelling orders on the Vertex market.

    Attributes:
        context (VertexClientContext): The context that provides connectivity configuration for VertexClient.

    Note:
        This class should not be instantiated directly, it is designed to be used through a VertexClient instance.
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

    def place_market_order(self, params: PlaceMarketOrderParams) -> ExecuteResponse:
        """
        Places a market order through the engine.

        Args:
            params (PlaceMarketOrderParams): Parameters required to place a market order.

        Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.place_market_order(params)

    def cancel_orders(self, params: CancelOrdersParams) -> ExecuteResponse:
        """
        Cancels orders through the engine.

        Args:
            params (CancelOrdersParams): Parameters required to cancel orders.

        Returns:
            ExecuteResponse: The response from the engine execution containing information about the canceled product orders.

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
            ExecuteResponse: The response from the engine execution containing information about the canceled product orders.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.cancel_product_orders(params)

    def cancel_and_place(self, params: CancelAndPlaceParams) -> ExecuteResponse:
        """
        Cancels orders and places a new one through the engine on the same request.

        Args:
            params (CancelAndPlaceParams): Parameters required to cancel orders and place a new one.

        Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.cancel_and_place(params)

    def close_position(
        self, subaccount: Subaccount, product_id: int
    ) -> ExecuteResponse:
        """
        Places an order through the engine to close a position for the provided `product_id`.

        Attributes:
            subaccount (Subaccount): The subaccount to close position for.
            product_id (int): The ID of the product to close position for.

         Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.close_position(subaccount, product_id)
