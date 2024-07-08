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

    claim_and_stake_vrtx_contract_params = (
        client.rewards._get_claim_vrtx_contract_params(
            ClaimVrtxParams(epoch=10, amount=to_x18(100)), signer
        )
    )

    print("claim and stake vrtx params:", claim_and_stake_vrtx_contract_params)

    print("claiming and staking vrtx...")
    tx = client.rewards.claim_and_stake_vrtx(
        ClaimVrtxParams(epoch=10, amount=to_x18(100))
    )
    print("tx:", tx)

    vrtx_balance = vrtx.functions.balanceOf(signer.address).call()
    print("vrtx balance (post-claim-and-stake):", vrtx_balance)

    print("approving allowance to staking contract...")
    tx = client.context.contracts.approve_allowance(
        vrtx, to_x18(100), signer, to=client.context.contracts.vrtx_staking.address
    )
    print("tx:", tx)

    print("staking vrtx...")
    tx = client.rewards.stake_vrtx(to_x18(100))
    print("tx:", tx)

    vrtx_balance = vrtx.functions.balanceOf(signer.address).call()
    print("vrtx balance (post-stake):", vrtx_balance)

    print("unstaking vrtx...")
    tx = client.rewards.unstake_vrtx(to_x18(100))
    print(tx)

    print("withdrawing unstaked vrtx...")
    tx = client.rewards.withdraw_unstaked_vrtx()
    print(tx)

    print("claiming usdc rewards...")
    tx = client.rewards.claim_usdc_rewards()
    print(tx)

    print("claiming and staking usdc rewards...")
    tx = client.rewards.claim_and_stake_usdc_rewards()
    print(tx)

    print(
        "claim and stake estimated vrtx...",
        client.rewards.get_claim_and_stake_estimated_vrtx(signer.address),
    )

    claim_foundation_rewards_contract_params = (
        client.rewards._get_claim_foundation_rewards_contract_params(signer)
    )

    print(
        "foundation rewards contract params:",
        claim_foundation_rewards_contract_params.json(indent=2),
    )

    print("claiming foundation rewards...")
    tx = client.rewards.claim_foundation_rewards()
    print(tx)
