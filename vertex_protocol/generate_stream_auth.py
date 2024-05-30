"""
Script that shows how to generate an auth signature, which is
required for subscribing to websocket endpoints.
"""

from vertex_protocol.client import create_vertex_client, VertexClientMode as ClientMode
from vertex_protocol.contracts.types import VertexExecuteType
from vertex_protocol.engine_client.types.execute import (
    BaseParams,
)
from vertex_protocol.contracts.eip712.sign import build_eip712_typed_data, sign_eip712_typed_data
from vertex_protocol.utils.subaccount import SubaccountParams

import os
def load_env_variables(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value
load_env_variables('../.env')

private_key = os.environ.get("SIGNER_PRIVATE_KEY")

client = create_vertex_client(ClientMode.MAINNET, private_key)

owner = client.context.engine_client.signer.address
sender = SubaccountParams(
    subaccount_owner=owner,
    subaccount_name="default",
)

sender_ser = BaseParams(sender=sender, nonce=None).serialize_sender(sender)
expiration = 13835058056999227925
msg = {
    "sender": sender_ser,
    "expiration": expiration,
}
typed_data = build_eip712_typed_data(
    execute=VertexExecuteType.AUTHENTICATION,
    msg=msg,
    verifying_contract=client.context.contracts.endpoint.address,
    chain_id=client.context.engine_client.chain_id,
)

auth_sig = sign_eip712_typed_data(typed_data=typed_data, signer=client.context.signer)
print(f"Auth sig: {auth_sig}")