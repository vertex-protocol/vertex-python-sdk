from enum import StrEnum
from typing import Optional

from pydantic import Field
from vertex_protocol.indexer_client.types.models import (
    IndexerCandlestick,
    IndexerCandlesticksGranularity,
    IndexerEvent,
    IndexerEventType,
    IndexerHistoricalOrder,
    IndexerLiquidatableAccount,
    IndexerMarketMaker,
    IndexerMatch,
    IndexerOraclePrice,
    IndexerProduct,
    IndexerTokenReward,
    IndexerTx,
)
from vertex_protocol.utils.model import VertexBaseModel


class IndexerQueryType(StrEnum):
    ORDERS = "orders"
    MATCHES = "matches"
    EVENTS = "events"
    SUMMARY = "summary"
    PRODUCTS = "products"
    CANDLESTICKS = "candlesticks"
    FUNDING_RATE = "funding_rate"
    PERP_PRICES = "price"
    ORACLE_PRICES = "oracle_price"
    REWARDS = "rewards"
    MAKER_STATISTICS = "maker_statistics"
    LIQUIDATION_FEED = "liquidation_feed"
    LINKED_SIGNER_RATE_LIMIT = "linked_signer_rate_limit"


class IndexerBaseParams(VertexBaseModel):
    idx: Optional[int] = Field(alias="submission_idx")
    max_time: Optional[int]
    limit: Optional[int]


class IndexerSubaccountHistoricalOrdersParams(IndexerBaseParams):
    subaccount: str
    product_ids: Optional[list[int]]


class IndexerHistoricalOrdersByDigestParams(VertexBaseModel):
    digests: list[str]


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


class IndexerSubaccountSummaryParams(VertexBaseModel):
    subaccount: str
    timestamp: Optional[int]


class IndexerProductSnapshotsParams(IndexerBaseParams):
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


class IndexerTokenRewardsParams(VertexBaseModel):
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
    IndexerSubaccountHistoricalOrdersParams
    | IndexerHistoricalOrdersByDigestParams
    | IndexerMatchesParams
    | IndexerEventsParams
    | IndexerSubaccountSummaryParams
    | IndexerProductSnapshotsParams
    | IndexerCandlesticksParams
    | IndexerFundingRateParams
    | IndexerPerpPricesParams
    | IndexerOraclePricesParams
    | IndexerTokenRewardsParams
    | IndexerMakerStatisticsParams
    | IndexerLiquidationFeedParams
    | IndexerLinkedSignerRateLimitParams
)


class IndexerHistoricalOrdersRequest(VertexBaseModel):
    orders: IndexerSubaccountHistoricalOrdersParams | IndexerHistoricalOrdersByDigestParams


class IndexerMatchesRequest(VertexBaseModel):
    matches: IndexerMatchesParams


class IndexerEventsRequest(VertexBaseModel):
    events: IndexerEventsParams


class IndexerSubaccountSummaryRequest(VertexBaseModel):
    summary: IndexerSubaccountSummaryParams


class IndexerProductSnapshotsRequest(VertexBaseModel):
    products: IndexerProductSnapshotsParams


class IndexerCandlesticksRequest(VertexBaseModel):
    candlesticks: IndexerCandlesticksParams


class IndexerFundingRateRequest(VertexBaseModel):
    funding_rate: IndexerFundingRateParams


class IndexerPerpPricesRequest(VertexBaseModel):
    price: IndexerPerpPricesParams


class IndexerOraclePricesRequest(VertexBaseModel):
    oracle_price: IndexerOraclePricesParams


class IndexerTokenRewardsRequest(VertexBaseModel):
    rewards: IndexerTokenRewardsParams


class IndexerMakerStatisticsRequest(VertexBaseModel):
    maker_statistics: IndexerMakerStatisticsParams


class IndexerLiquidationFeedRequest(VertexBaseModel):
    liquidation_feed: IndexerLiquidationFeedParams


class IndexerLinkedSignerRateLimitRequest(VertexBaseModel):
    linked_signer_rate_limit: IndexerLinkedSignerRateLimitParams


IndexerRequest = (
    IndexerHistoricalOrdersRequest
    | IndexerMatchesRequest
    | IndexerEventsRequest
    | IndexerSubaccountSummaryRequest
    | IndexerProductSnapshotsRequest
    | IndexerCandlesticksRequest
    | IndexerFundingRateRequest
    | IndexerPerpPricesRequest
    | IndexerOraclePricesRequest
    | IndexerTokenRewardsRequest
    | IndexerMakerStatisticsRequest
    | IndexerLiquidationFeedRequest
    | IndexerLinkedSignerRateLimitRequest
)


class IndexerHistoricalOrdersData(VertexBaseModel):
    orders: list[IndexerHistoricalOrder]


class IndexerMatchesData(VertexBaseModel):
    matches: list[IndexerMatch]
    txs: list[IndexerTx]


class IndexerEventsData(VertexBaseModel):
    events: list[IndexerEvent]
    txs: list[IndexerTx]


class IndexerSubaccountSummaryData(VertexBaseModel):
    events: list[IndexerEvent]


class IndexerProductSnapshotsData(VertexBaseModel):
    products: list[IndexerProduct]
    txs: list[IndexerTx]


class IndexerCandlesticksData(VertexBaseModel):
    candlesticks: list[IndexerCandlestick]


class IndexerFundingRateData(VertexBaseModel):
    product_id: int
    funding_rate_x18: str
    update_time: str


class IndexerPerpPricesData(VertexBaseModel):
    product_id: int
    index_price_x18: str
    mark_price_x18: str
    update_time: str


class IndexerOraclePricesData(VertexBaseModel):
    prices: list[IndexerOraclePrice]


class IndexerTokenRewardsData(VertexBaseModel):
    rewards: list[IndexerTokenReward]
    update_time: str


class IndexerMakerStatisticsData(VertexBaseModel):
    reward_coefficient: float
    makers: list[IndexerMarketMaker]


class IndexerLinkedSignerRateLimitData(VertexBaseModel):
    remaining_tx: str
    wait_time: int
    signer: str


IndexerLiquidationFeedData = list[IndexerLiquidatableAccount]


IndexerResponseData = (
    IndexerHistoricalOrdersData
    | IndexerMatchesData
    | IndexerEventsData
    | IndexerSubaccountSummaryData
    | IndexerProductSnapshotsData
    | IndexerCandlesticksData
    | IndexerFundingRateData
    | IndexerPerpPricesData
    | IndexerOraclePricesData
    | IndexerTokenRewardsData
    | IndexerMakerStatisticsData
    | IndexerLinkedSignerRateLimitData
    | IndexerLiquidationFeedData
)


class IndexerResponse(VertexBaseModel):
    data: IndexerResponseData


def to_indexer_request(params: IndexerParams) -> IndexerRequest:
    indexer_request_mapping = {
        IndexerSubaccountHistoricalOrdersParams: (
            IndexerHistoricalOrdersRequest,
            IndexerQueryType.ORDERS,
        ),
        IndexerHistoricalOrdersByDigestParams: (
            IndexerHistoricalOrdersRequest,
            IndexerQueryType.ORDERS,
        ),
        IndexerMatchesParams: (IndexerMatchesRequest, IndexerQueryType.MATCHES),
        IndexerEventsParams: (IndexerEventsRequest, IndexerQueryType.EVENTS),
        IndexerSubaccountSummaryParams: (
            IndexerSubaccountSummaryRequest,
            IndexerQueryType.SUMMARY,
        ),
        IndexerProductSnapshotsParams: (
            IndexerProductSnapshotsRequest,
            IndexerQueryType.PRODUCTS,
        ),
        IndexerCandlesticksParams: (
            IndexerCandlesticksRequest,
            IndexerQueryType.CANDLESTICKS,
        ),
        IndexerFundingRateParams: (
            IndexerFundingRateRequest,
            IndexerQueryType.FUNDING_RATE,
        ),
        IndexerPerpPricesParams: (
            IndexerPerpPricesRequest,
            IndexerQueryType.PERP_PRICES,
        ),
        IndexerOraclePricesParams: (
            IndexerOraclePricesRequest,
            IndexerQueryType.ORACLE_PRICES,
        ),
        IndexerTokenRewardsParams: (
            IndexerTokenRewardsRequest,
            IndexerQueryType.REWARDS,
        ),
        IndexerMakerStatisticsParams: (
            IndexerMakerStatisticsRequest,
            IndexerQueryType.MAKER_STATISTICS,
        ),
        IndexerLiquidationFeedParams: (
            IndexerLiquidationFeedRequest,
            IndexerQueryType.LIQUIDATION_FEED,
        ),
        IndexerLinkedSignerRateLimitParams: (
            IndexerLinkedSignerRateLimitRequest,
            IndexerQueryType.LINKED_SIGNER_RATE_LIMIT,
        ),
    }

    RequestClass, field_name = indexer_request_mapping[type(params)]
    return RequestClass(**{field_name: params})
