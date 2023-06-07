from vertex_protocol.contracts.types import VertexExecuteType


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
