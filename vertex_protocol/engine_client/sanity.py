from pprint import pprint
from vertex_protocol.engine_client import EngineClient, EngineClientOpts
from vertex_protocol.engine_client.types.execute import (
    PlaceOrderParams,
    OrderParams,
    SubaccountParams,
)
from vertex_protocol.utils.nonce import gen_order_nonce

private_key = "0xa0dff2b40838cef1ae86ddd11b8c2a34aa52d2d6f4355e3eb9abbaaf8eccee91"
backend_url = "https://test.vertexprotocol-backend.com"

print("setting up engine client...")
client = EngineClient(opts=EngineClientOpts(url=backend_url, signer=private_key))

print("querying contracts...")
contracts_data = client.get_contracts()
pprint(contracts_data.json())

client.endpoint_addr = contracts_data.endpoint_addr
client.chain_id = contracts_data.chain_id
client.book_addrs = contracts_data.book_addrs

print("placing order...")
product_id = 1
order = OrderParams(
    sender=SubaccountParams(
        subaccount_owner=client.signer.address, subaccount_name="default"
    ),
    priceX18=28898000000000000000000,
    amount=10000000000000000,
    expiration=4611687701117784255,
    nonce=gen_order_nonce(),
)
order_digest = client.get_order_digest(order, product_id)
print("order digest", order_digest)

place_order = PlaceOrderParams(product_id=product_id, order=order)
res = client.place_order(place_order)
print("order result", res.json(indent=2))
