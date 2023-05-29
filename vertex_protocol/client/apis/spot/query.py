from vertex_protocol.client.apis.spot.base import BaseSpotAPI
from vertex_protocol.engine_client.types.query import MaxWithdrawableData


class SpotQueryAPI(BaseSpotAPI):
    def get_max_withdrawable(
        self, product_id: int, sender: str, spot_leverage: bool = None
    ) -> MaxWithdrawableData:
        """
        Retrieves the estimated maximum withdrawable amount for a provided spot product.

        Args:
            product_id (int): The identifier for the spot product.
            sender (str): The address and subaccount identifier in a bytes32 hex string.
            spot_leverage (Optional[bool]): If False, calculates max amount without considering leverage. Defaults to True.

        Returns:
            MaxWithdrawableData: The maximum withdrawable amount for the spot product.
        """
        return self.context.engine_client.get_max_withdrawable(
            product_id, sender, spot_leverage
        )

    def get_token_wallet_balance(self, product_id: int, address: str):
        """
        Placeholder for a function to retrieve the current balance of a specific token in the user's wallet,
        excluding the amount in any Vertex subaccounts.

        Args:
            product_id (int): The identifier for the spot product.
            address (str): The user's wallet address.

        Raises:
            NotImplementedError: This function is not yet implemented.
        """
        raise NotImplementedError("This function is not yet implemented")

    def get_token_allowance(self, product_id: int, address: str):
        """
        Placeholder for a function to retrieve the current allowance of a specific token for a user's wallet.

        Args:
            product_id (int): The identifier for the spot product.
            address (str): The user's wallet address.

        Raises:
            NotImplementedError: This function is not yet implemented.
        """
        raise NotImplementedError("This function is not yet implemented")
