from pydantic import BaseModel, AnyUrl, validator
from vertex_protocol.indexer_client.types.models import *
from vertex_protocol.indexer_client.types.query import *


class IndexerClientOpts(BaseModel):
    """
    Model representing the options for the Indexer Client
    """

    url: AnyUrl

    @validator("url")
    def clean_url(cls, v: AnyUrl) -> str:
        return v.rstrip("/")


__all__ = [
    "IndexerQueryType",
    "IndexerBaseParams",
    "IndexerSubaccountHistoricalOrdersParams",
    "IndexerHistoricalOrdersByDigestParams",
    "IndexerMatchesParams",
    "IndexerEventsRawLimit",
    "IndexerEventsTxsLimit",
    "IndexerEventsLimit",
    "IndexerEventsParams",
    "IndexerSubaccountSummaryParams",
    "IndexerProductSnapshotsParams",
    "IndexerCandlesticksParams",
    "IndexerFundingRateParams",
    "IndexerPerpPricesParams",
    "IndexerOraclePricesParams",
    "IndexerTokenRewardsParams",
    "IndexerMakerStatisticsParams",
    "IndexerLiquidationFeedParams",
    "IndexerLinkedSignerRateLimitParams",
    "IndexerReferralCodeParams",
    "IndexerSubaccountsParams",
    "IndexerParams",
    "IndexerHistoricalOrdersRequest",
    "IndexerMatchesRequest",
    "IndexerEventsRequest",
    "IndexerSubaccountSummaryRequest",
    "IndexerProductSnapshotsRequest",
    "IndexerCandlesticksRequest",
    "IndexerFundingRateRequest",
    "IndexerFundingRatesRequest",
    "IndexerPerpPricesRequest",
    "IndexerOraclePricesRequest",
    "IndexerTokenRewardsRequest",
    "IndexerMakerStatisticsRequest",
    "IndexerLiquidationFeedRequest",
    "IndexerLinkedSignerRateLimitRequest",
    "IndexerReferralCodeRequest",
    "IndexerSubaccountsRequest",
    "IndexerRequest",
    "IndexerHistoricalOrdersData",
    "IndexerMatchesData",
    "IndexerEventsData",
    "IndexerSubaccountSummaryData",
    "IndexerProductSnapshotsData",
    "IndexerCandlesticksData",
    "IndexerFundingRateData",
    "IndexerPerpPricesData",
    "IndexerOraclePricesData",
    "IndexerTokenRewardsData",
    "IndexerMakerStatisticsData",
    "IndexerLinkedSignerRateLimitData",
    "IndexerReferralCodeData",
    "IndexerSubaccountsData",
    "IndexerLiquidationFeedData",
    "IndexerResponseData",
    "IndexerResponse",
    "IndexerEventType",
    "IndexerCandlesticksGranularity",
    "IndexerBaseModel",
    "IndexerBaseOrder",
    "IndexerOrderFill",
    "IndexerHistoricalOrder",
    "IndexerSignedOrder",
    "IndexerMatch",
    "IndexerMatchOrdersTxData",
    "IndexerMatchOrdersTx",
    "IndexerWithdrawCollateralTxData",
    "IndexerWithdrawCollateralTx",
    "IndexerLiquidateSubaccountTxData",
    "IndexerLiquidateSubaccountTx",
    "IndexerMintLpTxData",
    "IndexerMintLpTx",
    "IndexerBurnLpTxData",
    "IndexerBurnLpTx",
    "IndexerTxData",
    "IndexerTx",
    "IndexerSpotProductBalanceData",
    "IndexerSpotProductData",
    "IndexerPerpProductData",
    "IndexerProductData",
    "IndexerEventTrackedData",
    "IndexerEvent",
    "IndexerProduct",
    "IndexerCandlestick",
    "IndexerOraclePrice",
    "IndexerAddressReward",
    "IndexerGlobalRewards",
    "IndexerTokenReward",
    "IndexerMarketMakerData",
    "IndexerMarketMaker",
    "IndexerLiquidatableAccount",
    "IndexerSubaccount",
    "IndexerUsdcPriceData",
    "IndexerInterestAndFundingParams",
    "IndexerInterestAndFundingRequest",
    "IndexerInterestAndFundingData",
    "IndexerTickerInfo",
    "IndexerPerpContractInfo",
    "IndexerTradeInfo",
    "VrtxTokenQueryType",
    "IndexerTickersData",
    "IndexerPerpContractsData",
    "IndexerHistoricalTradesData",
]
