import time
from sanity import CLIENT_MODE, SIGNER_PRIVATE_KEY

from vertex_protocol.client import VertexClient, create_vertex_client
from vertex_protocol.contracts.types import DepositCollateralParams
from vertex_protocol.engine_client.types.execute import (
    BurnLpParams,
    CancelAndPlaceParams,
    MarketOrderParams,
    MintLpParams,
    OrderParams,
    PlaceMarketOrderParams,
    WithdrawCollateralParams,
)
from vertex_protocol.engine_client.types.models import SpotProductBalance
from vertex_protocol.engine_client.types.query import QueryMaxOrderSizeParams
from vertex_protocol.utils.bytes32 import subaccount_to_bytes32, subaccount_to_hex
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import round_x18, to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import SubaccountParams

btc_withdraw_fee = 40000000000000
usdc_withdraw_fee = 1000000


def assert_equal(a, b):
    assert a == b, f"expected {b} but got {a}"


def to_reduce_only(expiration):
    return expiration | (1 << 61)


def expiration_for_order_type(order_type: OrderType) -> int:
    return get_expiration_timestamp(order_type, int(time.time()) + 1000)


def place_order(
    client: VertexClient,
    subaccount: str,
    product_id: int,
    price: float,
    amount: float,
    expiration: int,
    nonce: int = gen_order_nonce(),
):
    order = OrderParams(
        sender=subaccount,
        priceX18=to_x18(price),
        amount=to_x18(amount),
        expiration=expiration,
        nonce=nonce,
    )
    client.market.place_order({"product_id": product_id, "order": order})
    # print("order result:", res.json(indent=2))


def withdraw_collateral(
    client: VertexClient, subaccount: str, product_id: int, amount: int
):
    withdraw_collateral_params = WithdrawCollateralParams(
        productId=product_id, amount=amount, sender=subaccount
    )
    client.spot.withdraw(withdraw_collateral_params)
    # print("withdraw result:", res.json(indent=2))


def pull_balances(
    client: VertexClient, subaccounts: list[int], product_ids: list[int]
) -> list[list[int]]:
    balances = []
    for subaccount in subaccounts:
        info = client.subaccount.get_engine_subaccount_summary(subaccount)
        sub_balances = []
        for product_id in product_ids:
            balance = [
                balance
                for balance in info.spot_balances + info.perp_balances
                if balance.product_id == product_id
            ][0]
            sub_balances.append(int(balance.balance.amount))
        balances.append(sub_balances)
    return balances


def run():
    print("setting up vertex client...")
    client: VertexClient = create_vertex_client(CLIENT_MODE, SIGNER_PRIVATE_KEY)

    print("minting quote test tokens...")
    mint_tx_hash = client.spot._mint_mock_erc20(0, to_pow_10(1000000, 6))
    print("mint tx hash:", mint_tx_hash)

    print("approving allowance...")
    approve_allowance_tx_hash = client.spot.approve_allowance(0, to_pow_10(1000000, 6))
    print("approve allowance tx hash:", approve_allowance_tx_hash)

    print("minting quote test tokens...")
    mint_tx_hash = client.spot._mint_mock_erc20(1, to_pow_10(99, 18))
    print("mint tx hash:", mint_tx_hash)

    print("approving allowance...")
    approve_allowance_tx_hash = client.spot.approve_allowance(1, to_pow_10(99, 18))
    print("approve allowance tx hash:", approve_allowance_tx_hash)

    print("depositing collateral (a1)...")
    deposit_tx_hash = client.spot.deposit(
        DepositCollateralParams(
            subaccount_name="a1", product_id=0, amount=to_pow_10(300000, 6)
        )
    )
    print("deposit collateral tx hash:", deposit_tx_hash)

    print("depositing collateral (a2)...")
    deposit_tx_hash = client.spot.deposit(
        DepositCollateralParams(
            subaccount_name="a2", product_id=1, amount=to_pow_10(10, 18)
        )
    )
    print("deposit collateral tx hash:", deposit_tx_hash)

    print("depositing collateral (a3)...")
    deposit_tx_hash = client.spot.deposit(
        DepositCollateralParams(
            subaccount_name="a3", product_id=1, amount=to_pow_10(10, 18)
        )
    )
    print("deposit collateral tx hash:", deposit_tx_hash)

    time.sleep(3)

    expiration_default = expiration_for_order_type(OrderType.DEFAULT)
    # expiration_ioc = expiration_for_order_type(OrderType.IOC)
    # expiration_fok = expiration_for_order_type(OrderType.FOK)
    expiration_post_only = expiration_for_order_type(OrderType.POST_ONLY)

    owner = client.context.engine_client.signer.address

    a1 = subaccount_to_hex(owner, "a1")
    a2 = subaccount_to_hex(owner, "a2")
    a3 = subaccount_to_hex(owner, "a3")

    print("initial balances:", pull_balances(client, [a1, a2, a3], [0, 1, 2]))

    # assert_equal(
    #     pull_balances(client, [a1, a2, a3], [0, 1, 2]),
    #     [[to_x18(300000), 0, 0], [0, to_x18(10), 0], [0, to_x18(10), 0]],
    # )

    non_taker_expirations = [expiration_default, expiration_post_only]
    owner = client.context.engine_client.signer.address

    # non-taker reduce only orders are rejected
    for non_taker_expirations in non_taker_expirations:
        for product_id in [1, 2]:
            try:
                place_order(
                    client,
                    a1,
                    product_id,
                    25000,
                    0.1,
                    to_reduce_only(non_taker_expirations),
                )
                print("panic panic!")
                exit(-1)
            except Exception as e:
                assert "Only taker orders can be set as reduce only" in str(e)

    # place_order(client, a1, 1, 25000, 11, expiration_default)

    # # reduce amount > position; (spots)
    # # should reduce position to 0.
    # place_order(client, a2, 1, 25000, -11, to_reduce_only(expiration_fok))

    # assert_equal(
    #     pull_balances(client, [a1, a2, a3], [1, 2]),
    #     [[to_x18(10), 0], [0, 0], [to_x18(10), 0]],
    # )

    # clean up
    senders = [a1, a2, a3]
    balances = pull_balances(client, [a1, a2, a3], [0, 1])
    for i in range(len(senders)):
        sender = senders[i]
        balance = balances[i]

        if balance[0] > 0:
            to_withdraw = (balance[0] / 10**12) - usdc_withdraw_fee
            print("withdrawing", to_withdraw)
            withdraw_collateral(client, sender, 0, to_withdraw)
        if balance[1] > 0:
            to_withdraw = balance[1] - btc_withdraw_fee
            print("withdrawing", to_withdraw)
            withdraw_collateral(client, sender, 1, to_withdraw)

    print("final balances:", pull_balances(client, [a1, a2, a3], [0, 1, 2]))
