import os
import time

from vertex_protocol.client import create_vertex_client
from vertex_protocol.engine_client.types.execute import (
    BurnLpParams,
    MintLpParams,
    OrderParams,
    SubaccountParams,
    WithdrawCollateralParams,
)
from vertex_protocol.engine_client.types.query import QueryMaxOrderSizeParams
from vertex_protocol.utils.bytes32 import subaccount_to_bytes32, subaccount_to_hex
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce


private_key = os.getenv("PRIVATE_KEY")


def run():
    print("setting up vertex client...")
    client = create_vertex_client("testnet", private_key)

    print("minting test tokens...")
    mint_tx_hash = client.spot._mint_mock_erc20(0, to_pow_10(1, 6))
    print("mint tx hash:", mint_tx_hash)

    print("approving allowance...")
    approve_allowance_tx_hash = client.spot.approve_allowance(0, to_pow_10(1, 6))
    print("approve allowance tx hash:", approve_allowance_tx_hash)

    print("querying my allowance...")
    token_allowance = client.spot.get_token_allowance(0, client.context.signer.address)
    print("token allowance:", token_allowance)

    print("depositing collateral...")
    deposit_tx_hash = client.spot.deposit(
        {"subaccount_name": "default", "product_id": 0, "amount": to_pow_10(1, 6)}
    )
    print("deposit collateral tx hash:", deposit_tx_hash)

    print("querying my token balance...")
    token_balance = client.spot.get_token_wallet_balance(
        1, client.context.signer.address
    )
    print("my token balance:", token_balance)

    owner = client.context.engine_client.signer.address
    print("placing order...")
    product_id = 1
    order = OrderParams(
        sender=SubaccountParams(
            subaccount_owner=owner,
            subaccount_name="default",
        ),
        priceX18=to_x18(20000),
        amount=to_pow_10(1, 17),
        expiration=get_expiration_timestamp(OrderType.POST_ONLY, int(time.time()) + 40),
        nonce=gen_order_nonce(),
    )
    res = client.market.place_order({"product_id": product_id, "order": order})
    print("order result:", res.json(indent=2))

    sender = subaccount_to_hex(order.sender)
    order.sender = subaccount_to_bytes32(order.sender)
    order_digest = client.context.engine_client.get_order_digest(order, product_id)
    print("order digest:", order_digest)

    print("querying open orders...")
    open_orders = client.market.get_subaccount_open_orders(1, sender)
    print("open orders:", open_orders.json(indent=2))

    print("querying subaccount summary...")
    subaccount_summary = client.subaccount.get_engine_subaccount_summary(sender)
    print("subaccount summary:", subaccount_summary.json(indent=2))

    print("cancelling order...")
    res = client.market.cancel_orders(
        {"productIds": [product_id], "digests": [order_digest]}
    )
    print("cancel order result:", res.json(indent=2))

    print("querying open orders after cancel...")
    open_orders = client.market.get_subaccount_open_orders(1, sender)
    print("open orders:", open_orders.json(indent=2))

    print("placing multiple orders...")
    for product_id in [1, 2]:
        order.nonce = gen_order_nonce()
        res = client.market.place_order({"product_id": product_id, "order": order})
        print("order result:", res.json(indent=2))

    print("cancelling product orders...")
    res = client.market.cancel_product_orders({"productIds": [1, 2]})
    print("cancel product orders results:", res.json(indent=2))

    for product_id in [1, 2]:
        print(
            f"querying open orders after cancel product orders product_id={product_id}..."
        )
        open_orders = client.market.get_subaccount_open_orders(product_id, sender)
        print("open orders:", open_orders.json(indent=2))

    print("querying historical orders...")
    historical_orders = client.market.get_subaccount_historical_orders(
        {"subaccount": sender, "limit": 2}
    )
    print("subaccount historical orders:", historical_orders.json(indent=2))

    print("querying all engine markets...")
    engine_markets = client.market.get_all_engine_markets()
    print("engine markets:", engine_markets.json(indent=2))

    print("querying market liquidity...")
    market_liquidity = client.market.get_market_liquidity(1, 2)
    print("market liquidity:", market_liquidity.json(indent=2))

    print("querying latest market price...")
    latest_market_price = client.market.get_latest_market_price(1)
    print("latest market price:", latest_market_price.json(indent=2))

    print("querying max order size...")
    max_order_size = client.market.get_max_order_size(
        QueryMaxOrderSizeParams(
            sender=sender, product_id=product_id, price_x18=30000, direction="short"
        )
    )
    print("max order size:", max_order_size.json(indent=2))

    print("querying max lp mintable...")
    max_lp_mintable = client.market.get_max_lp_mintable(1, sender)
    print("max lp mintable:", max_lp_mintable.json(indent=2))

    print("querying candlesticks...")
    candlesticks = client.market.get_candlesticks(
        {"product_id": 1, "granularity": 300, "limit": 2}
    )
    print("candlesticks:", candlesticks.json(indent=2))

    print("querying funding rate...")
    funding_rate = client.market.get_perp_funding_rate(2)
    print("funding rate:", funding_rate.json(indent=2))

    print("querying product snapshots...")
    product_snapshots = client.market.get_product_snapshots(
        {"product_id": 1, "limit": 2}
    )
    print("product snapshots:", product_snapshots.json(indent=2))

    print("querying perp prices...")
    perp_prices = client.perp.get_prices(2)
    print("perp prices:", perp_prices.json(indent=2))

    print("minting lp...")
    mint_lp_params = MintLpParams(
        sender=SubaccountParams(
            subaccount_owner=client.context.engine_client.signer.address,
            subaccount_name="default",
        ),
        productId=3,
        amountBase=to_x18(1),
        quoteAmountLow=to_x18(1000),
        quoteAmountHigh=to_x18(2000),
    )
    res = client.market.mint_lp(mint_lp_params)
    print("mint lp results:", res.json(indent=2))

    print("burning lp...")
    burn_lp_params = BurnLpParams(
        sender=SubaccountParams(
            subaccount_owner=client.context.engine_client.signer.address,
            subaccount_name="default",
        ),
        productId=3,
        amount=to_x18(1),
        nonce=client.context.engine_client.tx_nonce(),
    )
    res = client.market.burn_lp(burn_lp_params)
    print("burn lp result:", res.json(indent=2))

    print("querying subaccount fee rates...")
    fee_rates = client.subaccount.get_subaccount_fee_rates(sender)
    print("fee rates:", fee_rates.json(indent=2))

    print("querying subaccount token rewards...")
    token_rewards = client.subaccount.get_subaccount_token_rewards(owner)
    print("token rewards:", token_rewards.json(indent=2))

    print("querying subaccount linked signer rate limits...")
    linked_signer_rate_limits = (
        client.subaccount.get_subaccount_linked_signer_rate_limits(sender)
    )
    print("linked signer rate limits:", linked_signer_rate_limits.json(indent=2))

    print("querying max withdrawable...")
    max_withdrawable = client.spot.get_max_withdrawable(1, sender)
    print("max withdrawable:", max_withdrawable.json(indent=2))

    print("withdrawing collateral...")
    withdraw_collateral_params = WithdrawCollateralParams(
        productId=0, amount=to_pow_10(1, 6)
    )
    res = client.spot.withdraw(withdraw_collateral_params)
    print("withdraw result:", res.json(indent=2))
