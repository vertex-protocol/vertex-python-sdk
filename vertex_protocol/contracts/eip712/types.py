from vertex_protocol.utils.engine import VertexExecute


def get_vertex_eip712_type(execute: VertexExecute) -> dict:
    return {
        VertexExecute.PLACE_ORDER: {
            "Order": [
                {"name": "sender", "type": "bytes32"},
                {"name": "priceX18", "type": "int128"},
                {"name": "amount", "type": "int128"},
                {"name": "expiration", "type": "uint64"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecute.CANCEL_ORDERS: {
            "Cancellation": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productIds", "type": "uint32[]"},
                {"name": "digests", "type": "bytes32[]"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecute.CANCEL_PRODUCT_ORDERS: {
            "CancellationProducts": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productIds", "type": "uint32[]"},
                {"name": "nonce", "type": "uint64"},
            ],
        },
        VertexExecute.WITHDRAW_COLLATERAL: {
            "WithdrawCollateral": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amount", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecute.LIQUIDATE_SUBACCOUNT: {
            "LiquidateSubaccount": [
                {"name": "sender", "type": "bytes32"},
                {"name": "liquidatee", "type": "bytes32"},
                {"name": "mode", "type": "uint8"},
                {"name": "healthGroup", "type": "uint32"},
                {"name": "amount", "type": "int128"},
                {"name": "nonce", "type": "uint64"},
            ],
        },
        VertexExecute.MINT_LP: {
            "MintLp": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amountBase", "type": "uint128"},
                {"name": "quoteAmountLow", "type": "uint128"},
                {"name": "quoteAmountHigh", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ],
        },
        VertexExecute.BURN_LP: {
            "BurnLp": [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amount", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
        VertexExecute.LINK_SIGNER: {
            "LinkSigner": [
                {"name": "sender", "type": "bytes32"},
                {"name": "signer", "type": "bytes32"},
                {"name": "nonce", "type": "uint64"},
            ]
        },
    }.get(execute)