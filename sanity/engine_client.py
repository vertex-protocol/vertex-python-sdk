from pprint import pprint
import time
import os
from vertex_protocol.engine_client import EngineClient, EngineClientOpts
from vertex_protocol.engine_client.types.execute import (
    PlaceOrderParams,
    OrderParams,
    SubaccountParams,
)
from vertex_protocol.engine_client.types.query import QueryMarketLiquidityParams
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce

private_key = os.getenv("PRIVATE_KEY")
backend_url = "https://test.vertexprotocol-backend.com"


def run():
    print("setting up engine client...")
    client = EngineClient(opts=EngineClientOpts(url=backend_url, signer=private_key))

    print("querying status...")
    status_data = client.get_status()
    print("status:", status_data)

    print("querying contracts...")
    contracts_data = client.get_contracts()
    pprint(contracts_data.json())

    client.endpoint_addr = contracts_data.endpoint_addr
    client.chain_id = contracts_data.chain_id
    client.book_addrs = contracts_data.book_addrs

    print("placing order...")
    product_id = 2
    order = OrderParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        priceX18=to_x18(27000),
        amount=to_pow_10(-1, 17),
        expiration=get_expiration_timestamp(OrderType.POST_ONLY, int(time.time()) + 40),
        nonce=gen_order_nonce(),
    )
    order_digest = client.get_order_digest(order, product_id)
    print("order digest:", order_digest)

    place_order = PlaceOrderParams(product_id=product_id, order=order)
    res = client.place_order(place_order)
    print("order result:", res.json(indent=2))

    print("querying order...")
    order = client.get_order(product_id, order_digest)
    print("order found", order.json(indent=2))

    print("querying subaccount info...")
    subaccount_info = client.get_subaccount_info(order.sender)
    print("subaccount info:", subaccount_info.json(indent=2))

    print("querying subaccount open orders...")
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
