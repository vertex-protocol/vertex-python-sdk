from eth_account.signers.local import LocalAccount
from vertex_protocol.contracts.eip712 import EIP712TypedData, EIP712Types
from vertex_protocol.contracts.eip712.domain import (
    get_eip712_domain_type,
    get_vertex_eip712_domain,
)
from vertex_protocol.contracts.eip712.types import get_vertex_eip712_type
from vertex_protocol.engine_client.types import VertexExecute
from eth_account.messages import encode_structured_data, _hash_eip191_message


def build_eip712_typed_data(
    execute: VertexExecute, verifying_contract: str, chain_id: int, msg: dict
) -> EIP712TypedData:
    eip17_domain = get_vertex_eip712_domain(verifying_contract, chain_id)
    eip712_execute_type = get_vertex_eip712_type(execute)
    eip712_primary_type = eip712_execute_type.keys()[0]
    eip712_types = EIP712Types(EIP712Domain=get_eip712_domain_type())
    eip712_types[eip712_primary_type] = eip712_execute_type
    return EIP712TypedData(
        domain=eip17_domain,
        primaryType=eip712_primary_type,
        types=eip712_types,
        message=msg,
    )


def get_eip712_typed_data_digest(typed_data: EIP712TypedData) -> str:
    encoded_data = encode_structured_data(typed_data)
    return _hash_eip191_message(encoded_data).hex()


def sign_eip712_typed_data(typed_data: EIP712TypedData, signer: LocalAccount) -> str:
    encoded_data = encode_structured_data(typed_data.dict())
    typed_data_hash = signer.sign_message(encoded_data)
    return typed_data_hash.signature.hex()
