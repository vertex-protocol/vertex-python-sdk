from unittest.mock import MagicMock

from vertex_protocol.client import VertexClient
from vertex_protocol.contracts.types import VertexExecuteType

from vertex_protocol.engine_client.types.execute import (
    LinkSignerParams,
    LiquidateSubaccountParams,
)
from vertex_protocol.utils.bytes32 import subaccount_to_bytes32


def test_liquidate_subaccount(
    vertex_client: VertexClient,
    senders: list[str],
    mock_execute_response: MagicMock,
    mock_tx_nonce: MagicMock,
):
    params = LiquidateSubaccountParams(
        sender=senders[0],
        liquidatee=senders[1],
        productId=1,
        isEncodedSpread=False,
        amount=10,
        nonce=2,
    )
    res = vertex_client.subaccount.liquidate_subaccount(params)
    params.sender = subaccount_to_bytes32(senders[0])
    signature = vertex_client.context.engine_client.sign(
        VertexExecuteType.LIQUIDATE_SUBACCOUNT,
        params.dict(),
        vertex_client.context.engine_client.endpoint_addr,
        vertex_client.context.engine_client.chain_id,
        vertex_client.context.engine_client.signer,
    )
    assert res.req == {
        "liquidate_subaccount": {
            "tx": {
                "sender": senders[0].lower(),
                "liquidatee": senders[1].lower(),
                "productId": 1,
                "isEncodedSpread": False,
                "amount": str(10),
                "nonce": str(2),
            },
            "signature": signature,
        }
    }


def test_link_signer(
    vertex_client: VertexClient,
    senders: list[str],
    mock_execute_response: MagicMock,
    mock_tx_nonce: MagicMock,
):
    params = LinkSignerParams(
        sender=senders[0],
        signer=senders[1],
        nonce=2,
    )
    res = vertex_client.subaccount.link_signer(params)
    params.sender = subaccount_to_bytes32(senders[0])
    signature = vertex_client.context.engine_client.sign(
        VertexExecuteType.LINK_SIGNER,
        params.dict(),
        vertex_client.context.engine_client.endpoint_addr,
        vertex_client.context.engine_client.chain_id,
        vertex_client.context.engine_client.signer,
    )
    assert res.req == {
        "link_signer": {
            "tx": {
                "sender": senders[0].lower(),
                "signer": senders[1].lower(),
                "nonce": str(2),
            },
            "signature": signature,
        }
    }
