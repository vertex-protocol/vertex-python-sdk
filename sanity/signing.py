from sanity import CLIENT_MODE, SIGNER_PRIVATE_KEY
from vertex_protocol.contracts.types import VertexTxType
from vertex_protocol.utils.bytes32 import subaccount_to_hex, subaccount_to_bytes32
from vertex_protocol.contracts.eip712.sign import (
    build_eip712_typed_data,
    sign_eip712_typed_data,
)
from vertex_protocol.client import VertexClient, create_vertex_client


import time

from vertex_protocol.engine_client.types.execute import (
    OrderParams,
)

from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import SubaccountParams
from vertex_protocol.utils.time import now_in_millis


def run():
    print("setting up vertex client...")
    client: VertexClient = create_vertex_client(CLIENT_MODE, SIGNER_PRIVATE_KEY)

    print("chain_id:", client.context.engine_client.get_contracts().chain_id)

    subaccount = subaccount_to_hex(client.context.signer.address, "default")

    print("subaccount:", subaccount)

    print("building StreamAuthentication signature...")
    authenticate_stream_typed_data = build_eip712_typed_data(
        tx=VertexTxType.AUTHENTICATE_STREAM,
        msg={
            "sender": subaccount_to_bytes32(subaccount),
            "expiration": now_in_millis(90),
        },
        verifying_contract=client.context.contracts.endpoint.address,
        chain_id=client.context.engine_client.chain_id,
    )
    authenticate_stream_signature = sign_eip712_typed_data(
        typed_data=authenticate_stream_typed_data, signer=client.context.signer
    )
    print("authenticate stream signature:", authenticate_stream_signature)

    print("building order signature...")
    order = OrderParams(
        sender=SubaccountParams(
            subaccount_owner=client.context.signer.address, subaccount_name="default"
        ),
        priceX18=to_x18(60000),
        amount=to_pow_10(1, 17),
        expiration=get_expiration_timestamp(OrderType.DEFAULT, int(time.time()) + 40),
        nonce=gen_order_nonce(),
    )
    now = time.time()
    signature = client.context.engine_client._sign(
        "place_order", order.dict(), product_id=1
    )
    elapsed_time = (time.time() - now) * 1000
    print("place order signature:", signature, "elapsed_time:", elapsed_time)
