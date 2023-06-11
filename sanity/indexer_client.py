import json

from eth_account import Account
from sanity import INDEXER_BACKEND_URL, SIGNER_PRIVATE_KEY
from vertex_protocol.indexer_client import IndexerClient
from vertex_protocol.indexer_client.types.models import (
    IndexerCandlesticksGranularity,
    IndexerEventType,
)
from vertex_protocol.indexer_client.types.query import (
    IndexerCandlesticksParams,
    IndexerEventsParams,
    IndexerEventsRawLimit,
    IndexerMatchesParams,
    IndexerSubaccountHistoricalOrdersParams,
)
from vertex_protocol.utils.bytes32 import subaccount_to_hex
from vertex_protocol.utils.subaccount import SubaccountParams


def run():
    print("setting up indexer client...")
    client = IndexerClient(opts={"url": INDEXER_BACKEND_URL})

    owner = Account.from_key(SIGNER_PRIVATE_KEY).address
    subaccount = subaccount_to_hex(
        SubaccountParams(subaccount_owner=owner, subaccount_name="default")
    )
    print("subaccount:", subaccount)

    print("querying subaccount historical orders...")
    subaccount_historical_orders = client.get_subaccount_historical_orders(
        IndexerSubaccountHistoricalOrdersParams(subaccount=subaccount, limit=3)
    )
    print("subaccount historical orders:", subaccount_historical_orders.json(indent=2))

    digests = [order.digest for order in subaccount_historical_orders.orders][:2]
    print("querying historical orders by digests...", digests)
    historical_orders_by_digest = client.get_historical_orders_by_digest(digests)
    print("historical orders by digest:", historical_orders_by_digest.json(indent=2))

    print("querying matches by product...")
    last_spot_matches = client.get_matches(
        IndexerMatchesParams(product_ids=[1, 3], limit=2)
    )
    print("last spot matches:", last_spot_matches.json(indent=2))

    print("querying subaccount matches...")
    subaccount_matches = client.get_matches(
        IndexerMatchesParams(subaccount=subaccount, limit=2, product_ids=[1])
    )
    print("subaccount matches:", subaccount_matches.json(indent=2))

    print("querying collateral events...")
    collateral_events = client.get_events(
        IndexerEventsParams(
            event_types=[
                IndexerEventType.DEPOSIT_COLLATERAL,
                IndexerEventType.WITHDRAW_COLLATERAL,
            ],
            limit=IndexerEventsRawLimit(raw=3),
        )
    )
    print("collateral events:", collateral_events.json(indent=2))

    print("querying subaccount events...")
    subaccount_events = client.get_events(
        params={"subaccount": subaccount, "limit": {"raw": 2}}
    )
    print("subaccount events:", subaccount_events.json(indent=2))

    print("querying subaccount summary...")
    subaccount_summary = client.get_subaccount_summary(subaccount)
    print("subaccount summary:", subaccount_summary.json(indent=2))

    print("querying product snapshots...")
    btc_snapshots = client.get_product_snapshots({"product_id": 1, "limit": 3})
    print("btc snapshots:", btc_snapshots.json(indent=2))

    print("querying candlesticks...")
    candlesticks = client.get_candlesticks(
        IndexerCandlesticksParams(
            product_id=1,
            granularity=IndexerCandlesticksGranularity.FIVE_MINUTES,
            limit=3,
        )
    )
    print("candlesticks:", candlesticks.json(indent=2))

    print("querying perp funding rate...")
    btc_perp_funding_rate = client.get_perp_funding_rate(2)
    print("btc-perp funding rate:", btc_perp_funding_rate.json(indent=2))

    print("querying perp prices...")
    eth_perp_prices = client.get_perp_prices(4)
    print("eth-perp prices:", eth_perp_prices.json(indent=2))

    print("querying oracle prices...")
    oracle_prices = client.get_oracle_prices(product_ids=[1, 2])
    print("oracle prices:", oracle_prices.json(indent=2))

    print("querying token rewards...")
    token_rewards = client.get_token_rewards(owner)
    print("token rewards:", token_rewards.json(indent=2))

    print("querying maker stats...")
    maker_stats = client.get_maker_statistics(
        {"product_id": 1, "epoch": 2, "interval": 10000}
    )
    print("maker stats:", maker_stats.json(indent=2))

    print("querying liquidation feed...")
    liquidation_feed = client.get_liquidation_feed()
    print(
        "liquidation feed:",
        json.dumps([acc.dict() for acc in liquidation_feed], indent=2),
    )

    print("querying linked signer rate limit...")
    linked_signer_rate_limit = client.get_linked_signer_rate_limits(subaccount)
    print("linked signer rate limit:", linked_signer_rate_limit.json(indent=2))
