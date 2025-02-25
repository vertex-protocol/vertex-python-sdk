import time
from sanity import CLIENT_MODE, SIGNER_PRIVATE_KEY

from vertex_protocol.client import VertexClient, create_vertex_client
from vertex_protocol.contracts.types import DepositCollateralParams
from vertex_protocol.engine_client.types.models import SpotProductBalance
from vertex_protocol.utils.bytes32 import subaccount_to_hex
from vertex_protocol.utils.execute import IsolatedOrderParams
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import SubaccountParams


def run():
    print("setting up vertex client...")
    client: VertexClient = create_vertex_client(CLIENT_MODE, SIGNER_PRIVATE_KEY)

    print("chain_id:", client.context.engine_client.get_contracts().chain_id)

    print("minting test tokens...")
    mint_tx_hash = client.spot._mint_mock_erc20(0, to_pow_10(100000, 6))
    print("mint tx hash:", mint_tx_hash)

    print("approving allowance...")
    approve_allowance_tx_hash = client.spot.approve_allowance(0, to_pow_10(100000, 6))
    print("approve allowance tx hash:", approve_allowance_tx_hash)

    print("querying my allowance...")
    token_allowance = client.spot.get_token_allowance(0, client.context.signer.address)
    print("token allowance:", token_allowance)

    print("depositing collateral...")
    deposit_tx_hash = client.spot.deposit(
        DepositCollateralParams(
            subaccount_name="default", product_id=0, amount=to_pow_10(100000, 6)
        )
    )
    print("deposit collateral tx hash:", deposit_tx_hash)

    subaccount = subaccount_to_hex(client.context.signer.address, "default")

    usdc_balance: SpotProductBalance = client.subaccount.get_engine_subaccount_summary(
        subaccount
    ).parse_subaccount_balance(0)
    while int(usdc_balance.balance.amount) == 0:
        print("waiting for deposit...")
        usdc_balance: SpotProductBalance = (
            client.subaccount.get_engine_subaccount_summary(
                subaccount
            ).parse_subaccount_balance(0)
        )
        time.sleep(1)

    order_price = 95_000

    owner = client.context.engine_client.signer.address
    print("placing isolated order...")
    product_id = 2
    isolated_order = IsolatedOrderParams(
        sender=SubaccountParams(
            subaccount_owner=owner,
            subaccount_name="default",
        ),
        priceX18=to_x18(order_price),
        amount=to_pow_10(1, 17),
        expiration=get_expiration_timestamp(OrderType.IOC, int(time.time()) + 40),
        nonce=gen_order_nonce(),
        margin=to_pow_10(1000, 18),
    )
    res = client.market.place_isolated_order(
        {"product_id": product_id, "isolated_order": isolated_order}
    )
    print("order result:", res.json(indent=2))

    print("querying isolated positions...")
    isolated_positions = client.market.get_isolated_positions(subaccount)
    print("isolated positions:", isolated_positions.json(indent=2))

    print("querying historical isolated orders...")
    historical_isolated_orders = client.market.get_subaccount_historical_orders(
        {"subaccount": subaccount, "isolated": True}
    )
    print("historical isolated orders:", historical_isolated_orders.json(indent=2))

    print("querying isolated matches...")
    isolated_matches = client.context.indexer_client.get_matches(
        {"subaccount": subaccount, "isolated": True}
    )
    print("isolated matches:", isolated_matches.json(indent=2))

    print("querying isolated events...")
    isolated_events = client.context.indexer_client.get_events(
        {"subaccount": subaccount, "limit": {"raw": 5}, "isolated": True}
    )
    print("isolated events:", isolated_events.json(indent=2))
