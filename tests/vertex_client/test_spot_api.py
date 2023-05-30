from unittest.mock import MagicMock

from vertex_protocol.client import VertexClient
from vertex_protocol.engine_client.types.execute import (
    WithdrawCollateralParams,
)
from vertex_protocol.utils.bytes32 import subaccount_to_bytes32
from vertex_protocol.utils.engine import VertexExecute


def test_withdraw(
    vertex_client: VertexClient,
    senders: list[str],
    mock_execute_response: MagicMock,
    mock_nonces: MagicMock,
):
    params = WithdrawCollateralParams(
        productId=1,
        amount=10,
        nonce=2,
    )
    res = vertex_client.spot.withdraw(params)
    params.sender = subaccount_to_bytes32(senders[0])
    signature = vertex_client.context.engine_client.sign(
        VertexExecute.WITHDRAW_COLLATERAL,
        params.dict(),
        vertex_client.context.engine_client.endpoint_addr,
        vertex_client.context.engine_client.chain_id,
        vertex_client.context.engine_client.signer,
    )
    assert res.req == {
        "withdraw_collateral": {
            "tx": {
                "sender": senders[0].lower(),
                "productId": 1,
                "amount": str(10),
                "nonce": str(2),
            },
            "signature": signature,
        }
    }
