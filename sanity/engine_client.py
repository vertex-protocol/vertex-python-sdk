from pprint import pprint
import time
from vertex_protocol.engine_client import EngineClient, EngineClientOpts
from vertex_protocol.engine_client.types.execute import (
    PlaceOrderParams,
    OrderParams,
    SubaccountParams,
)
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce

private_key = "0xa0dff2b40838cef1ae86ddd11b8c2a34aa52d2d6f4355e3eb9abbaaf8eccee91"
backend_url = "https://test.vertexprotocol-backend.com"


def run():
    print("setting up engine client...")
    client = EngineClient(opts=EngineClientOpts(url=backend_url, signer=private_key))

    print("querying status...")
    status_data = client.get_status()
    print("status", status_data)

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
    print("order digest", order_digest)

    place_order = PlaceOrderParams(product_id=product_id, order=order)
    res = client.place_order(place_order)
    print("order result", res.json(indent=2))

    print("querying order...")
    order = client.get_order({"product_id": product_id, "digest": order_digest})
    print("found order", order.json(indent=2))
