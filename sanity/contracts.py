import time
from sanity import CLIENT_MODE, NETWORK, SIGNER_PRIVATE_KEY
from vertex_protocol.client import VertexClient, create_vertex_client
from vertex_protocol.contracts import VertexContracts, VertexContractsContext
from vertex_protocol.contracts.loader import load_abi, load_deployment
from vertex_protocol.contracts.types import DepositCollateralParams, VertexAbiName
from vertex_protocol.engine_client.types.execute import WithdrawCollateralParams
from vertex_protocol.utils.bytes32 import subaccount_to_hex, subaccount_to_bytes32
from vertex_protocol.utils.math import to_pow_10, to_x18

from web3 import Web3
from eth_abi import encode
from eth_abi.packed import encode_packed
from eth_utils import to_bytes, to_hex


def slow_mode_withdrawal(client: VertexClient):
    # Encoding the transaction
    params = encode(
        ["bytes32", "uint32", "uint128", "uint64"],
        [
            subaccount_to_bytes32(client.context.signer.address, "default"),
            0,  # productId
            to_pow_10(1, 6),  # amount
            1,  # nonce
        ],
    )

    # Prepare the transaction bytes
    method_id = Web3.keccak(text="WithdrawCollateral(bytes32,uint32,uint128,uint64)")[
        :4
    ]
    tx_bytes = method_id + params
    bytes_data = bytearray([2]) + bytearray(tx_bytes)
    # print(to_hex(bytes_data))

    # # Preparing the transaction bytes
    # tx_bytes = to_bytes(hexstr=encoded_tx)
    # bytes_data = bytearray([2]) + bytearray(tx_bytes)
    # print(to_hex(bytes_data))

    tx = client.context.contracts.execute(
        client.context.contracts.endpoint.functions.submitSlowModeTransaction(
            bytes_data
        ),
        client.context.signer,
    )
    print(tx)


# Definitions for subaccount_to_bytes32 and to_fixed_point are required.


def run():
    print("setting up vertex contracts")
    deployment = load_deployment(NETWORK)
    vertex_contracts = VertexContracts(
        node_url=deployment.node_url,
        contracts_context=VertexContractsContext(**deployment.dict()),
    )

    old_token = vertex_contracts.w3.eth.contract(
        address="0x5FbDB2315678afecb367f032d93F642f64180aa3",
        abi=load_abi(VertexAbiName.MOCK_ERC20),
    )

    new_token = vertex_contracts.w3.eth.contract(
        address="0x5FbDB2315678afecb367f032d93F642f64180aa3",
        abi=load_abi(VertexAbiName.MOCK_ERC20),
    )

    print("node url:", deployment.node_url)
    print("endpoint:", vertex_contracts.endpoint.address)
    print("querier:", vertex_contracts.querier.address)
    print("clearinghouse:", vertex_contracts.clearinghouse.address)
    print("spot_engine:", vertex_contracts.spot_engine.address)
    print("perp_engine:", vertex_contracts.perp_engine.address)
    print("n-submissions", vertex_contracts.endpoint.functions.nSubmissions().call())
    print("quote:", vertex_contracts.clearinghouse.functions.getQuote().call())
    print(
        "old token balance:",
        old_token.functions.balanceOf(vertex_contracts.clearinghouse.address).call(),
    )
    print(
        "new token balance:",
        new_token.functions.balanceOf(vertex_contracts.clearinghouse.address).call(),
    )

    client: VertexClient = create_vertex_client(CLIENT_MODE, SIGNER_PRIVATE_KEY)
    slow_mode_withdrawal(client)
    # print("minting test tokens...")
    # mint_tx_hash = vertex_contracts._mint_mock_erc20(
    #     new_token, to_pow_10(100000, 6), client.context.signer
    # )
    # print("mint tx hash:", mint_tx_hash)

    # print("approving allowance...")
    # approve_allowance_tx_hash = vertex_contracts.approve_allowance(
    #     new_token, to_pow_10(100000, 6), client.context.signer
    # )
    # print("approve allowance tx hash:", approve_allowance_tx_hash)

    # time.sleep(1)

    # print("depositing collateral...")
    # deposit_tx_hash = client.spot.deposit(
    #     DepositCollateralParams(
    #         subaccount_name="default", product_id=0, amount=to_pow_10(100000, 6)
    #     )
    # )
    # print("deposit collateral tx hash:", deposit_tx_hash)

    subaccount = subaccount_to_hex(client.context.signer.address, "default")

    print("subaccount:", subaccount)

    print("withdrawing collateral...")
    # withdraw_collateral_params = WithdrawCollateralParams(
    #     productId=0, amount=to_pow_10(1, 6), sender=subaccount
    # )
    # res = client.spot.withdraw(withdraw_collateral_params)
    # print("withdraw result:", res.json(indent=2))
