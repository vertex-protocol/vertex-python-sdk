from typing import Optional

from pydantic import Field
from vertex_protocol.indexer_client.types.models import (
    IndexerCandlesticksGranularity,
    IndexerEventType,
)
from vertex_protocol.utils.indexer import VertexIndexer
from vertex_protocol.utils.model import VertexBaseModel


class IndexerBaseParams(VertexBaseModel):
    idx: Optional[int] = Field(alias="submission_idx")
    max_time: Optional[int]
    limit: Optional[int]


class IndexerOrdersParams(IndexerBaseParams):
    subaccount: Optional[str]
    product_ids: Optional[list[int]]
    digests: Optional[list[str]]


class IndexerMatchesParams(IndexerBaseParams):
    subaccount: Optional[str]
    product_ids: Optional[list[int]]


class IndexerEventsRawLimit(VertexBaseModel):
    raw: int


class IndexerEventsTxsLimit(VertexBaseModel):
    txs: int


IndexerEventsLimit = IndexerEventsRawLimit | IndexerEventsTxsLimit


class IndexerEventsParams(IndexerBaseParams):
    subaccount: Optional[str]
    product_ids: Optional[list[int]]
    event_types: Optional[list[IndexerEventType]]
    limit: Optional[IndexerEventsLimit]


class IndexerSummaryParams(VertexBaseModel):
    subaccount: str
    timestamp: Optional[int]


class IndexerProductsParams(IndexerBaseParams):
    product_id: int


class IndexerCandlesticksParams(IndexerBaseParams):
    product_id: int
    granularity: IndexerCandlesticksGranularity

    class Config:
        fields = {"idx": {"exclude": True}}


class IndexerFundingRateParams(VertexBaseModel):
    product_id: int


class IndexerPerpPricesParams(VertexBaseModel):
    product_id: int


class IndexerOraclePricesParams(VertexBaseModel):
    product_ids: list[int]


class IndexerRewardsParams(VertexBaseModel):
    address: str


class IndexerMakerStatisticsParams(VertexBaseModel):
    product_id: int
    epoch: int
    interval: int


class IndexerLiquidationFeedParams(VertexBaseModel):
    pass


class IndexerLinkedSignerRateLimitParams(VertexBaseModel):
    subaccount: str


IndexerParams = (
    IndexerOrdersParams
    | IndexerMatchesParams
    | IndexerEventsParams
    | IndexerSummaryParams
    | IndexerProductsParams
    | IndexerCandlesticksParams
    | IndexerFundingRateParams
    | IndexerPerpPricesParams
    | IndexerOraclePricesParams
    | IndexerRewardsParams
    | IndexerMakerStatisticsParams
    | IndexerLiquidationFeedParams
    | IndexerLinkedSignerRateLimitParams
)


class IndexerOrdersRequest(VertexBaseModel):
    orders: IndexerOrdersParams


class IndexerMatchesRequest(VertexBaseModel):
    matches: IndexerMatchesParams


class IndexerEventsRequest(VertexBaseModel):
    events: IndexerEventsParams


class IndexerSummaryRequest(VertexBaseModel):
    summary: IndexerSummaryParams


class IndexerProductRequest(VertexBaseModel):
    products: IndexerProductsParams


class IndexerCandlesticksRequest(VertexBaseModel):
    candlesticks: IndexerCandlesticksParams


class IndexerFundingRateRequest(VertexBaseModel):
    funding_rate: IndexerFundingRateParams


class IndexerPerpPricesRequest(VertexBaseModel):
    price: IndexerPerpPricesParams


class IndexerOraclePricesRequest(VertexBaseModel):
    oracle_price: IndexerOraclePricesParams


class IndexerRewardsRequest(VertexBaseModel):
    rewards: IndexerRewardsParams


class IndexerMakerStatisticsRequest(VertexBaseModel):
    maker_statistics: IndexerMakerStatisticsParams


class IndexerLiquidationFeedRequest(VertexBaseModel):
    liquidation_feed: IndexerLiquidationFeedParams


class IndexerLinkedSignerRateLimitRequest(VertexBaseModel):
    linked_signer_rate_limit: IndexerLinkedSignerRateLimitParams


IndexerRequest = (
    IndexerOrdersRequest
    | IndexerMatchesRequest
    | IndexerEventsRequest
    | IndexerSummaryRequest
    | IndexerProductRequest
    | IndexerCandlesticksRequest
    | IndexerSummaryRequest
    | IndexerFundingRateRequest
    | IndexerPerpPricesRequest
    | IndexerOraclePricesRequest
    | IndexerRewardsRequest
    | IndexerMakerStatisticsRequest
    | IndexerLiquidationFeedRequest
    | IndexerLinkedSignerRateLimitRequest
)


def to_indexer_request(params: IndexerParams) -> IndexerRequest:
    indexer_request_mapping = {
        IndexerOrdersParams: (IndexerOrdersRequest, VertexIndexer.ORDERS),
        IndexerMatchesParams: (IndexerMatchesRequest, VertexIndexer.MATCHES),
        IndexerEventsParams: (IndexerEventsRequest, VertexIndexer.EVENTS),
        IndexerSummaryParams: (IndexerSummaryRequest, VertexIndexer.SUMMARY),
        IndexerProductsParams: (IndexerProductRequest, VertexIndexer.PRODUCTS),
        IndexerCandlesticksParams: (
            IndexerCandlesticksRequest,
            VertexIndexer.CANDLESTICKS,
        ),
        IndexerFundingRateParams: (
            IndexerFundingRateRequest,
            VertexIndexer.FUNDING_RATE,
        ),
        IndexerPerpPricesParams: (IndexerPerpPricesRequest, VertexIndexer.PERP_PRICES),
        IndexerOraclePricesParams: (
            IndexerOraclePricesRequest,
            VertexIndexer.ORACLE_PRICES,
        ),
        IndexerRewardsParams: (IndexerRewardsRequest, VertexIndexer.REWARDS),
        IndexerMakerStatisticsParams: (
            IndexerMakerStatisticsRequest,
            VertexIndexer.MAKER_STATISTICS,
        ),
        IndexerLiquidationFeedParams: (
            IndexerLiquidationFeedRequest,
            VertexIndexer.LIQUIDATION_FEED,
        ),
        IndexerLinkedSignerRateLimitParams: (
            IndexerLinkedSignerRateLimitRequest,
            VertexIndexer.LINKED_SIGNER_RATE_LIMIT,
        ),
    }

    RequestClass, field_name = indexer_request_mapping[type(params)]
    return RequestClass(**{field_name: params})


IndexerResponse = None
