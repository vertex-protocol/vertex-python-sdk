from vertex_protocol.utils.enum import StrEnum
from typing import Dict, Optional, Union

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
    IndexerSubaccount,
    IndexerTokenReward,
    IndexerTx,
)
from vertex_protocol.utils.model import VertexBaseModel


class IndexerQueryType(StrEnum):
    """
    Enumeration of query types available in the Indexer service.
    """

    ORDERS = "orders"
    MATCHES = "matches"
    EVENTS = "events"
    SUMMARY = "summary"
    PRODUCTS = "products"
    CANDLESTICKS = "candlesticks"
    FUNDING_RATE = "funding_rate"
    FUNDING_RATES = "funding_rates"
    PERP_PRICES = "price"
    ORACLE_PRICES = "oracle_price"
    REWARDS = "rewards"
    MAKER_STATISTICS = "maker_statistics"
    LIQUIDATION_FEED = "liquidation_feed"
    LINKED_SIGNER_RATE_LIMIT = "linked_signer_rate_limit"
    REFERRAL_CODE = "referral_code"
    SUBACCOUNTS = "subaccounts"


class IndexerBaseParams(VertexBaseModel):
    """
    Base parameters for the indexer queries.
    """

    idx: Optional[int] = Field(alias="submission_idx")
    max_time: Optional[int]
    limit: Optional[int]

    class Config:
        allow_population_by_field_name = True


class IndexerSubaccountHistoricalOrdersParams(IndexerBaseParams):
    """
    Parameters for querying historical orders by subaccount.
    """

    subaccount: str
    product_ids: Optional[list[int]]


class IndexerHistoricalOrdersByDigestParams(VertexBaseModel):
    """
    Parameters for querying historical orders by digests.
    """

    digests: list[str]


class IndexerMatchesParams(IndexerBaseParams):
    """
    Parameters for querying matches.
    """

    subaccount: Optional[str]
    product_ids: Optional[list[int]]


class IndexerEventsRawLimit(VertexBaseModel):
    """
    Parameters for limiting by events count.
    """

    raw: int


class IndexerEventsTxsLimit(VertexBaseModel):
    """
    Parameters for limiting events by transaction count.
    """

    txs: int


IndexerEventsLimit = Union[IndexerEventsRawLimit, IndexerEventsTxsLimit]


class IndexerEventsParams(IndexerBaseParams):
    """
    Parameters for querying events.
    """

    subaccount: Optional[str]
    product_ids: Optional[list[int]]
    event_types: Optional[list[IndexerEventType]]
    limit: Optional[IndexerEventsLimit]  # type: ignore


class IndexerSubaccountSummaryParams(VertexBaseModel):
    """
    Parameters for querying subaccount summary.
    """

    subaccount: str
    timestamp: Optional[int]


class IndexerProductSnapshotsParams(IndexerBaseParams):
    """
    Parameters for querying product snapshots.
    """

    product_id: int


class IndexerCandlesticksParams(IndexerBaseParams):
    """
    Parameters for querying candlestick data.
    """

    product_id: int
    granularity: IndexerCandlesticksGranularity

    class Config:
        fields = {"idx": {"exclude": True}}


class IndexerFundingRateParams(VertexBaseModel):
    """
    Parameters for querying funding rates.
    """

    product_id: int


class IndexerFundingRatesParams(VertexBaseModel):
    """
    Parameters for querying funding rates.
    """

    product_ids: list


class IndexerPerpPricesParams(VertexBaseModel):
    """
    Parameters for querying perpetual prices.
    """

    product_id: int


class IndexerOraclePricesParams(VertexBaseModel):
    """
    Parameters for querying oracle prices.
    """

    product_ids: list[int]


class IndexerTokenRewardsParams(VertexBaseModel):
    """
    Parameters for querying token rewards.
    """

    address: str


class IndexerMakerStatisticsParams(VertexBaseModel):
    """
    Parameters for querying maker statistics.
    """

    product_id: int
    epoch: int
    interval: int


class IndexerLiquidationFeedParams(VertexBaseModel):
    """
    Parameters for querying liquidation feed.
    """

    pass


class IndexerLinkedSignerRateLimitParams(VertexBaseModel):
    """
    Parameters for querying linked signer rate limits.
    """

    subaccount: str


class IndexerReferralCodeParams(VertexBaseModel):
    """
    Parameters for querying a referral code.
    """

    subaccount: str


class IndexerSubaccountsParams(VertexBaseModel):
    """
    Parameters for querying subaccounts.
    """

    address: Optional[str]
    limit: Optional[int]
    start: Optional[int]


IndexerParams = Union[
    IndexerSubaccountHistoricalOrdersParams,
    IndexerHistoricalOrdersByDigestParams,
    IndexerMatchesParams,
    IndexerEventsParams,
    IndexerSubaccountSummaryParams,
    IndexerProductSnapshotsParams,
    IndexerCandlesticksParams,
    IndexerFundingRateParams,
    IndexerPerpPricesParams,
    IndexerOraclePricesParams,
    IndexerTokenRewardsParams,
    IndexerMakerStatisticsParams,
    IndexerLiquidationFeedParams,
    IndexerLinkedSignerRateLimitParams,
    IndexerReferralCodeParams,
    IndexerSubaccountsParams,
]


class IndexerHistoricalOrdersRequest(VertexBaseModel):
    """
    Request object for querying historical orders.
    """

    orders: Union[
        IndexerSubaccountHistoricalOrdersParams, IndexerHistoricalOrdersByDigestParams
    ]


class IndexerMatchesRequest(VertexBaseModel):
    """
    Request object for querying matches.
    """

    matches: IndexerMatchesParams


class IndexerEventsRequest(VertexBaseModel):
    """
    Request object for querying events.
    """

    events: IndexerEventsParams


class IndexerSubaccountSummaryRequest(VertexBaseModel):
    """
    Request object for querying subaccount summary.
    """

    summary: IndexerSubaccountSummaryParams


class IndexerProductSnapshotsRequest(VertexBaseModel):
    """
    Request object for querying product snapshots.
    """

    products: IndexerProductSnapshotsParams


class IndexerCandlesticksRequest(VertexBaseModel):
    """
    Request object for querying candlestick data.
    """

    candlesticks: IndexerCandlesticksParams


class IndexerFundingRateRequest(VertexBaseModel):
    """
    Request object for querying funding rates.
    """

    funding_rate: IndexerFundingRateParams


class IndexerFundingRatesRequest(VertexBaseModel):
    """
    Request object for querying funding rates.
    """

    funding_rates: IndexerFundingRatesParams


class IndexerPerpPricesRequest(VertexBaseModel):
    """
    Request object for querying perpetual prices.
    """

    price: IndexerPerpPricesParams


class IndexerOraclePricesRequest(VertexBaseModel):
    """
    Request object for querying oracle prices.
    """

    oracle_price: IndexerOraclePricesParams


class IndexerTokenRewardsRequest(VertexBaseModel):
    """
    Request object for querying token rewards.
    """

    rewards: IndexerTokenRewardsParams


class IndexerMakerStatisticsRequest(VertexBaseModel):
    """
    Request object for querying maker statistics.
    """

    maker_statistics: IndexerMakerStatisticsParams


class IndexerLiquidationFeedRequest(VertexBaseModel):
    """
    Request object for querying liquidation feed.
    """

    liquidation_feed: IndexerLiquidationFeedParams


class IndexerLinkedSignerRateLimitRequest(VertexBaseModel):
    """
    Request object for querying linked signer rate limits.
    """

    linked_signer_rate_limit: IndexerLinkedSignerRateLimitParams


class IndexerReferralCodeRequest(VertexBaseModel):
    """
    Request object for querying a referral code.
    """

    referral_code: IndexerReferralCodeParams


class IndexerSubaccountsRequest(VertexBaseModel):
    """
    Request object for querying subaccounts.
    """

    subaccounts: IndexerSubaccountsParams


IndexerRequest = Union[
    IndexerHistoricalOrdersRequest,
    IndexerMatchesRequest,
    IndexerEventsRequest,
    IndexerSubaccountSummaryRequest,
    IndexerProductSnapshotsRequest,
    IndexerCandlesticksRequest,
    IndexerFundingRateRequest,
    IndexerPerpPricesRequest,
    IndexerOraclePricesRequest,
    IndexerTokenRewardsRequest,
    IndexerMakerStatisticsRequest,
    IndexerLiquidationFeedRequest,
    IndexerLinkedSignerRateLimitRequest,
    IndexerReferralCodeRequest,
    IndexerSubaccountsRequest,
]


class IndexerHistoricalOrdersData(VertexBaseModel):
    """
    Data object for historical orders.
    """

    orders: list[IndexerHistoricalOrder]


class IndexerMatchesData(VertexBaseModel):
    """
    Data object for matches.
    """

    matches: list[IndexerMatch]
    txs: list[IndexerTx]


class IndexerEventsData(VertexBaseModel):
    """
    Data object for events.
    """

    events: list[IndexerEvent]
    txs: list[IndexerTx]


class IndexerSubaccountSummaryData(VertexBaseModel):
    """
    Data object for subaccount summary.
    """

    events: list[IndexerEvent]


class IndexerProductSnapshotsData(VertexBaseModel):
    """
    Data object for product snapshots.
    """

    products: list[IndexerProduct]
    txs: list[IndexerTx]


class IndexerCandlesticksData(VertexBaseModel):
    """
    Data object for candlestick data.
    """

    candlesticks: list[IndexerCandlestick]


class IndexerFundingRateData(VertexBaseModel):
    """
    Data object for funding rates.
    """

    product_id: int
    funding_rate_x18: str
    update_time: str


IndexerFundingRatesData = Dict[str, IndexerFundingRateData]


class IndexerPerpPricesData(VertexBaseModel):
    """
    Data object for perpetual prices.
    """

    product_id: int
    index_price_x18: str
    mark_price_x18: str
    update_time: str


class IndexerOraclePricesData(VertexBaseModel):
    """
    Data object for oracle prices.
    """

    prices: list[IndexerOraclePrice]


class IndexerTokenRewardsData(VertexBaseModel):
    """
    Data object for token rewards.
    """

    rewards: list[IndexerTokenReward]
    update_time: str
    total_referrals: str


class IndexerMakerStatisticsData(VertexBaseModel):
    """
    Data object for maker statistics.
    """

    reward_coefficient: float
    makers: list[IndexerMarketMaker]


class IndexerLinkedSignerRateLimitData(VertexBaseModel):
    """
    Data object for linked signer rate limits.
    """

    remaining_tx: str
    total_tx_limit: str
    wait_time: int
    signer: str


class IndexerReferralCodeData(VertexBaseModel):
    """
    Data object for referral codes.
    """

    referral_code: str


class IndexerSubaccountsData(VertexBaseModel):
    """
    Data object for subaccounts response from the indexer.
    """

    subaccounts: list[IndexerSubaccount]


IndexerLiquidationFeedData = list[IndexerLiquidatableAccount]


IndexerResponseData = Union[
    IndexerHistoricalOrdersData,
    IndexerMatchesData,
    IndexerEventsData,
    IndexerSubaccountSummaryData,
    IndexerProductSnapshotsData,
    IndexerCandlesticksData,
    IndexerFundingRateData,
    IndexerPerpPricesData,
    IndexerOraclePricesData,
    IndexerTokenRewardsData,
    IndexerMakerStatisticsData,
    IndexerLinkedSignerRateLimitData,
    IndexerReferralCodeData,
    IndexerSubaccountsData,
    IndexerLiquidationFeedData,
    IndexerFundingRatesData,
]


class IndexerResponse(VertexBaseModel):
    """
    Represents the response returned by the indexer.

    Attributes:
        data (IndexerResponseData): The data contained in the response.
    """

    data: IndexerResponseData


def to_indexer_request(params: IndexerParams) -> IndexerRequest:
    """
    Converts an IndexerParams object to the corresponding IndexerRequest object.

    Args:
        params (IndexerParams): The IndexerParams object to convert.

    Returns:
        IndexerRequest: The converted IndexerRequest object.
    """
    indexer_request_mapping = {
        IndexerSubaccountHistoricalOrdersParams: (
            IndexerHistoricalOrdersRequest,
            IndexerQueryType.ORDERS.value,
        ),
        IndexerHistoricalOrdersByDigestParams: (
            IndexerHistoricalOrdersRequest,
            IndexerQueryType.ORDERS.value,
        ),
        IndexerMatchesParams: (IndexerMatchesRequest, IndexerQueryType.MATCHES.value),
        IndexerEventsParams: (IndexerEventsRequest, IndexerQueryType.EVENTS.value),
        IndexerSubaccountSummaryParams: (
            IndexerSubaccountSummaryRequest,
            IndexerQueryType.SUMMARY.value,
        ),
        IndexerProductSnapshotsParams: (
            IndexerProductSnapshotsRequest,
            IndexerQueryType.PRODUCTS.value,
        ),
        IndexerCandlesticksParams: (
            IndexerCandlesticksRequest,
            IndexerQueryType.CANDLESTICKS.value,
        ),
        IndexerFundingRateParams: (
            IndexerFundingRateRequest,
            IndexerQueryType.FUNDING_RATE.value,
        ),
        IndexerFundingRatesParams: (
            IndexerFundingRatesRequest,
            IndexerQueryType.FUNDING_RATES.value,
        ),
        IndexerPerpPricesParams: (
            IndexerPerpPricesRequest,
            IndexerQueryType.PERP_PRICES.value,
        ),
        IndexerOraclePricesParams: (
            IndexerOraclePricesRequest,
            IndexerQueryType.ORACLE_PRICES.value,
        ),
        IndexerTokenRewardsParams: (
            IndexerTokenRewardsRequest,
            IndexerQueryType.REWARDS.value,
        ),
        IndexerMakerStatisticsParams: (
            IndexerMakerStatisticsRequest,
            IndexerQueryType.MAKER_STATISTICS.value,
        ),
        IndexerLiquidationFeedParams: (
            IndexerLiquidationFeedRequest,
            IndexerQueryType.LIQUIDATION_FEED.value,
        ),
        IndexerLinkedSignerRateLimitParams: (
            IndexerLinkedSignerRateLimitRequest,
            IndexerQueryType.LINKED_SIGNER_RATE_LIMIT.value,
        ),
        IndexerReferralCodeParams: (
            IndexerReferralCodeRequest,
            IndexerQueryType.REFERRAL_CODE.value,
        ),
        IndexerSubaccountsParams: (
            IndexerSubaccountsRequest,
            IndexerQueryType.SUBACCOUNTS.value,
        ),
    }

    RequestClass, field_name = indexer_request_mapping[type(params)]
    return RequestClass(**{field_name: params})
