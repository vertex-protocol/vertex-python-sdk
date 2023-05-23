import binascii


def hex_to_bytes32(hex_string: str) -> bytes:
    if hex_string.startswith("0x"):
        hex_string = hex_string[2:]
    data_bytes = bytes.fromhex(hex_string)
    padded_data = data_bytes + b"\x00" * (32 - len(data_bytes))
    return padded_data


def subaccount_to_bytes32(subaccount_owner: str, subaccount_name: str) -> str:
    return hex_to_bytes32(
        f"{subaccount_owner}{binascii.hexlify(subaccount_name.encode()).decode()}"
    )


def bytes32_to_hex(bytes32: bytes) -> str:
    return f"0x{bytes32.hex()}"
