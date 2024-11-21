import json
from pprint import pprint

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
    IndexerSubaccountsParams,
)
from vertex_protocol.utils.bytes32 import subaccount_to_hex
from vertex_protocol.utils.subaccount import SubaccountParams


def run():
    print("setting up indexer client...")
    client = IndexerClient(opts={"url": INDEXER_BACKEND_URL})

    print("querying spot tickers...")
    spot_tickers = client.get_tickers("spot")
    pprint(spot_tickers)

    print("querying perp tickers...")
    perp_tickers = client.get_tickers("perp")
    pprint(perp_tickers)

    print("querying perp contracts info...")
    perp_contracts = client.get_perp_contracts_info()
    pprint(perp_contracts)

    print("querying ETH-PERP historical trades...")
    eth_perp_trades = client.get_historical_trades("ETH-PERP_USDC", 2)
    pprint(eth_perp_trades)

    print("querying VRTX token total supply...")
    vrtx_total_supply = client.get_vrtx_token_info("total_supply")
    pprint(vrtx_total_supply)

    print("querying VRTX token circulating supply...")
    vrtx_circulating_supply = client.get_vrtx_token_info("circulating_supply")
    pprint(vrtx_circulating_supply)

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

    print("querying multi perps funding rates...")
    multi_perps_funding_rates = client.get_perp_funding_rates([2, 4])
    print("multi perps funding rates:", multi_perps_funding_rates)

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
    try:
        maker_stats = client.get_maker_statistics(
            {"product_id": 1, "epoch": 2, "interval": 10000}
        )
        print("maker stats:", maker_stats.json(indent=2))
    except Exception as e:
        # this endpoint fails locally when there's no epoch data.
        print("failed to retrieve maker stats with error:", e)

    print("querying liquidation feed...")
    liquidation_feed = client.get_liquidation_feed()
    print(
        "liquidation feed:",
        json.dumps([acc.dict() for acc in liquidation_feed], indent=2),
    )

    print("querying linked signer rate limit...")
    linked_signer_rate_limit = client.get_linked_signer_rate_limits(subaccount)
    print("linked signer rate limit:", linked_signer_rate_limit.json(indent=2))

    print("querying referral code...")
    referral_code = client.get_referral_code(subaccount=subaccount)
    print("referral code:", referral_code.json(indent=2))

    print("querying subaccounts...")
    subaccounts = client.get_subaccounts(
        IndexerSubaccountsParams(limit=2, start=0, address=owner)
    )
    print("subaccounts:", subaccounts.json(indent=2))

    print("querying usdc price...")
    usdc_price = client.get_usdc_price()
    print("usdc price", usdc_price.price_x18)

    print("querying vrtx merkle proofs...")
    print(owner)
    vrtx_merkle_proofs = client.get_vrtx_merkle_proofs(owner)
    print("vrtx merkle proofs:", vrtx_merkle_proofs.json(indent=2))

    print("querying foundation rewards merkle proofs...")
    foundation_rewards_merkle_proofs = client.get_foundation_rewards_merkle_proofs(
        owner
    )
    print(
        "foundation rewards merkle proofs:",
        foundation_rewards_merkle_proofs.json(indent=2),
    )
