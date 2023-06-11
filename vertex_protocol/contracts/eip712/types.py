from pydantic import BaseModel
from vertex_protocol.contracts.types import VertexExecuteType


class EIP712Domain(BaseModel):
    """
    Model that represents the EIP-712 Domain data structure.

    Attributes:
        name (str): The user-readable name of the signing domain, i.e., the name of the DApp or the protocol.
        version (str): The current major version of the signing domain. Signatures from different versions are not compatible.
        chainId (int): The chain ID of the originating network.
        verifyingContract (str): The address of the contract that will verify the signature.
    """

    name: str
    version: str
    chainId: int
    verifyingContract: str


class EIP712Types(BaseModel):
    """
    Util to encapsulate the EIP-712 type data structure.

    Attributes:
        EIP712Domain (list[dict]): A list of dictionaries representing EIP-712 Domain data.
    """

    EIP712Domain: list[dict]

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"


class EIP712TypedData(BaseModel):
    """
    Util to represent the EIP-712 Typed Data structure.

    Attributes:
        types (EIP712Types): EIP-712 type data.
        primaryType (str): The primary type for EIP-712 message signing.
        domain (EIP712Domain): The domain data of the EIP-712 typed message.
        message (dict): The actual data to sign.
    """

    types: EIP712Types
    primaryType: str
    domain: EIP712Domain
    message: dict


def get_vertex_eip712_type(execute: VertexExecuteType) -> dict:
    """
    Util that provides the EIP712 type information for Vertex execute types.

    Args:
        execute (VertexExecuteType): The Vertex execute type for which to retrieve EIP712 type information.

    Returns:
        dict: A dictionary containing the EIP712 type information for the given execute type.
    """
    return {
        VertexExecuteType.PLACE_ORDER: {
            "Order": [
                {"name": "sender", "type": "bytes32"},
                {"name": "priceX18", "type": "int128"},
                {"name": "amount", "type": "int128"},
                {"name": "expiration", "type": "uint64"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecuteType.CANCEL_ORDERS: {
            "Cancellation": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productIds", "type": "uint32[]"},
                {"name": "digests", "type": "bytes32[]"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecuteType.CANCEL_PRODUCT_ORDERS: {
            "CancellationProducts": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productIds", "type": "uint32[]"},
                {"name": "nonce", "type": "uint64"},
            ],
        },
        VertexExecuteType.WITHDRAW_COLLATERAL: {
            "WithdrawCollateral": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amount", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecuteType.LIQUIDATE_SUBACCOUNT: {
            "LiquidateSubaccount": [
                {"name": "sender", "type": "bytes32"},
                {"name": "liquidatee", "type": "bytes32"},
                {"name": "mode", "type": "uint8"},
                {"name": "healthGroup", "type": "uint32"},
                {"name": "amount", "type": "int128"},
                {"name": "nonce", "type": "uint64"},
            ],
        },
        VertexExecuteType.MINT_LP: {
            "MintLp": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amountBase", "type": "uint128"},
                {"name": "quoteAmountLow", "type": "uint128"},
                {"name": "quoteAmountHigh", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecuteType.BURN_LP: {
            "BurnLp": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amount", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecuteType.LINK_SIGNER: {
            "LinkSigner": [
                {"name": "sender", "type": "bytes32"},
                {"name": "signer", "type": "bytes32"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
    }[execute]
