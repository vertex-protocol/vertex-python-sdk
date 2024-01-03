from typing import Optional, Union
import requests
from functools import singledispatchmethod
from vertex_protocol.indexer_client.types import IndexerClientOpts
from vertex_protocol.indexer_client.types.query import (
    IndexerCandlesticksParams,
    IndexerCandlesticksData,
    IndexerEventsParams,
    IndexerEventsData,
    IndexerFundingRateParams,
    IndexerFundingRateData,
    IndexerFundingRatesParams,
    IndexerFundingRatesData,
    IndexerHistoricalOrdersByDigestParams,
    IndexerHistoricalOrdersData,
    IndexerReferralCodeData,
    IndexerReferralCodeParams,
    IndexerSubaccountHistoricalOrdersParams,
    IndexerLinkedSignerRateLimitData,
    IndexerLinkedSignerRateLimitParams,
    IndexerLiquidationFeedData,
    IndexerLiquidationFeedParams,
    IndexerMakerStatisticsData,
    IndexerMakerStatisticsParams,
    IndexerMatchesParams,
    IndexerMatchesData,
    IndexerOraclePricesData,
    IndexerOraclePricesParams,
    IndexerParams,
    IndexerPerpPricesData,
    IndexerPerpPricesParams,
    IndexerProductSnapshotsData,
    IndexerProductSnapshotsParams,
    IndexerRequest,
    IndexerResponse,
    IndexerSubaccountSummaryParams,
    IndexerSubaccountSummaryData,
    IndexerSubaccountsData,
    IndexerSubaccountsParams,
    IndexerTokenRewardsData,
    IndexerTokenRewardsParams,
    to_indexer_request,
)
from vertex_protocol.utils.model import (
    VertexBaseModel,
    ensure_data_type,
    is_instance_of_union,
)


class IndexerQueryClient:
    """
    Client for querying data from the indexer service.

    Attributes:
        _opts (IndexerClientOpts): Client configuration options for connecting and interacting with the indexer service.
        url (str): URL of the indexer service.
    """

    def __init__(self, opts: IndexerClientOpts):
        """
        Initializes the IndexerQueryClient with the provided options.

        Args:
            opts (IndexerClientOpts): Client configuration options for connecting and interacting with the indexer service.
        """
        self._opts = IndexerClientOpts.parse_obj(opts)
        self.url = self._opts.url
        self.session = requests.Session()

    @singledispatchmethod
    def query(self, params: Union[IndexerParams, IndexerRequest]) -> IndexerResponse:
        """
        Sends a query request to the indexer service and returns the response.

        The `query` method is overloaded to accept either `IndexerParams` or a dictionary or `IndexerRequest`
        as the input parameters. Based on the type of the input, the appropriate internal method is invoked
        to process the query request.

        Args:
            params (IndexerParams | dict | IndexerRequest): The parameters for the query request.

        Returns:
            IndexerResponse: The response from the indexer service.
        """
        req: IndexerRequest = (
            params if is_instance_of_union(params, IndexerRequest) else to_indexer_request(params)  # type: ignore
        )
        return self._query(req)

    @query.register
    def _(self, req: dict) -> IndexerResponse:
        return self._query(VertexBaseModel.parse_obj(req))  # type: ignore

    def _query(self, req: IndexerRequest) -> IndexerResponse:
        res = self.session.post(self.url, json=req.dict())
        if res.status_code != 200:
            raise Exception(res.text)
        try:
            indexer_res = IndexerResponse(data=res.json())
        except Exception:
            raise Exception(res.text)
        return indexer_res

    def get_subaccount_historical_orders(
        self, params: IndexerSubaccountHistoricalOrdersParams
    ) -> IndexerHistoricalOrdersData:
        """
        Retrieves the historical orders associated with a specific subaccount.

        Args:
            params (IndexerSubaccountHistoricalOrdersParams): The parameters specifying the subaccount for which to retrieve historical orders.

        Returns:
            IndexerHistoricalOrdersData: The historical orders associated with the specified subaccount.
        """
        return ensure_data_type(
            self.query(IndexerSubaccountHistoricalOrdersParams.parse_obj(params)).data,
            IndexerHistoricalOrdersData,
        )

    def get_historical_orders_by_digest(
        self, digests: list[str]
    ) -> IndexerHistoricalOrdersData:
        """
        Retrieves historical orders using their unique digests.

        Args:
            digests (list[str]): A list of order digests.

        Returns:
            IndexerHistoricalOrdersData: The historical orders corresponding to the provided digests.
        """
        return ensure_data_type(
            self.query(IndexerHistoricalOrdersByDigestParams(digests=digests)).data,
            IndexerHistoricalOrdersData,
        )

    def get_matches(self, params: IndexerMatchesParams) -> IndexerMatchesData:
        """
        Retrieves match data based on provided parameters.

        Args:
            params (IndexerMatchesParams): The parameters for the match data retrieval request.

        Returns:
            IndexerMatchesData: The match data corresponding to the provided parameters.
        """
        return ensure_data_type(
            self.query(IndexerMatchesParams.parse_obj(params)).data, IndexerMatchesData
        )

    def get_events(self, params: IndexerEventsParams) -> IndexerEventsData:
        """
        Retrieves event data based on provided parameters.

        Args:
            params (IndexerEventsParams): The parameters for the event data retrieval request.

        Returns:
            IndexerEventsData: The event data corresponding to the provided parameters.
        """
        return ensure_data_type(
            self.query(IndexerEventsParams.parse_obj(params)).data, IndexerEventsData
        )

    def get_subaccount_summary(
        self, subaccount: str, timestamp: Optional[int] = None
    ) -> IndexerSubaccountSummaryData:
        """
        Retrieves a summary of a specified subaccount at a certain timestamp.

        Args:
            subaccount (str): The identifier for the subaccount.

            timestamp (int | None, optional): The timestamp for which to retrieve the subaccount summary. If not provided, the most recent summary is retrieved.

        Returns:
            IndexerSubaccountSummaryData: The summary of the specified subaccount at the provided timestamp.
        """
        return ensure_data_type(
            self.query(
                IndexerSubaccountSummaryParams(
                    subaccount=subaccount, timestamp=timestamp
                )
            ).data,
            IndexerSubaccountSummaryData,
        )

    def get_product_snapshots(
        self, params: IndexerProductSnapshotsParams
    ) -> IndexerProductSnapshotsData:
        """
        Retrieves snapshot data for specific products.

        Args:
            params (IndexerProductSnapshotsParams): Parameters specifying the products for which to retrieve snapshot data.

        Returns:
            IndexerProductSnapshotsData: The product snapshot data corresponding to the provided parameters.
        """
        return ensure_data_type(
            self.query(IndexerProductSnapshotsParams.parse_obj(params)).data,
            IndexerProductSnapshotsData,
        )

    def get_candlesticks(
        self, params: IndexerCandlesticksParams
    ) -> IndexerCandlesticksData:
        """
        Retrieves candlestick data based on provided parameters.

        Args:
            params (IndexerCandlesticksParams): The parameters for retrieving candlestick data.

        Returns:
            IndexerCandlesticksData: The candlestick data corresponding to the provided parameters.
        """
        return ensure_data_type(
            self.query(IndexerCandlesticksParams.parse_obj(params)).data,
            IndexerCandlesticksData,
        )

    def get_perp_funding_rate(self, product_id: int) -> IndexerFundingRateData:
        """
        Retrieves the funding rate data for a specific perp product.

        Args:
            product_id (int): The identifier of the perp product.

        Returns:
            IndexerFundingRateData: The funding rate data for the specified perp product.
        """
        return ensure_data_type(
            self.query(IndexerFundingRateParams(product_id=product_id)).data,
            IndexerFundingRateData,
        )

    def get_perp_funding_rates(self, product_ids: list) -> IndexerFundingRatesData:
        """
        Fetches the latest funding rates for a list of perp products.

        Args:
            product_ids (list): List of identifiers for the perp products.

        Returns:
            dict: A dictionary mapping each product_id to its latest funding rate and related details.
        """
        return ensure_data_type(
            self.query(IndexerFundingRatesParams(product_ids=product_ids)).data, dict
        )

    def get_perp_prices(self, product_id: int) -> IndexerPerpPricesData:
        """
        Retrieves the price data for a specific perp product.

        Args:
            product_id (int): The identifier of the perp product.

        Returns:
            IndexerPerpPricesData: The price data for the specified perp product.
        """
        return ensure_data_type(
            self.query(IndexerPerpPricesParams(product_id=product_id)).data,
            IndexerPerpPricesData,
        )

    def get_oracle_prices(self, product_ids: list[int]) -> IndexerOraclePricesData:
        """
        Retrieves the oracle price data for specific products.

        Args:
            product_ids (list[int]): A list of product identifiers.

        Returns:
            IndexerOraclePricesData: The oracle price data for the specified products.
        """
        return ensure_data_type(
            self.query(IndexerOraclePricesParams(product_ids=product_ids)).data,
            IndexerOraclePricesData,
        )

    def get_token_rewards(self, address: str) -> IndexerTokenRewardsData:
        """
        Retrieves the token reward data for a specific address.

        Args:
            address (str): The address for which to retrieve token reward data.

        Returns:
            IndexerTokenRewardsData: The token reward data for the specified address.
        """
        return ensure_data_type(
            self.query(IndexerTokenRewardsParams(address=address)).data,
            IndexerTokenRewardsData,
        )

    def get_maker_statistics(
        self, params: IndexerMakerStatisticsParams
    ) -> IndexerMakerStatisticsData:
        """
        Retrieves maker statistics based on provided parameters.

        Args:
            params (IndexerMakerStatisticsParams): The parameters for retrieving maker statistics.

        Returns:
            IndexerMakerStatisticsData: The maker statistics corresponding to the provided parameters.
        """
        return ensure_data_type(
            self.query(IndexerMakerStatisticsParams.parse_obj(params)).data,
            IndexerMakerStatisticsData,
        )

    def get_liquidation_feed(self) -> IndexerLiquidationFeedData:
        """
        Retrieves the liquidation feed data.

        Returns:
            IndexerLiquidationFeedData: The latest liquidation feed data.
        """
        return ensure_data_type(self.query(IndexerLiquidationFeedParams()).data, list)

    def get_linked_signer_rate_limits(
        self, subaccount: str
    ) -> IndexerLinkedSignerRateLimitData:
        """
        Retrieves the rate limits for a linked signer of a specific subaccount.

        Args:
            subaccount (str): The identifier of the subaccount.

        Returns:
            IndexerLinkedSignerRateLimitData: The rate limits for the linked signer of the specified subaccount.
        """
        return ensure_data_type(
            self.query(IndexerLinkedSignerRateLimitParams(subaccount=subaccount)).data,
            IndexerLinkedSignerRateLimitData,
        )

    def get_referral_code(self, subaccount: str) -> IndexerReferralCodeData:
        """
        Retrieves the referral code for a given address.

        Args:
            subaccount (str): Unique identifier for the subaccount.

        Returns:
            IndexerReferralCodeData: The referral code for the specific address.
        """
        return ensure_data_type(
            self.query(IndexerReferralCodeParams(subaccount=subaccount)).data,
            IndexerReferralCodeData,
        )

    def get_subaccounts(
        self, params: IndexerSubaccountsParams
    ) -> IndexerSubaccountsData:
        """
        Retrieves subaccounts via the indexer.

        Args:
            params (IndexerSubaccountsParams): The filter parameters for retrieving subaccounts.

        Returns:
            IndexerSubaccountsData: List of subaccounts found.
        """
        return ensure_data_type(
            self.query(params).data,
            IndexerSubaccountsData,
        )
