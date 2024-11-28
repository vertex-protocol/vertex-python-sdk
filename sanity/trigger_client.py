import time
from sanity import ENGINE_BACKEND_URL, SIGNER_PRIVATE_KEY, TRIGGER_BACKEND_URL
from vertex_protocol.engine_client import EngineClient
from vertex_protocol.engine_client.types import EngineClientOpts
from vertex_protocol.engine_client.types.execute import OrderParams
from vertex_protocol.trigger_client import TriggerClient
from vertex_protocol.trigger_client.types import TriggerClientOpts
from vertex_protocol.trigger_client.types.execute import (
    PlaceTriggerOrderParams,
    CancelTriggerOrdersParams,
)
from vertex_protocol.trigger_client.types.models import (
    LastPriceAboveTrigger,
    PriceAboveTrigger,
)
from vertex_protocol.trigger_client.types.query import (
    ListTriggerOrdersParams,
    ListTriggerOrdersTx,
)
from vertex_protocol.utils.bytes32 import subaccount_to_hex
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.subaccount import SubaccountParams
from vertex_protocol.utils.time import now_in_millis


def run():
    print("setting up trigger client...")
    client = TriggerClient(
        opts=TriggerClientOpts(url=TRIGGER_BACKEND_URL, signer=SIGNER_PRIVATE_KEY)
    )

    engine_client = EngineClient(
        opts=EngineClientOpts(url=ENGINE_BACKEND_URL, signer=SIGNER_PRIVATE_KEY)
    )

    contracts_data = engine_client.get_contracts()
    client.endpoint_addr = contracts_data.endpoint_addr
    client.chain_id = contracts_data.chain_id
    client.book_addrs = contracts_data.book_addrs

    print("placing trigger order...")
    order_price = 100_000

    product_id = 1
    order = OrderParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        priceX18=to_x18(order_price),
        amount=to_pow_10(1, 17),
        expiration=get_expiration_timestamp(OrderType.DEFAULT, int(time.time()) + 40),
        nonce=client.order_nonce(is_trigger_order=True),
    )
    order_digest = client.get_order_digest(order, product_id)
    print("order digest:", order_digest)

    place_order = PlaceTriggerOrderParams(
        product_id=product_id,
        order=order,
        trigger=PriceAboveTrigger(price_above=to_x18(120_000)),
    )
    res = client.place_trigger_order(place_order)
    print("trigger order result:", res.json(indent=2))

    sender = subaccount_to_hex(order.sender)

    cancel_orders = CancelTriggerOrdersParams(
        sender=sender, productIds=[product_id], digests=[order_digest]
    )
    res = client.cancel_trigger_orders(cancel_orders)
    print("cancel trigger order result:", res.json(indent=2))

    product_id = 2
    order = OrderParams(
        sender=SubaccountParams(
            subaccount_owner=client.signer.address, subaccount_name="default"
        ),
        priceX18=to_x18(order_price),
        amount=to_pow_10(1, 17),
        expiration=get_expiration_timestamp(OrderType.DEFAULT, int(time.time()) + 40),
        nonce=client.order_nonce(is_trigger_order=True),
    )
    order_digest = client.get_order_digest(order, product_id)
    print("order digest:", order_digest)

    place_order = PlaceTriggerOrderParams(
        product_id=product_id,
        order=order,
        trigger=LastPriceAboveTrigger(last_price_above=to_x18(120_000)),
    )
    res = client.place_trigger_order(place_order)

    print("listing trigger orders...")
    trigger_orders = client.list_trigger_orders(
        ListTriggerOrdersParams(
            tx=ListTriggerOrdersTx(
                sender=SubaccountParams(
                    subaccount_owner=client.signer.address, subaccount_name="default"
                ),
                recvTime=now_in_millis(90),
            ),
            pending=True,
            product_id=2,
        )
    )
    print("trigger orders:", trigger_orders.json(indent=2))
