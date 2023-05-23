from pprint import pprint
from vertex_protocol.engine_client import EngineClient, EngineClientOpts
from vertex_protocol.engine_client.types.execute import (
    PlaceOrderParams,
    OrderParams,
    SubaccountParams,
)

private_key = "xxx"
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
    sender=SubaccountParams(subaccount_name="default"),
    priceX18=28898000000000000000000,
    amount=10000000000000000,
    expiration=4611687701117784255,
)
place_order = PlaceOrderParams(product_id=product_id, order=order)
pprint(place_order.dict())
res = client.place_order(place_order)
pprint(res.dict())
