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
from vertex_protocol.utils.model import VertexBaseModel


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
        return self._query(VertexBaseModel.parse_obj(req))

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
        return self.query(
            IndexerSubaccountHistoricalOrdersParams.parse_obj(params)
        ).data

    def get_historical_orders_by_digest(
        self, digests: list[str]
    ) -> IndexerHistoricalOrdersData:
        """
        Queries historical orders by their digest.
        """
        return self.query(IndexerHistoricalOrdersByDigestParams(digests=digests)).data

    def get_matches(self, params: IndexerMatchesParams) -> IndexerMatchesData:
        """
        Queries match data.
        """
        return self.query(IndexerMatchesParams.parse_obj(params)).data

    def get_events(self, params: IndexerEventsParams) -> IndexerEventsData:
        """
        Queries event data.
        """
        return self.query(IndexerEventsParams.parse_obj(params)).data

    def get_subaccount_summary(
        self, subaccount: str, timestamp: int = None
    ) -> IndexerSubaccountSummaryData:
        """
        Queries a summary of a subaccount.
        """
        return self.query(
            IndexerSubaccountSummaryParams(subaccount=subaccount, timestamp=timestamp)
        ).data

    def get_product_snapshots(
        self, params: IndexerProductSnapshotsParams
    ) -> IndexerProductSnapshotsData:
        """
        Queries product snapshot data.
        """
        return self.query(IndexerProductSnapshotsParams.parse_obj(params)).data

    def get_candlesticks(
        self, params: IndexerCandlesticksParams
    ) -> IndexerCandlesticksData:
        """
        Queries candlestick data.
        """
        return self.query(IndexerCandlesticksParams.parse_obj(params)).data

    def get_perp_funding_rate(self, product_id: int) -> IndexerFundingRateData:
        """
        Queries perp funding rate data.
        """
        return self.query(IndexerFundingRateParams(product_id=product_id)).data

    def get_perp_prices(self, product_id: int) -> IndexerPerpPricesData:
        """
        Queries perp price data.
        """
        return self.query(IndexerPerpPricesParams(product_id=product_id)).data

    def get_oracle_prices(self, product_ids: list[int]) -> IndexerOraclePricesData:
        """
        Queries oracle price data.
        """
        return self.query(IndexerOraclePricesParams(product_ids=product_ids)).data

    def get_token_rewards(self, address: str) -> IndexerTokenRewardsData:
        """
        Queries token reward data.
        """
        return self.query(IndexerTokenRewardsParams(address=address)).data

    def get_maker_statistics(
        self, params: IndexerMakerStatisticsParams
    ) -> IndexerMakerStatisticsData:
        """
        Queries maker statistic data.
        """
        return self.query(IndexerMakerStatisticsParams.parse_obj(params)).data

    def get_liquidation_feed(self) -> IndexerLiquidationFeedData:
        """
        Queries liquidation feed data.
        """
        return self.query(IndexerLiquidationFeedParams()).data

    def get_linked_signer_rate_limits(
        self, subaccount: str
    ) -> IndexerLinkedSignerRateLimitData:
        """
        Queries rate limits for a linked signer.
        """
        return self.query(
            IndexerLinkedSignerRateLimitParams(subaccount=subaccount)
        ).data
