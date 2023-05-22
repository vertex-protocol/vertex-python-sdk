from vertex_protocol.engine_client.types.execute import (
    OrderParams,
    PlaceOrderParams,
    SubaccountParams,
)
from vertex_protocol.utils.bytes32 import hex_to_bytes32


def test_place_order_params(senders: list[str], owners: list[str], order_params: dict):
    product_id = 1
    sender_1 = hex_to_bytes32(senders[0])
    params_from_dict = PlaceOrderParams(
        **{
            "product_id": product_id,
            "order": {
                "sender": senders[0],
                "priceX18": order_params["priceX18"],
                "amount": order_params["amount"],
                "expiration": order_params["expiration"],
            },
        }
    )
    params_from_obj = PlaceOrderParams(
        product_id=product_id,
        order=OrderParams(
            sender=senders[0],
            priceX18=order_params["priceX18"],
            amount=order_params["amount"],
            expiration=order_params["expiration"],
        ),
    )
    bytes32_sender = PlaceOrderParams(
        product_id=product_id,
        order=OrderParams(
            sender=hex_to_bytes32(senders[0]),
            priceX18=order_params["priceX18"],
            amount=order_params["amount"],
            expiration=order_params["expiration"],
        ),
    )
    subaccount_params_sender = PlaceOrderParams(
        product_id=product_id,
        order=OrderParams(
            sender=SubaccountParams(
                subaccount_owner=owners[0], subaccount_name="default"
            ),
            priceX18=order_params["priceX18"],
            amount=order_params["amount"],
            expiration=order_params["expiration"],
        ),
    )

    assert (
        params_from_dict
        == params_from_obj
        == bytes32_sender
        == subaccount_params_sender
    )

    assert params_from_dict.product_id == product_id
    assert params_from_dict.order.sender == sender_1
    assert params_from_dict.order.amount == order_params["amount"]
    assert params_from_dict.order.priceX18 == order_params["priceX18"]
    assert params_from_dict.order.expiration == order_params["expiration"]
    assert params_from_dict.order.nonce is None
    assert params_from_dict.signature is None
