from sanity import CLIENT_MODE, SIGNER_PRIVATE_KEY
from vertex_protocol.contracts.types import VertexTxType
from vertex_protocol.utils.bytes32 import subaccount_to_hex, subaccount_to_bytes32
from vertex_protocol.contracts.eip712.sign import (
    build_eip712_typed_data,
    sign_eip712_typed_data,
)
from vertex_protocol.client import VertexClient, create_vertex_client


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
            "expiration": 13835058056999227925,
        },
        verifying_contract=client.context.contracts.endpoint.address,
        chain_id=client.context.engine_client.chain_id,
    )
    authenticate_stream_signature = sign_eip712_typed_data(
        typed_data=authenticate_stream_typed_data, signer=client.context.signer
    )
    print("authenticate stream signature:", authenticate_stream_signature)
