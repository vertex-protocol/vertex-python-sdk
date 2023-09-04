from unittest.mock import MagicMock

from vertex_protocol.indexer_client import IndexerClient
from vertex_protocol.indexer_client.types.query import (
    IndexerCandlesticksParams,
    IndexerCandlesticksRequest,
    IndexerEventsParams,
    IndexerFundingRateRequest,
    IndexerHistoricalOrdersRequest,
    IndexerLinkedSignerRateLimitRequest,
    IndexerLiquidationFeedRequest,
    IndexerMakerStatisticsParams,
    IndexerMakerStatisticsRequest,
    IndexerMatchesParams,
    IndexerMatchesRequest,
    IndexerOraclePricesRequest,
    IndexerPerpPricesRequest,
    IndexerProductSnapshotsParams,
    IndexerProductSnapshotsRequest,
    IndexerSubaccountHistoricalOrdersParams,
    IndexerSubaccountSummaryRequest,
    IndexerReferralCodeRequest,
    IndexerBaseParams,
    IndexerTokenRewardsRequest,
)


def test_indexer_obj_query_params(
    mock_post: MagicMock,
    url: str,
):
    indexer_client = IndexerClient({"url": url})

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"orders": []}
    mock_post.return_value = mock_response

    indexer_client.get_subaccount_historical_orders(
        IndexerSubaccountHistoricalOrdersParams(subaccount="xxx")
    )
    indexer_client.get_historical_orders_by_digest([])

    mock_response.json.return_value = {"matches": [], "txs": []}
    mock_post.return_value = mock_response
    indexer_client.get_matches(IndexerMatchesParams(subaccount="xxx"))

    mock_response.json.return_value = {"events": [], "txs": []}
    mock_post.return_value = mock_response
    indexer_client.get_events(IndexerEventsParams(submission_idx=10))

    mock_response.json.return_value = {"events": []}
    mock_post.return_value = mock_response
    indexer_client.get_subaccount_summary("xxx")

    mock_response.json.return_value = {"products": [], "txs": []}
    mock_post.return_value = mock_response
    indexer_client.get_product_snapshots(IndexerProductSnapshotsParams(product_id=1))

    mock_response.json.return_value = {"candlesticks": []}
    mock_post.return_value = mock_response
    indexer_client.get_candlesticks(
        IndexerCandlesticksParams(granularity=60, product_id=1)
    )

    mock_response.json.return_value = {
        "product_id": 1,
        "funding_rate_x18": "0",
        "update_time": "0",
    }
    mock_post.return_value = mock_response
    indexer_client.get_perp_funding_rate(product_id=1)

    mock_response.json.return_value = {
        "product_id": 1,
        "index_price_x18": "0",
        "mark_price_x18": "0",
        "update_time": "0",
    }
    mock_post.return_value = mock_response
    indexer_client.get_perp_prices(product_id=1)

    mock_response.json.return_value = {"prices": []}
    mock_post.return_value = mock_response
    indexer_client.get_oracle_prices([])

    mock_response.json.return_value = {
        "rewards": [],
        "update_time": "0",
        "total_referrals": "0",
    }
    mock_post.return_value = mock_response
    indexer_client.get_token_rewards("xxx")

    mock_response.json.return_value = {"reward_coefficient": 0.0, "makers": []}
    mock_post.return_value = mock_response
    indexer_client.get_maker_statistics(
        IndexerMakerStatisticsParams(product_id=1, epoch=1, interval=1)
    )

    mock_response.json.return_value = []
    mock_post.return_value = mock_response
    indexer_client.get_liquidation_feed()

    mock_response.json.return_value = {
        "remaining_tx": "0",
        "total_tx_limit": "0",
        "wait_time": 0,
        "signer": "xxx",
    }
    mock_post.return_value = mock_response
    indexer_client.get_linked_signer_rate_limits("xxx")

    mock_response.json.return_value = {"referral_code": "vertex"}
    mock_post.return_value = mock_response
    indexer_client.get_referral_code("xxx")


def test_indexer_raw_query_params(
    mock_post: MagicMock,
    url: str,
):
    indexer_client = IndexerClient({"url": url})

    mock_response = MagicMock()
    mock_response.status_code = 200

    mock_response.json.return_value = {"orders": []}
    mock_post.return_value = mock_response
    indexer_client.get_subaccount_historical_orders({"subaccount": "xxx"})

    mock_response.json.return_value = {"matches": [], "txs": []}
    mock_post.return_value = mock_response
    indexer_client.get_matches({"subaccount": "xxx"})

    mock_response.json.return_value = {"events": [], "txs": []}
    mock_post.return_value = mock_response
    indexer_client.get_events({"submission_idx": 10})

    mock_response.json.return_value = {"products": [], "txs": []}
    mock_post.return_value = mock_response
    indexer_client.get_product_snapshots({"product_id": 1})

    mock_response.json.return_value = {"candlesticks": []}
    mock_post.return_value = mock_response
    indexer_client.get_candlesticks({"granularity": 60, "product_id": 1})

    mock_response.json.return_value = {"reward_coefficient": 0.0, "makers": []}
    mock_post.return_value = mock_response
    indexer_client.get_maker_statistics({"product_id": 1, "epoch": 1, "interval": 1})


def test_indexer_request_params(
    mock_post: MagicMock,
    url: str,
):
    indexer_client = IndexerClient({"url": url})

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_post.return_value = mock_response

    indexer_client.query({"orders": {"subaccount": "xxx"}})
    indexer_client.query(IndexerHistoricalOrdersRequest(orders={"subaccount": "xxx"}))

    indexer_client.query({"matches": {"subaccount": "xxx"}})
    indexer_client.query(IndexerMatchesRequest(matches={"subaccount": "xxx"}))

    indexer_client.query({"events": {"subaccount": "xxx"}})
    indexer_client.query(IndexerEventsParams(events={"subaccount": "xxx"}))

    indexer_client.query({"summary": {"subaccount": "xxx"}})
    indexer_client.query(IndexerSubaccountSummaryRequest(summary={"subaccount": "xxx"}))

    indexer_client.query({"products": {"product_id": 1}})
    indexer_client.query(IndexerProductSnapshotsRequest(products={"product_id": 1}))

    indexer_client.query({"candlesticks": {"granularity": 300, "product_id": 1}})
    indexer_client.query(
        IndexerCandlesticksRequest(candlesticks={"granularity": 300, "product_id": 1})
    )

    indexer_client.query({"funding_rate": {"product_id": 1}})
    indexer_client.query(IndexerFundingRateRequest(funding_rate={"product_id": 1}))

    indexer_client.query({"price": {"product_id": 1}})
    indexer_client.query(IndexerPerpPricesRequest(price={"product_id": 1}))

    indexer_client.query({"oracle_price": {"product_ids": [1]}})
    indexer_client.query(IndexerOraclePricesRequest(oracle_price={"product_ids": [1]}))

    indexer_client.query({"rewards": {"address": "xxx"}})
    indexer_client.query(IndexerTokenRewardsRequest(rewards={"address": "xxx"}))

    indexer_client.query(
        {"maker_statistics": {"product_id": 1, "epoch": 1, "interval": 1}}
    )
    indexer_client.query(
        IndexerMakerStatisticsRequest(
            maker_statistics={"product_id": 1, "epoch": 1, "interval": 1}
        )
    )

    indexer_client.query({"liquidation_feed": {}})
    indexer_client.query(IndexerLiquidationFeedRequest(liquidation_feed={}))

    indexer_client.query({"linked_signer_rate_limit": {"subaccount": "xxx"}})
    indexer_client.query(
        IndexerLinkedSignerRateLimitRequest(
            linked_signer_rate_limit={"subaccount": "xxx"}
        )
    )

    indexer_client.query({"referral_code": {"subaccount": "xxx"}})
    indexer_client.query(
        IndexerReferralCodeRequest(referral_code={"subaccount": "xxx"})
    )


def test_indexer_base_params():
    params_with_idx = IndexerBaseParams(idx=100)
    params_with_submission_idx = IndexerBaseParams(submission_idx=100)

    assert params_with_idx == params_with_submission_idx
