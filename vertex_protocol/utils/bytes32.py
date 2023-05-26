import binascii
from vertex_protocol.utils.model import VertexBaseModel


def hex_to_bytes32(input: str) -> bytes:
    if isinstance(input, bytes):
        return input
    if input.startswith("0x"):
        input = input[2:]
    data_bytes = bytes.fromhex(input)
    padded_data = data_bytes + b"\x00" * (32 - len(data_bytes))
    return padded_data


def str_to_hex(input: str) -> str:
    return binascii.hexlify(input.encode()).decode()


def subaccount_to_bytes32(
    subaccount: str | bytes | VertexBaseModel, name: str = None
) -> str:
    # When subaccount is a string
    if isinstance(subaccount, str):
        if name is None:
            return hex_to_bytes32(subaccount)
        else:
            return hex_to_bytes32(subaccount + str_to_hex(name))

    # When subaccount is a VertexBaseModel i.e: SubaccountParams
    elif isinstance(subaccount, VertexBaseModel):
        subaccount_owner = subaccount.dict().get("subaccount_owner")
        subaccount_name = subaccount.dict().get("subaccount_name")
        if subaccount_owner is None or subaccount_name is None:
            return subaccount
        else:
            return hex_to_bytes32(subaccount_owner + str_to_hex(subaccount_name))

    # When subaccount is a bytes
    else:
        return subaccount


def bytes32_to_hex(bytes32: bytes) -> str:
    if isinstance(bytes32, bytes):
        return f"0x{bytes32.hex()}"
    else:
        return bytes32
