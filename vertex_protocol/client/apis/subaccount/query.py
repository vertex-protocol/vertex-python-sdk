from typing import Optional
from vertex_protocol.client.apis.base import VertexBaseAPI
from vertex_protocol.engine_client.types.query import (
    FeeRatesData,
    QuerySubaccountInfoTx,
    SubaccountInfoData,
)
from vertex_protocol.indexer_client.types.query import (
    IndexerLinkedSignerRateLimitData,
    IndexerReferralCodeData,
    IndexerSubaccountsData,
    IndexerSubaccountsParams,
    IndexerTokenRewardsData,
)


class SubaccountQueryAPI(VertexBaseAPI):
    """
    Provides functionalities for querying data related to subaccounts in the Vertex Protocol.

    Inherits from VertexBaseAPI, which provides a basic context setup for accessing Vertex Clearinghouse.
    This class extends the base class to provide specific functionalities for querying data related to subaccounts.

    Attributes:
        context (VertexClientContext): Provides connectivity details for accessing Vertex APIs.
    """

    def get_engine_subaccount_summary(
        self, subaccount: str, txs: Optional[list[QuerySubaccountInfoTx]] = None
    ) -> SubaccountInfoData:
        """
        Retrieve a comprehensive summary of the specified subaccount's state as per the off-chain engine.

        You can optionally provide a list of txs to get an estimated view of your subaccount.

        Args:
            subaccount (str): Unique identifier for the subaccount.

            txs (list[QuerySubaccountInfoTx], optional): Optional list of transactions for the subaccount.

        Returns:
            SubaccountInfoData: A data class object containing detailed state information about the queried subaccount.
        """
        return self.context.engine_client.get_subaccount_info(subaccount, txs)

    def get_subaccount_fee_rates(self, subaccount: str) -> FeeRatesData:
        """
        Retrieve the fee rates associated with a specific subaccount from the off-chain engine.

        Args:
            subaccount (str): Unique identifier for the subaccount.

        Returns:
            FeeRatesData: A data class object containing detailed fee rates data for the specified subaccount.
        """
        return self.context.engine_client.get_fee_rates(subaccount)

    def get_subaccount_token_rewards(self, address: str) -> IndexerTokenRewardsData:
        """
        Query the $VRTX token rewards accumulated per epoch for a specified wallet from the indexer.

        Args:
            address (str): Wallet address to be queried.

        Returns:
            IndexerTokenRewardsData: A data class object containing detailed information about the accrued token rewards.
        """
        return self.context.indexer_client.get_token_rewards(address)

    def get_subaccount_linked_signer_rate_limits(
        self, subaccount: str
    ) -> IndexerLinkedSignerRateLimitData:
        """
        Retrieve the current linked signer and their rate limit for a specified subaccount from the indexer.

        Args:
            subaccount (str): Unique identifier for the subaccount.

        Returns:
            IndexerLinkedSignerRateLimitData: A data class object containing information about the current linked signer and their rate limits for the queried subaccount.
        """
        return self.context.indexer_client.get_linked_signer_rate_limits(subaccount)

    def get_referral_code(self, subaccount: str) -> IndexerReferralCodeData:
        """
        Query the referral code for the specified wallet from the indexer.

        Args:
            subaccount (str): Unique identifier for the subaccount.

        Returns:
            IndexerReferralCodeData: A data class object containing the wallet's referral code.
        """
        return self.context.indexer_client.get_referral_code(subaccount)

    def get_subaccounts(
        self,
        address: Optional[str] = None,
        start_idx: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> IndexerSubaccountsData:
        """
        List vertex subaccounts via the indexer.

        Args:
            address (Optional[str]): An optional wallet address to find all subaccounts associated to it.
            start_idx (Optional[int]): Optional subaccount id to start from. Used for pagination. Defaults to 0.
            limit (Optional[int]): Maximum number of subaccounts to return. Defaults to 100. Max of 500.

        Returns:
            IndexerSubaccountsData: A data class object containing the list of subaccounts found.
        """
        return self.context.indexer_client.get_subaccounts(
            IndexerSubaccountsParams(address=address, start=start_idx, limit=limit)
        )
