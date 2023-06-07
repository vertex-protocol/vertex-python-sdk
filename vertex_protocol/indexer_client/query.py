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
    IndexerHistoricalOrdersByDigestParams,
    IndexerHistoricalOrdersData,
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
    IndexerTokenRewardsData,
    IndexerTokenRewardsParams,
    to_indexer_request,
)
from vertex_protocol.utils.model import VertexBaseModel, ensure_data_type


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

    @singledispatchmethod
    def query(self, params: IndexerParams) -> IndexerResponse:
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
        return self._query(to_indexer_request(params))

    @query.register
    def _(self, req: dict | IndexerRequest) -> IndexerResponse:
        return self._query(VertexBaseModel.parse_obj(req))  # type: ignore

    def _query(self, req: IndexerRequest) -> IndexerResponse:
        res = requests.post(f"{self.url}/indexer", json=req.dict())
        if res.status_code != 200:
            raise Exception(res.text)
        return IndexerResponse(data=res.json())

    def get_subaccount_historical_orders(
        self, params: IndexerSubaccountHistoricalOrdersParams
    ) -> IndexerHistoricalOrdersData:
        """
        Queries historical orders of a subaccount.
        """
        return ensure_data_type(
            self.query(IndexerSubaccountHistoricalOrdersParams.parse_obj(params)).data,
            IndexerHistoricalOrdersData,
        )

    def get_historical_orders_by_digest(
        self, digests: list[str]
    ) -> IndexerHistoricalOrdersData:
        """
        Queries historical orders by their digest.
        """
        return ensure_data_type(
            self.query(IndexerHistoricalOrdersByDigestParams(digests=digests)).data,
            IndexerHistoricalOrdersData,
        )

    def get_matches(self, params: IndexerMatchesParams) -> IndexerMatchesData:
        """
        Queries match data.
        """
        return ensure_data_type(
            self.query(IndexerMatchesParams.parse_obj(params)).data, IndexerMatchesData
        )

    def get_events(self, params: IndexerEventsParams) -> IndexerEventsData:
        """
        Queries event data.
        """
        return ensure_data_type(
            self.query(IndexerEventsParams.parse_obj(params)).data, IndexerEventsData
        )

    def get_subaccount_summary(
        self, subaccount: str, timestamp: int | None = None
    ) -> IndexerSubaccountSummaryData:
        """
        Queries a summary of a subaccount.
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
        Queries product snapshot data.
        """
        return ensure_data_type(
            self.query(IndexerProductSnapshotsParams.parse_obj(params)).data,
            IndexerProductSnapshotsData,
        )

    def get_candlesticks(
        self, params: IndexerCandlesticksParams
    ) -> IndexerCandlesticksData:
        """
        Queries candlestick data.
        """
        return ensure_data_type(
            self.query(IndexerCandlesticksParams.parse_obj(params)).data,
            IndexerCandlesticksData,
        )

    def get_perp_funding_rate(self, product_id: int) -> IndexerFundingRateData:
        """
        Queries perp funding rate data.
        """
        return ensure_data_type(
            self.query(IndexerFundingRateParams(product_id=product_id)).data,
            IndexerFundingRateData,
        )

    def get_perp_prices(self, product_id: int) -> IndexerPerpPricesData:
        """
        Queries perp price data.
        """
        return ensure_data_type(
            self.query(IndexerPerpPricesParams(product_id=product_id)).data,
            IndexerPerpPricesData,
        )

    def get_oracle_prices(self, product_ids: list[int]) -> IndexerOraclePricesData:
        """
        Queries oracle price data.
        """
        return ensure_data_type(
            self.query(IndexerOraclePricesParams(product_ids=product_ids)).data,
            IndexerOraclePricesData,
        )

    def get_token_rewards(self, address: str) -> IndexerTokenRewardsData:
        """
        Queries token reward data.
        """
        return ensure_data_type(
            self.query(IndexerTokenRewardsParams(address=address)).data,
            IndexerTokenRewardsData,
        )

    def get_maker_statistics(
        self, params: IndexerMakerStatisticsParams
    ) -> IndexerMakerStatisticsData:
        """
        Queries maker statistic data.
        """
        return ensure_data_type(
            self.query(IndexerMakerStatisticsParams.parse_obj(params)).data,
            IndexerMakerStatisticsData,
        )

    def get_liquidation_feed(self) -> IndexerLiquidationFeedData:
        """
        Queries liquidation feed data.
        """
        return ensure_data_type(self.query(IndexerLiquidationFeedParams()).data, list)

    def get_linked_signer_rate_limits(
        self, subaccount: str
    ) -> IndexerLinkedSignerRateLimitData:
        """
        Queries rate limits for a linked signer.
        """
        return ensure_data_type(
            self.query(IndexerLinkedSignerRateLimitParams(subaccount=subaccount)).data,
            IndexerLinkedSignerRateLimitData,
        )
