from unittest.mock import MagicMock

from eth_account import Account
from eth_account.signers.local import LocalAccount
from vertex_protocol.contracts.eip712.sign import (
    build_eip712_typed_data,
    sign_eip712_typed_data,
)
from vertex_protocol.engine_client import EngineClient
from vertex_protocol.engine_client.types.execute import (
    OrderParams,
    PlaceOrderParams,
    PlaceOrderRequest,
    SubaccountParams,
)
from vertex_protocol.utils.bytes32 import (
    bytes32_to_hex,
    hex_to_bytes32,
    subaccount_to_bytes32,
)
import pytest

from vertex_protocol.utils.engine import VertexExecute
from vertex_protocol.utils.nonce import gen_order_nonce


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


def test_place_order_execute_fails_incomplete_client(
    mock_post: MagicMock,
    url: str,
    chain_id: int,
    book_addrs: list[str],
    private_keys: list[str],
    senders: list[str],
    order_params: dict,
):
    engine_client = EngineClient({"url": url})
    place_order_params = {
        "product_id": 1,
        "order": order_params,
    }

    with pytest.raises(AttributeError, match="Book addresses are not set"):
        engine_client.place_order(place_order_params)

    engine_client.book_addrs = book_addrs

    with pytest.raises(AttributeError, match="Chain ID is not set."):
        engine_client.place_order(place_order_params)

    engine_client.chain_id = chain_id

    with pytest.raises(AttributeError, match="Signer is not set."):
        engine_client.place_order(place_order_params)

    engine_client.signer = Account.from_key(private_keys[0])

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "signature": "xxx",
    }
    mock_post.return_value = mock_response

    res = engine_client.place_order(place_order_params)
    place_order_req = PlaceOrderRequest(**res.req)

    assert place_order_req.place_order.order.sender.lower() == senders[0].lower()


def test_place_order_execute_success(
    engine_client: EngineClient, mock_post: MagicMock, senders: list[str]
):
    place_order_params = PlaceOrderParams(
        product_id=1,
        order=OrderParams(
            sender=SubaccountParams(subaccount_name="default"),
            priceX18=1000,
            amount=1000,
            expiration=1000,
            nonce=1000,
        ),
    )

    order = place_order_params.order.copy(deep=True)
    order.sender = hex_to_bytes32(senders[0])

    with pytest.raises(
        ValueError, match="Missing `product_id` to sign place_order execute"
    ):
        engine_client._sign(VertexExecute.PLACE_ORDER, order.dict())

    expected_signature = engine_client._sign(
        VertexExecute.PLACE_ORDER,
        order.dict(),
        product_id=place_order_params.product_id,
    )
    computed_signature = sign_eip712_typed_data(
        typed_data=build_eip712_typed_data(
            VertexExecute.PLACE_ORDER,
            engine_client._opts.book_addrs[1],
            engine_client.chain_id,
            order.dict(),
        ),
        signer=engine_client._opts.linked_signer,
    )

    assert expected_signature == computed_signature

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "signature": expected_signature,
    }
    mock_post.return_value = mock_response

    res = engine_client.place_order(place_order_params)
    place_order_req = PlaceOrderRequest(**res.req)

    assert place_order_req.place_order.signature == res.signature == expected_signature
    assert place_order_req.place_order.order.sender.lower() == senders[0].lower()
    assert res.status == "success"
    assert res.error is None

    mock_response.status_code = 429
    mock_response.json.return_value = {
        "status": "failure",
        "error": "Too Many Requests!",
    }
    mock_post.return_value = mock_response

    with pytest.raises(Exception, match="Too Many Requests!"):
        engine_client.place_order(place_order_params)

    # deactivate linked signer
    engine_client.linked_signer = None

    expected_signature = sign_eip712_typed_data(
        typed_data=build_eip712_typed_data(
            VertexExecute.PLACE_ORDER,
            engine_client._opts.book_addrs[1],
            engine_client.chain_id,
            order.dict(),
        ),
        signer=engine_client._opts.signer,
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "signature": expected_signature,
    }
    mock_post.return_value = mock_response

    res = engine_client.place_order(place_order_params)
    place_order_req = PlaceOrderRequest(**res.req)

    assert place_order_req.place_order.signature == expected_signature


def test_place_order_execute_provide_full_params(
    mock_post: MagicMock,
    url: str,
    chain_id: int,
    private_keys: list[str],
    book_addrs: str,
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "signature": "xxx",
    }
    mock_post.return_value = mock_response

    engine_client = EngineClient({"url": url})
    signer: LocalAccount = Account.from_key(private_keys[0])
    sender = subaccount_to_bytes32(signer.address, "default")
    product_id = 1
    order_params = {
        "priceX18": 10000,
        "amount": 10000,
        "sender": sender,
        "nonce": gen_order_nonce(),
        "expiration": 10000,
    }
    signature = engine_client.sign(
        VertexExecute.PLACE_ORDER, order_params, book_addrs[1], chain_id, signer
    )
    order_params["sender"] = bytes32_to_hex(order_params["sender"])
    res = engine_client.place_order(
        {"product_id": product_id, "order": order_params, "signature": signature}
    )
    req = PlaceOrderRequest(**res.req)

    assert req.place_order.signature == signature
    assert req.place_order.order.amount == str(order_params["amount"])
    assert req.place_order.order.priceX18 == str(order_params["priceX18"])
    assert req.place_order.order.sender == order_params["sender"]
    assert req.place_order.order.nonce == str(order_params["nonce"])
    assert req.place_order.order.expiration == str(order_params["expiration"])
