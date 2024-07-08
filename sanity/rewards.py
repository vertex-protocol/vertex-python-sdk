from sanity import CLIENT_MODE, SIGNER_PRIVATE_KEY
from vertex_protocol.client import VertexClient, create_vertex_client
from vertex_protocol.utils.math import to_x18
from vertex_protocol.contracts.types import ClaimVrtxParams


def run():
    print("setting up vertex client...")
    client: VertexClient = create_vertex_client(CLIENT_MODE, SIGNER_PRIVATE_KEY)
    signer = client.context.signer

    print("network:", client.context.contracts.network)
    print("signer:", signer.address)

    claim_vrtx_contract_params = client.rewards._get_claim_vrtx_contract_params(
        ClaimVrtxParams(epoch=10, amount=to_x18(100)), signer
    )

    print("claim vrtx params:", claim_vrtx_contract_params)

    vrtx = client.context.contracts.get_token_contract_for_product(41)
    vrtx_balance = vrtx.functions.balanceOf(signer.address).call()

    print("vrtx balance (pre-claim):", vrtx_balance)

    print("claiming vrtx...")
    tx = client.rewards.claim_vrtx(ClaimVrtxParams(epoch=10, amount=to_x18(100)))
    print("tx:", tx)

    vrtx_balance = vrtx.functions.balanceOf(signer.address).call()
    print("vrtx balance (post-claim):", vrtx_balance)
