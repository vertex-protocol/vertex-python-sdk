import json
from unittest.mock import MagicMock

from eth_account import Account
from eth_account.signers.local import LocalAccount
from vertex_protocol.contracts.eip712.sign import (
    build_eip712_typed_data,
    sign_eip712_typed_data,
)
from vertex_protocol.engine_client import EngineClient
from vertex_protocol.contracts.types import VertexExecuteType

from vertex_protocol.engine_client.types.execute import (
    IsolatedOrderParams,
    PlaceIsolatedOrderParams,
    PlaceIsolatedOrderRequest,
    to_execute_request,
)
from vertex_protocol.utils.bytes32 import (
    bytes32_to_hex,
    hex_to_bytes32,
    subaccount_to_bytes32,
)
import pytest
from vertex_protocol.utils.exceptions import ExecuteFailedException

from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import SubaccountParams


def test_place_isolated_order_params(
    senders: list[str], owners: list[str], isolated_order_params: dict
):
    product_id = 1
    sender = hex_to_bytes32(senders[0])
    params_from_dict = PlaceIsolatedOrderParams(
        **{
            "product_id": product_id,
            "isolated_order": {
                "sender": senders[0],
                "priceX18": isolated_order_params["priceX18"],
                "amount": isolated_order_params["amount"],
                "expiration": isolated_order_params["expiration"],
                "margin": isolated_order_params["margin"],
            },
        }
    )
    params_from_obj = PlaceIsolatedOrderParams(
        product_id=product_id,
        isolated_order=IsolatedOrderParams(
            sender=senders[0],
            priceX18=isolated_order_params["priceX18"],
            amount=isolated_order_params["amount"],
            expiration=isolated_order_params["expiration"],
            margin=isolated_order_params["margin"],
        ),
    )
    bytes32_sender = PlaceIsolatedOrderParams(
        product_id=product_id,
        isolated_order=IsolatedOrderParams(
            sender=hex_to_bytes32(senders[0]),
            priceX18=isolated_order_params["priceX18"],
            amount=isolated_order_params["amount"],
            expiration=isolated_order_params["expiration"],
            margin=isolated_order_params["margin"],
        ),
    )
    subaccount_params_sender = PlaceIsolatedOrderParams(
        product_id=product_id,
        isolated_order=IsolatedOrderParams(
            sender=SubaccountParams(
                subaccount_owner=owners[0], subaccount_name="default"
            ),
            priceX18=isolated_order_params["priceX18"],
            amount=isolated_order_params["amount"],
            expiration=isolated_order_params["expiration"],
            margin=isolated_order_params["margin"],
        ),
    )

    assert (
        params_from_dict
        == params_from_obj
        == bytes32_sender
        == subaccount_params_sender
    )

    assert params_from_dict.product_id == product_id
    assert params_from_dict.isolated_order.sender == sender
    assert params_from_dict.isolated_order.amount == isolated_order_params["amount"]
    assert params_from_dict.isolated_order.priceX18 == isolated_order_params["priceX18"]
    assert (
        params_from_dict.isolated_order.expiration
        == isolated_order_params["expiration"]
    )
    assert params_from_dict.signature is None

    params_from_dict.signature = (
        "0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"
    )
    params_from_dict.isolated_order.nonce = gen_order_nonce()
    place_isolated_order_req = PlaceIsolatedOrderRequest(
        place_isolated_order=params_from_dict
    )
    assert place_isolated_order_req == to_execute_request(params_from_dict)
    assert place_isolated_order_req.dict() == {
        "place_isolated_order": {
            "product_id": product_id,
            "isolated_order": {
                "sender": senders[0].lower(),
                "priceX18": str(isolated_order_params["priceX18"]),
                "amount": str(isolated_order_params["amount"]),
                "expiration": str(isolated_order_params["expiration"]),
                "nonce": str(params_from_dict.isolated_order.nonce),
                "margin": str(isolated_order_params["margin"]),
            },
            "signature": params_from_dict.signature,
        }
    }

    params_from_dict.id = 100
    place_isolated_order_req = PlaceIsolatedOrderRequest(
        place_isolated_order=params_from_dict
    )
    assert place_isolated_order_req == to_execute_request(params_from_dict)
    assert place_isolated_order_req.dict() == {
        "place_isolated_order": {
            "id": 100,
            "product_id": product_id,
            "isolated_order": {
                "sender": senders[0].lower(),
                "priceX18": str(isolated_order_params["priceX18"]),
                "amount": str(isolated_order_params["amount"]),
                "expiration": str(isolated_order_params["expiration"]),
                "nonce": str(params_from_dict.isolated_order.nonce),
                "margin": str(isolated_order_params["margin"]),
            },
            "signature": params_from_dict.signature,
        }
    }


def test_place_isolated_order_execute_fails_incomplete_client(
    mock_post: MagicMock,
    url: str,
    chain_id: int,
    book_addrs: list[str],
    private_keys: list[str],
    senders: list[str],
    isolated_order_params: dict,
):
    engine_client = EngineClient({"url": url})
    place_isolated_order_params = {
        "product_id": 1,
        "isolated_order": isolated_order_params,
    }

    with pytest.raises(AttributeError, match="Book addresses are not set"):
        engine_client.place_isolated_order(place_isolated_order_params)

    engine_client.book_addrs = book_addrs

    with pytest.raises(AttributeError, match="Chain ID is not set."):
        engine_client.place_isolated_order(place_isolated_order_params)

    engine_client.chain_id = chain_id

    with pytest.raises(AttributeError, match="Signer is not set."):
        engine_client.place_isolated_order(place_isolated_order_params)

    engine_client.signer = Account.from_key(private_keys[0])

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "signature": "xxx",
    }
    mock_post.return_value = mock_response

    res = engine_client.place_isolated_order(place_isolated_order_params)
    place_isolated_order_req = PlaceIsolatedOrderRequest(**res.req)

    assert (
        place_isolated_order_req.place_isolated_order.isolated_order.sender.lower()
        == senders[0].lower()
    )


def test_place_isolated_order_execute_success(
    engine_client: EngineClient, mock_post: MagicMock, senders: list[str]
):
    product_id = 1
    place_isolated_order_params = PlaceIsolatedOrderParams(
        product_id=product_id,
        isolated_order=IsolatedOrderParams(
            sender=SubaccountParams(subaccount_name="default"),
            priceX18=1000,
            amount=1000,
            expiration=1000,
            nonce=1000,
            margin=1000,
        ),
    )

    isolated_order = place_isolated_order_params.isolated_order.copy(deep=True)
    order_digest = "0x123"
    isolated_order.sender = hex_to_bytes32(senders[0])

    with pytest.raises(
        ValueError,
        match="Missing `product_id` to sign place_order or place_isolated_order execute",
    ):
        engine_client._sign(
            VertexExecuteType.PLACE_ISOLATED_ORDER, isolated_order.dict()
        )

    expected_signature = engine_client._sign(
        VertexExecuteType.PLACE_ISOLATED_ORDER,
        isolated_order.dict(),
        product_id=place_isolated_order_params.product_id,
    )
    computed_signature = sign_eip712_typed_data(
        typed_data=build_eip712_typed_data(
            VertexExecuteType.PLACE_ISOLATED_ORDER,
            isolated_order.dict(),
            engine_client._opts.book_addrs[1],
            engine_client.chain_id,
        ),
        signer=engine_client._opts.linked_signer,
    )

    assert expected_signature == computed_signature

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "signature": expected_signature,
        "data": {"digest": order_digest},
    }
    mock_post.return_value = mock_response

    res = engine_client.place_isolated_order(place_isolated_order_params)
    place_isolated_order_req = PlaceIsolatedOrderRequest(**res.req)

    assert (
        place_isolated_order_req.place_isolated_order.signature
        == res.signature
        == expected_signature
    )
    assert (
        place_isolated_order_req.place_isolated_order.isolated_order.sender.lower()
        == senders[0].lower()
    )
    assert res.status == "success"
    assert res.error is None
    assert res.data.digest == order_digest

    mock_response.status_code = 200
    json_response = {
        "status": "failure",
        "error_code": 1000,
        "error": "Too Many Requests!",
    }
    mock_response.json.return_value = json_response
    mock_post.return_value.text = json.dumps(json_response)

    with pytest.raises(ExecuteFailedException, match=json.dumps(json_response)):
        engine_client.place_isolated_order(place_isolated_order_params)

    # deactivate linked signer
    engine_client.linked_signer = None

    expected_signature = sign_eip712_typed_data(
        typed_data=build_eip712_typed_data(
            VertexExecuteType.PLACE_ISOLATED_ORDER,
            isolated_order.dict(),
            engine_client._opts.book_addrs[1],
            engine_client.chain_id,
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

    res = engine_client.place_isolated_order(place_isolated_order_params)
    place_isolated_order_req = PlaceIsolatedOrderRequest(**res.req)

    assert place_isolated_order_req.place_isolated_order.signature == expected_signature


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
    isolated_order_params = {
        "priceX18": 10000,
        "amount": 10000,
        "sender": sender,
        "nonce": gen_order_nonce(),
        "expiration": 10000,
        "margin": 10000,
    }
    signature = engine_client.sign(
        VertexExecuteType.PLACE_ISOLATED_ORDER,
        isolated_order_params,
        book_addrs[1],
        chain_id,
        signer,
    )
    isolated_order_params["sender"] = bytes32_to_hex(isolated_order_params["sender"])
    res = engine_client.place_isolated_order(
        {
            "product_id": product_id,
            "isolated_order": isolated_order_params,
            "signature": signature,
        }
    )
    req = PlaceIsolatedOrderRequest(**res.req)

    assert req.place_isolated_order.signature == signature
    assert req.place_isolated_order.isolated_order.amount == str(
        isolated_order_params["amount"]
    )
    assert req.place_isolated_order.isolated_order.priceX18 == str(
        isolated_order_params["priceX18"]
    )
    assert (
        req.place_isolated_order.isolated_order.sender
        == isolated_order_params["sender"]
    )
    assert req.place_isolated_order.isolated_order.nonce == str(
        isolated_order_params["nonce"]
    )
    assert req.place_isolated_order.isolated_order.expiration == str(
        isolated_order_params["expiration"]
    )
    assert req.place_isolated_order.isolated_order.margin == str(
        isolated_order_params["margin"]
    )
