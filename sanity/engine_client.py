from pprint import pprint
import time

from eth_account import Account
from eth_account.signers.local import LocalAccount

from sanity import ENGINE_BACKEND_URL, LINKED_SIGNER_PRIVATE_KEY, SIGNER_PRIVATE_KEY
from vertex_protocol.engine_client import EngineClient, EngineClientOpts
from vertex_protocol.engine_client.types.execute import (
    BurnLpParams,
    CancelOrdersParams,
    LinkSignerParams,
    LiquidateSubaccountParams,
    MintLpParams,
    PlaceOrderParams,
    OrderParams,
    WithdrawCollateralParams,
)
from vertex_protocol.engine_client.types.query import (
    QueryMaxOrderSizeParams,
)
from vertex_protocol.utils.bytes32 import (
    bytes32_to_hex,
    str_to_hex,
    subaccount_to_bytes32,
    zero_subaccount,
)
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import SubaccountParams


def run():
    print("setting up engine client...")
    client = EngineClient(
        opts=EngineClientOpts(url=ENGINE_BACKEND_URL, signer=SIGNER_PRIVATE_KEY)
    )

    print("querying status...")
    status_data = client.get_status()
    print("status:", status_data)

    print("querying contracts...")
    contracts_data = client.get_contracts()
    pprint(contracts_data.json())

    client.endpoint_addr = contracts_data.endpoint_addr
    client.chain_id = contracts_data.chain_id
    client.book_addrs = contracts_data.book_addrs

    print("querying product symbols...")
    product_symbols = client.get_product_symbols()
    pprint(product_symbols)

    print("querying symbols...")
    symbols = client.get_symbols(product_type="perp")
    pprint(symbols)

    print("placing order...")
    product_id = 1
    order = OrderParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        priceX18=to_x18(20000),
        amount=to_pow_10(1, 17),
        expiration=get_expiration_timestamp(OrderType.POST_ONLY, int(time.time()) + 40),
        nonce=gen_order_nonce(),
    )
    order_digest = client.get_order_digest(order, product_id)
    print("order digest:", order_digest)

    place_order = PlaceOrderParams(product_id=product_id, order=order)
    res = client.place_order(place_order)
    print("order result:", res.json(indent=2))

    print("placing order with custom id...")
    product_id = 1
    order = OrderParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        priceX18=to_x18(20000),
        amount=to_pow_10(1, 17),
        expiration=get_expiration_timestamp(OrderType.POST_ONLY, int(time.time()) + 40),
        nonce=gen_order_nonce(),
    )
    place_order = PlaceOrderParams(product_id=product_id, order=order, id=100)
    res = client.place_order(place_order)
    print("order with custom id result:", res.json(indent=2))

    print("querying order...")
    order = client.get_order(product_id, order_digest)
    print("order found", order.json(indent=2))

    print("querying subaccount info...")
    subaccount_info = client.get_subaccount_info(order.sender)
    print("subaccount info:", subaccount_info.json(indent=2))

    print("querying subaccount open orders...")
    subaccount_open_orders = client.get_subaccount_open_orders(product_id, order.sender)
    print("subaccount open orders:", subaccount_open_orders.json(indent=2))

    cancel_order = CancelOrdersParams(
        sender=order.sender, productIds=[product_id], digests=[order_digest]
    )
    res = client.cancel_orders(cancel_order)
    print("cancel orders result:", res.json(indent=2))

    print("querying order after cancel...")
    try:
        order = client.get_order(product_id, order_digest)
        print("order found but should not be!")
        exit(1)
    except Exception as e:
        print("order not found:", e)

    print("querying subaccount open orders (after cancel)...")
    subaccount_open_orders = client.get_subaccount_open_orders(product_id, order.sender)
    print("subaccount open orders:", subaccount_open_orders.json(indent=2))

    print("querying market liquidity...")
    market_liquidity = client.get_market_liquidity(product_id, depth=10)
    print("market liquidity:", market_liquidity)

    print("querying all products...")
    all_products = client.get_all_products()
    print("all products:", all_products.json(indent=2))

    print("querying market price...")
    market_price = client.get_market_price(product_id)
    print("market price:", market_price.json(indent=2))

    print("querying max order size...")
    max_order_size = client.get_max_order_size(
        QueryMaxOrderSizeParams(
            sender=order.sender,
            product_id=product_id,
            price_x18=to_x18(25000),
            direction="short",
        )
    )
    print("max order size:", max_order_size)

    print("querying max withdrawable...")
    max_withdrawable = client.get_max_withdrawable(product_id, order.sender)
    print("max withdrawable:", max_withdrawable.json(indent=2))

    print("querying max lp mintable...")
    max_lp_mintable = client.get_max_lp_mintable(
        product_id=1,
        sender=order.sender,
    )
    print("max lp mintable:", max_lp_mintable.json(indent=2))

    print("querying fee rates...")
    fee_rates = client.get_fee_rates(sender=order.sender)
    print("fee rates:", fee_rates.json(indent=2))

    print("querying health groups...")
    health_groups = client.get_health_groups()
    print("health groups:", health_groups.json(indent=2))

    print("querying linked signer...")
    linked_signer = client.get_linked_signer(subaccount=order.sender)
    print("linked signer:", linked_signer.json(indent=2))

    print("minting lp...")
    mint_lp_params = MintLpParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        productId=3,
        amountBase=to_x18(1),
        quoteAmountLow=to_x18(1000),
        quoteAmountHigh=to_x18(2000),
    )
    res = client.mint_lp(mint_lp_params)
    print("mint lp results:", res.json(indent=2))

    print("burning lp...")
    burn_lp_params = BurnLpParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        productId=3,
        amount=to_x18(1),
        nonce=client.tx_nonce(),
    )
    res = client.burn_lp(burn_lp_params)
    print("burn lp result:", res.json(indent=2))

    print("liquidating subaccount...")
    liquidate_subaccount_params = LiquidateSubaccountParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        liquidatee=subaccount_to_bytes32(
            "0x13df46D99A81DcA51A7fC9852a0c1b88072B6Ba9", "default"
        ),
        productId=1,
        isEncodedSpread=False,
        amount=to_x18(1),
    )
    try:
        res = client.liquidate_subaccount(liquidate_subaccount_params)
        print("liquidate subaccount result:", res.json(indent=2))
    except Exception as e:
        print("liquidate subaccount failed with error:", e)

    linked_signer: LocalAccount = Account.from_key(
        LINKED_SIGNER_PRIVATE_KEY or SIGNER_PRIVATE_KEY
    )

    print("linking signer...", linked_signer.address)
    link_signer_params = LinkSignerParams(
        sender=client.signer.address + str_to_hex("default"),
        signer=subaccount_to_bytes32(linked_signer.address, "default"),
    )

    try:
        res = client.link_signer(link_signer_params)
        print("link signer result:", res.json(indent=2))
    except Exception as e:
        print("link signer failed with error:", e)
    else:
        print(
            "linked signer:",
            client.get_linked_signer(
                subaccount=bytes32_to_hex(link_signer_params.sender)
            ).json(indent=2),
        )

        print("placing order as a linked signer...")
        client.linked_signer = linked_signer

        order = OrderParams(
            sender=SubaccountParams(
                subaccount_owner=client.signer.address, subaccount_name="default"
            ),
            priceX18=to_x18(20000),
            amount=to_pow_10(1, 17),
            expiration=get_expiration_timestamp(
                OrderType.POST_ONLY, int(time.time()) + 40
            ),
            nonce=gen_order_nonce(),
        )
        order_digest = client.get_order_digest(order, 2)
        print("order digest:", order_digest)

        place_order = PlaceOrderParams(product_id=2, order=order)
        res = client.place_order(place_order)
        print("order result:", res.json(indent=2))

    print("querying linked signer post update...")
    linked_signer_res = client.get_linked_signer(
        subaccount=bytes32_to_hex(link_signer_params.sender)
    )
    print("linked signer:", linked_signer_res.json(indent=2))

    print("revoking signer...")
    link_signer_params.signer = zero_subaccount()
    res = client.link_signer(link_signer_params)
    print("revoke signer result:", res.json(indent=2))

    client.linked_signer = None

    print("querying linked signer post revoking...")
    linked_signer_res = client.get_linked_signer(
        subaccount=bytes32_to_hex(link_signer_params.sender)
    )
    print("linked signer:", linked_signer_res.json(indent=2))

    print("withdrawing collateral...")
    withdraw_collateral_params = WithdrawCollateralParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        productId=0,
        amount=to_pow_10(1, 6),
    )

    res = client.withdraw_collateral(withdraw_collateral_params)
    print("withdraw collateral result:", res.json(indent=2))
