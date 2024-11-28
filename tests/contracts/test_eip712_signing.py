from eth_account import Account
from vertex_protocol.contracts.eip712.domain import (
    get_eip712_domain_type,
    get_vertex_eip712_domain,
)
from vertex_protocol.contracts.eip712.sign import (
    build_eip712_typed_data,
    get_eip712_typed_data_digest,
    sign_eip712_typed_data,
)
from vertex_protocol.contracts.eip712.types import get_vertex_eip712_type
from vertex_protocol.contracts.types import VertexTxType
import pytest


def test_build_eip712_domain(endpoint_addr: str, book_addrs: list[str], chain_id: int):
    eip712_domain_endpoint_addr = get_vertex_eip712_domain(
        verifying_contract=endpoint_addr, chain_id=chain_id
    )
    eip712_domain_book_addr = get_vertex_eip712_domain(
        verifying_contract=book_addrs[1], chain_id=chain_id
    )

    assert eip712_domain_endpoint_addr.name == eip712_domain_book_addr.name == "Vertex"
    assert (
        eip712_domain_endpoint_addr.version
        == eip712_domain_book_addr.version
        == "0.0.1"
    )
    assert (
        eip712_domain_endpoint_addr.chainId
        == eip712_domain_book_addr.chainId
        == chain_id
    )
    assert eip712_domain_endpoint_addr.verifyingContract == endpoint_addr
    assert eip712_domain_book_addr.verifyingContract == book_addrs[1]

    assert eip712_domain_endpoint_addr.dict() == {
        "name": "Vertex",
        "version": "0.0.1",
        "chainId": chain_id,
        "verifyingContract": endpoint_addr,
    }
    assert eip712_domain_book_addr.dict() == {
        "name": "Vertex",
        "version": "0.0.1",
        "chainId": chain_id,
        "verifyingContract": book_addrs[1],
    }


@pytest.mark.parametrize(
    "tx, primary_type, eip712_type",
    [
        (
            VertexTxType.PLACE_ORDER,
            "Order",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "priceX18", "type": "int128"},
                {"name": "amount", "type": "int128"},
                {"name": "expiration", "type": "uint64"},
                {"name": "nonce", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.CANCEL_ORDERS,
            "Cancellation",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "productIds", "type": "uint32[]"},
                {"name": "digests", "type": "bytes32[]"},
                {"name": "nonce", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.CANCEL_PRODUCT_ORDERS,
            "CancellationProducts",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "productIds", "type": "uint32[]"},
                {"name": "nonce", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.WITHDRAW_COLLATERAL,
            "WithdrawCollateral",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amount", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.LIQUIDATE_SUBACCOUNT,
            "LiquidateSubaccount",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "liquidatee", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "isEncodedSpread", "type": "bool"},
                {"name": "amount", "type": "int128"},
                {"name": "nonce", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.MINT_LP,
            "MintLp",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amountBase", "type": "uint128"},
                {"name": "quoteAmountLow", "type": "uint128"},
                {"name": "quoteAmountHigh", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.BURN_LP,
            "BurnLp",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "productId", "type": "uint32"},
                {"name": "amount", "type": "uint128"},
                {"name": "nonce", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.LINK_SIGNER,
            "LinkSigner",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "signer", "type": "bytes32"},
                {"name": "nonce", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.AUTHENTICATE_STREAM,
            "StreamAuthentication",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "expiration", "type": "uint64"},
            ],
        ),
        (
            VertexTxType.LIST_TRIGGER_ORDERS,
            "ListTriggerOrders",
            [
                {"name": "sender", "type": "bytes32"},
                {"name": "recvTime", "type": "uint64"},
            ],
        ),
    ],
)
def test_build_eip712_types(
    tx: VertexTxType, primary_type: str, eip712_type: list[dict]  # type: ignore
):
    computed_eip712_type = get_vertex_eip712_type(tx)
    eip712_primary_type = list(computed_eip712_type.keys())[0]

    assert eip712_primary_type == primary_type
    assert list(computed_eip712_type.values())[0] == eip712_type


def test_build_eip712_domain_type():
    assert get_eip712_domain_type() == [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"},
    ]


@pytest.mark.parametrize(
    "tx, primary_type, msg",
    [
        (
            VertexTxType.PLACE_ORDER,
            "Order",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "priceX18": 28898000000000000000000,
                "amount": -10000000000000000,
                "expiration": 4611687701117784255,
                "nonce": 1764428860167815857,
            },
        ),
        (
            VertexTxType.CANCEL_ORDERS,
            "Cancellation",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "productIds": [4],
                "digests": [
                    "0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"
                ],
                "nonce": 1,
            },
        ),
        (
            VertexTxType.CANCEL_PRODUCT_ORDERS,
            "CancellationProducts",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "productIds": [2, 4],
                "nonce": 1,
            },
        ),
        (
            VertexTxType.WITHDRAW_COLLATERAL,
            "WithdrawCollateral",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "productId": 2,
                "amount": 10000000000000000,
                "nonce": 1,
            },
        ),
        (
            VertexTxType.LIQUIDATE_SUBACCOUNT,
            "LiquidateSubaccount",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "liquidatee": "0x12a0b4888021576eb10a67616dd3dd3d9ce206b664656661756c740000000000",
                "productId": 1,
                "isEncodedSpread": False,
                "amount": 10000000000000000,
                "nonce": 1,
            },
        ),
        (
            VertexTxType.MINT_LP,
            "MintLp",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "productId": 1,
                "amountBase": 1000000000000000000,
                "quoteAmountLow": 20000000000000000000000,
                "quoteAmountHigh": 40000000000000000000000,
                "nonce": 1,
            },
        ),
        (
            VertexTxType.BURN_LP,
            "BurnLp",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "productId": 1,
                "amount": 1000000000000000000,
                "nonce": 1,
            },
        ),
        (
            VertexTxType.LINK_SIGNER,
            "LinkSigner",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "signer": "0x12a0b4888021576eb10a67616dd3dd3d9ce206b664656661756c740000000000",
                "nonce": 1,
            },
        ),
        (
            VertexTxType.AUTHENTICATE_STREAM,
            "StreamAuthentication",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "expiration": 4611687701117784255,
            },
        ),
        (
            VertexTxType.LIST_TRIGGER_ORDERS,
            "ListTriggerOrders",
            {
                "sender": "0x841fe4876763357975d60da128d8a54bb045d76a64656661756c740000000000",
                "recvTime": 4611687701117784255,
            },
        ),
    ],
)
def test_build_eip712_typed_data(
    tx: VertexTxType,  # type: ignore
    primary_type: str,
    msg: dict,
    endpoint_addr: str,
    chain_id: int,
):
    eip712_typed_data = build_eip712_typed_data(
        tx, verifying_contract=endpoint_addr, chain_id=chain_id, msg=msg
    )
    assert eip712_typed_data.dict() == {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            primary_type: list(get_vertex_eip712_type(tx).values())[0],
        },
        "primaryType": primary_type,
        "domain": {
            "name": "Vertex",
            "version": "0.0.1",
            "chainId": chain_id,
            "verifyingContract": endpoint_addr,
        },
        "message": msg,
    }


def test_sign_eip712_typed_data(
    chain_id: int,
    endpoint_addr: str,
    book_addrs: list[str],
    private_keys: list[str],
    order_params: dict,
    cancellation_params: dict,
    cancellation_products_params: dict,
    withdraw_collateral_params: dict,
    liquidate_subaccount_params: dict,
    mint_lp_params: dict,
    burn_lp_params: dict,
    link_signer_params: dict,
    authenticate_stream_params: dict,
    list_trigger_orders_params: dict,
):
    to_sign = [
        (VertexTxType.PLACE_ORDER, book_addrs[1], order_params),
        (VertexTxType.CANCEL_ORDERS, endpoint_addr, cancellation_params),
        (
            VertexTxType.CANCEL_PRODUCT_ORDERS,
            endpoint_addr,
            cancellation_products_params,
        ),
        (
            VertexTxType.WITHDRAW_COLLATERAL,
            endpoint_addr,
            withdraw_collateral_params,
        ),
        (
            VertexTxType.LIQUIDATE_SUBACCOUNT,
            endpoint_addr,
            liquidate_subaccount_params,
        ),
        (VertexTxType.MINT_LP, endpoint_addr, mint_lp_params),
        (VertexTxType.BURN_LP, endpoint_addr, burn_lp_params),
        (VertexTxType.LINK_SIGNER, endpoint_addr, link_signer_params),
        (VertexTxType.AUTHENTICATE_STREAM, endpoint_addr, authenticate_stream_params),
        (VertexTxType.LIST_TRIGGER_ORDERS, endpoint_addr, list_trigger_orders_params),
    ]

    signer = Account.from_key(private_keys[0])

    for tx, verifying_contract, msg in to_sign:
        eip712_typed_data = build_eip712_typed_data(
            tx, msg, verifying_contract, chain_id
        )
        # raises an exception if signing fails
        sign_eip712_typed_data(eip712_typed_data, signer)
        get_eip712_typed_data_digest(eip712_typed_data)
