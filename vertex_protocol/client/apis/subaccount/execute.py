from vertex_protocol.client.apis.base import VertexBaseAPI
from vertex_protocol.engine_client.types.execute import (
    ExecuteResponse,
    LinkSignerParams,
    LiquidateSubaccountParams,
)


class SubaccountExecuteAPI(VertexBaseAPI):
    """
    Provides functionalities for executing operations related to subaccounts in the Vertex Protocol.

    Inherits from VertexBaseAPI, which provides a basic context setup for accessing Vertex.
    This class extends the base class to provide specific functionalities for executing actions related to subaccounts.

    The provided methods include:
    - `liquidate_subaccount`: Performs the liquidation of a subaccount.
    - `link_signer`: Links a signer to a subaccount, granting them transaction signing permissions.

    Attributes:
        context (VertexClientContext): Provides connectivity details for accessing Vertex APIs.
    """

    def liquidate_subaccount(
        self, params: LiquidateSubaccountParams
    ) -> ExecuteResponse:
        """
        Liquidates a subaccount through the engine.

        Args:
            params (LiquidateSubaccountParams): Parameters for liquidating the subaccount.

        Returns:
            ExecuteResponse: Execution response from the engine.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.liquidate_subaccount(params)

    def link_signer(self, params: LinkSignerParams) -> ExecuteResponse:
        """
        Links a signer to a subaccount to allow them to sign transactions on behalf of the subaccount.

        Args:
            params (LinkSignerParams): Parameters for linking a signer to a subaccount.

        Returns:
            ExecuteResponse: Execution response from the engine.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.link_signer(params)
