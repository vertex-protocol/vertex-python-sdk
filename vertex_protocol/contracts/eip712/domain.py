from vertex_protocol.contracts.eip712 import EIP712Domain


def get_vertex_eip712_domain(verifying_contract: str, chain_id: int) -> EIP712Domain:
    return EIP712Domain(
        name="Vertex",
        version="0.0.1",
        verifyingContract=verifying_contract,
        chainId=chain_id,
    )


def get_eip712_domain_type() -> dict:
    return [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"},
    ]
