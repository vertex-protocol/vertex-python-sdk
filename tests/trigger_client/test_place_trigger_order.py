from vertex_protocol.engine_client.types.execute import OrderParams
from vertex_protocol.trigger_client.types.execute import (
    PlaceTriggerOrderParams,
    PlaceTriggerOrderRequest,
    PriceAboveTrigger,
    PriceBelowTrigger,
    to_trigger_execute_request,
)
from vertex_protocol.utils.bytes32 import hex_to_bytes32
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import SubaccountParams


def test_place_trigger_order_params(
    senders: list[str], owners: list[str], order_params: dict
):
    product_id = 1
    sender = hex_to_bytes32(senders[0])
    params_from_dict = PlaceTriggerOrderParams(
        **{
            "product_id": product_id,
            "order": {
                "sender": senders[0],
                "priceX18": order_params["priceX18"],
                "amount": order_params["amount"],
                "expiration": order_params["expiration"],
            },
            "trigger": {"price_below": "9900000000000000000000"},
        }
    )
    params_from_obj = PlaceTriggerOrderParams(
        product_id=product_id,
        order=OrderParams(
            sender=senders[0],
            priceX18=order_params["priceX18"],
            amount=order_params["amount"],
            expiration=order_params["expiration"],
        ),
        trigger=PriceBelowTrigger(price_below="9900000000000000000000"),
    )
    bytes32_sender = PlaceTriggerOrderParams(
        product_id=product_id,
        order=OrderParams(
            sender=hex_to_bytes32(senders[0]),
            priceX18=order_params["priceX18"],
            amount=order_params["amount"],
            expiration=order_params["expiration"],
        ),
        trigger=PriceBelowTrigger(price_below="9900000000000000000000"),
    )
    subaccount_params_sender = PlaceTriggerOrderParams(
        product_id=product_id,
        order=OrderParams(
            sender=SubaccountParams(
                subaccount_owner=owners[0], subaccount_name="default"
            ),
            priceX18=order_params["priceX18"],
            amount=order_params["amount"],
            expiration=order_params["expiration"],
        ),
        trigger=PriceBelowTrigger(price_below="9900000000000000000000"),
    )

    assert (
        params_from_dict
        == params_from_obj
        == bytes32_sender
        == subaccount_params_sender
    )

    assert params_from_dict.product_id == product_id
    assert params_from_dict.order.sender == sender
    assert params_from_dict.order.amount == order_params["amount"]
    assert params_from_dict.order.priceX18 == order_params["priceX18"]
    assert params_from_dict.order.expiration == order_params["expiration"]
    assert params_from_dict.trigger.price_below == "9900000000000000000000"
    assert params_from_dict.signature is None

    params_from_dict.signature = (
        "0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"
    )
    params_from_dict.order.nonce = gen_order_nonce()
    place_trigger_order_req = PlaceTriggerOrderRequest(place_order=params_from_dict)
    assert place_trigger_order_req == to_trigger_execute_request(params_from_dict)
    assert place_trigger_order_req.dict() == {
        "place_order": {
            "product_id": product_id,
            "order": {
                "sender": senders[0].lower(),
                "priceX18": str(order_params["priceX18"]),
                "amount": str(order_params["amount"]),
                "expiration": str(order_params["expiration"]),
                "nonce": str(params_from_dict.order.nonce),
            },
            "signature": params_from_dict.signature,
            "trigger": {"price_below": "9900000000000000000000"},
        }
    }

    params_from_dict.id = 100
    place_trigger_order_req = PlaceTriggerOrderRequest(place_order=params_from_dict)
    assert place_trigger_order_req == to_trigger_execute_request(params_from_dict)
    assert place_trigger_order_req.dict() == {
        "place_order": {
            "id": 100,
            "product_id": product_id,
            "order": {
                "sender": senders[0].lower(),
                "priceX18": str(order_params["priceX18"]),
                "amount": str(order_params["amount"]),
                "expiration": str(order_params["expiration"]),
                "nonce": str(params_from_dict.order.nonce),
            },
            "signature": params_from_dict.signature,
            "trigger": {"price_below": "9900000000000000000000"},
        }
    }
