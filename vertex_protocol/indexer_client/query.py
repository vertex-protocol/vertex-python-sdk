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
    IndexerHistoricalOrdersParams,
    IndexerHistoricalOrdersData,
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
    IndexerProductsParams,
    IndexerProductsData,
    IndexerRequest,
    IndexerResponse,
    IndexerSubaccountSummaryParams,
    IndexerSubaccountSummaryData,
    IndexerTokenRewardsData,
    IndexerTokenRewardsParams,
    to_indexer_request,
)


class IndexerQueryClient:
    def __init__(self, opts: IndexerClientOpts):
        """
        Initialize EngineQueryClient with provided options
        """
        self._opts = IndexerClientOpts.parse_obj(opts)
        self.url = self._opts.url

    @singledispatchmethod
    def query(self, params: IndexerParams) -> IndexerResponse:
        return self._query(to_indexer_request(params))

    @query.register
    def _(self, req: IndexerRequest) -> IndexerResponse:
        return self._query(req)

    def _query(self, req: IndexerRequest) -> IndexerResponse:
        res = requests.post(f"{self.url}/indexer", json=req.dict())
        if res.status_code != 200:
            raise Exception(res.text)
        return IndexerResponse(**res.json())

    def get_historical_orders(
        self, params: IndexerHistoricalOrdersParams
    ) -> IndexerHistoricalOrdersData:
        return self.query(params).data

    def get_matches(self, params: IndexerMatchesParams) -> IndexerMatchesData:
        return self.query(params).data

    def get_events(self, params: IndexerEventsParams) -> IndexerEventsData:
        return self.query(params).data

    def get_subaccount_summary(
        self, subaccount: str, timestamp: int = None
    ) -> IndexerSubaccountSummaryData:
        return self.query(
            IndexerSubaccountSummaryParams(subaccount=subaccount, timestamp=timestamp)
        ).data

    def get_products(self, params: IndexerProductsParams) -> IndexerProductsData:
        return self.query(params).data

    def get_candlesticks(
        self, params: IndexerCandlesticksParams
    ) -> IndexerCandlesticksData:
        return self.query(params).data

    def get_perp_funding_rate(self, product_id: int) -> IndexerFundingRateData:
        return self.query(IndexerFundingRateParams(product_id=product_id)).data

    def get_perp_prices(self, product_id: int) -> IndexerPerpPricesData:
        return self.query(IndexerPerpPricesParams(product_id=product_id)).data

    def get_oracle_prices(self, product_ids: list[int]) -> IndexerOraclePricesData:
        return self.query(IndexerOraclePricesParams(product_ids=product_ids)).data

    def get_token_rewards(self, address: str) -> IndexerTokenRewardsData:
        return self.query(IndexerTokenRewardsParams(address=address)).data

    def get_maker_statistics(
        self, params: IndexerMakerStatisticsParams
    ) -> IndexerMakerStatisticsData:
        return self.query(params).data

    def get_liquidation_feed(self) -> IndexerLiquidationFeedData:
        return self.query(IndexerLiquidationFeedParams()).data

    def get_linked_signer_rate_limits(
        self, subaccount: str
    ) -> IndexerLinkedSignerRateLimitData:
        return self.query(
            IndexerLinkedSignerRateLimitParams(subaccount=subaccount)
        ).data
