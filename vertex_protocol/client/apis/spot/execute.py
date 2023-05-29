from vertex_protocol.client.apis.spot.base import BaseSpotAPI
from vertex_protocol.engine_client.types.execute import (
    ExecuteResponse,
    WithdrawCollateralParams,
)


class SpotExecuteAPI(BaseSpotAPI):
    def deposit(self):
        """
        Placeholder for a function to deposit a specified amount into a spot product.

        Raises:
            NotImplementedError: This function is not yet implemented.
        """
        raise NotImplementedError("This function is not yet implemented")

    def withdraw(self, params: WithdrawCollateralParams) -> ExecuteResponse:
        """
        Executes a withdrawal for the specified spot product via the off-chain engine.

        Args:
            params (WithdrawCollateralParams): Parameters needed to execute the withdrawal.

        Returns:
            ExecuteResponse: The response from the engine execution.

        Raises:
            Exception: If there is an error during the execution or the response status is not "success".
        """
        return self.context.engine_client.withdraw_collateral(params)

    def approve_allowance(self):
        """
        Placeholder for a function to approve an allowance for a certain amount of tokens for a spot product.

        Raises:
            NotImplementedError: This function is not yet implemented.
        """
        raise NotImplementedError("This function is not yet implemented")

    def _mint_mock_erc20(self):
        """
        Placeholder for a function to mint a specified amount of mock ERC20 tokens for testing purposes.

        Raises:
            NotImplementedError: This function is not yet implemented.
        """
        raise NotImplementedError("This function is not yet implemented")
