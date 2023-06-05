from unittest.mock import MagicMock

from vertex_protocol.client import VertexClient
from vertex_protocol.engine_client.types.execute import (
    BurnLpParams,
    CancelOrdersParams,
    CancelProductOrdersParams,
    EngineExecuteType,
    MintLpParams,
    OrderParams,
    PlaceOrderParams,
)
from vertex_protocol.utils.bytes32 import subaccount_to_bytes32


def test_mint_lp(
    vertex_client: VertexClient,
    senders: list[str],
    mock_execute_response: MagicMock,
    mock_nonces: MagicMock,
):
    params = MintLpParams(
        productId=1, amountBase=10, quoteAmountLow=10, quoteAmountHigh=10
    )
    res = vertex_client.market.mint_lp(params)
    params.sender = subaccount_to_bytes32(senders[0])
    params.nonce = 1
    signature = vertex_client.context.engine_client.sign(
        EngineExecuteType.MINT_LP,
        params.dict(),
        vertex_client.context.engine_client.endpoint_addr,
        vertex_client.context.engine_client.chain_id,
        vertex_client.context.engine_client.signer,
    )
    assert res.req == {
        "mint_lp": {
            "tx": {
                "productId": 1,
                "amountBase": "10",
                "quoteAmountLow": "10",
                "quoteAmountHigh": "10",
                "sender": senders[0].lower(),
                "nonce": "1",
            },
            "signature": signature,
        }
    }


def test_burn_lp(
    vertex_client: VertexClient,
    senders: list[str],
    mock_execute_response: MagicMock,
    mock_nonces: MagicMock,
):
    params = BurnLpParams(productId=1, amount=10)
    res = vertex_client.market.burn_lp(params)
    params.sender = subaccount_to_bytes32(senders[0])
    params.nonce = 1
    signature = vertex_client.context.engine_client.sign(
        EngineExecuteType.BURN_LP,
        params.dict(),
        vertex_client.context.engine_client.endpoint_addr,
        vertex_client.context.engine_client.chain_id,
        vertex_client.context.engine_client.signer,
    )
    assert res.req == {
        "burn_lp": {
            "tx": {
                "productId": 1,
                "amount": "10",
                "sender": senders[0].lower(),
                "nonce": "1",
            },
            "signature": signature,
        }
    }


def test_place_order(
    vertex_client: VertexClient,
    senders: list[str],
    mock_execute_response: MagicMock,
    mock_nonces: MagicMock,
):
    order = OrderParams(priceX18=1000, amount=1, expiration=1, nonce=1)
    params = PlaceOrderParams(product_id=1, order=order)
    res = vertex_client.market.place_order(params)
    order.sender = subaccount_to_bytes32(senders[0])
    signature = vertex_client.context.engine_client.sign(
        EngineExecuteType.PLACE_ORDER,
        order.dict(),
        vertex_client.context.engine_client.book_addr(1),
        vertex_client.context.engine_client.chain_id,
        vertex_client.context.engine_client.signer,
    )
    assert res.req == {
        "place_order": {
            "product_id": 1,
            "order": {
                "sender": senders[0].lower(),
                "priceX18": str(1000),
                "amount": str(1),
                "expiration": str(1),
                "nonce": str(1),
            },
            "signature": signature,
        }
    }


def test_cancel_orders(
    vertex_client: VertexClient,
    senders: list[str],
    mock_execute_response: MagicMock,
    mock_nonces: MagicMock,
):
    params = CancelOrdersParams(
        productIds=[1],
        digests=["0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"],
        nonce=2,
    )
    res = vertex_client.market.cancel_orders(params)
    params.sender = subaccount_to_bytes32(senders[0])
    signature = vertex_client.context.engine_client.sign(
        EngineExecuteType.CANCEL_ORDERS,
        params.dict(),
        vertex_client.context.engine_client.endpoint_addr,
        vertex_client.context.engine_client.chain_id,
        vertex_client.context.engine_client.signer,
    )
    assert res.req == {
        "cancel_orders": {
            "tx": {
                "productIds": [1],
                "digests": [
                    "0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"
                ],
                "sender": senders[0].lower(),
                "nonce": str(2),
            },
            "signature": signature,
        }
    }


def test_cancel_product_orders(
    vertex_client: VertexClient,
    senders: list[str],
    mock_execute_response: MagicMock,
    mock_nonces: MagicMock,
):
    params = CancelProductOrdersParams(
        productIds=[1],
        nonce=2,
    )
    res = vertex_client.market.cancel_product_orders(params)
    params.sender = subaccount_to_bytes32(senders[0])
    signature = vertex_client.context.engine_client.sign(
        EngineExecuteType.CANCEL_PRODUCT_ORDERS,
        params.dict(),
        vertex_client.context.engine_client.endpoint_addr,
        vertex_client.context.engine_client.chain_id,
        vertex_client.context.engine_client.signer,
    )
    assert res.req == {
        "cancel_product_orders": {
            "tx": {
                "sender": senders[0].lower(),
                "productIds": [1],
                "nonce": str(2),
            },
            "signature": signature,
        }
    }
