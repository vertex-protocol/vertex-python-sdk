from typing import Optional
from vertex_protocol.contracts.types import (
    ClaimFoundationRewardsContractParams,
    ClaimVrtxContractParams,
    ClaimVrtxParams,
)
from vertex_protocol.client.apis.base import VertexBaseAPI
from eth_account.signers.local import LocalAccount

from vertex_protocol.utils.exceptions import InvalidVrtxClaimParams


class RewardsExecuteAPI(VertexBaseAPI):
    def _validate_claim_params(self, params: ClaimVrtxParams):
        p = ClaimVrtxParams.parse_obj(params)
        if p.amount is None and p.claim_all is None:
            raise InvalidVrtxClaimParams()

    def claim_vrtx(
        self, params: ClaimVrtxParams, signer: Optional[LocalAccount] = None
    ) -> str:
        self._validate_claim_params(params)
        signer = self._get_signer(signer)
        claim_params = self._get_claim_vrtx_contract_params(params, signer)
        return self.context.contracts.claim_vrtx(
            claim_params.epoch,
            claim_params.amount_to_claim,
            claim_params.total_claimable_amount,
            claim_params.merkle_proof,
            signer,
        )

    def claim_and_stake_vrtx(
        self, params: ClaimVrtxParams, signer: Optional[LocalAccount] = None
    ) -> str:
        self._validate_claim_params(params)
        signer = self._get_signer(signer)
        return ""

    def stake_vrtx(self, amount: int, signer: Optional[LocalAccount] = None) -> str:
        signer = self._get_signer(signer)
        return ""

    def unstake_vrtx(self, amount: int, signer: Optional[LocalAccount] = None) -> str:
        signer = self._get_signer(signer)
        return ""

    def withdraw_unstaked_vrtx(self, signer: Optional[LocalAccount] = None):
        signer = self._get_signer(signer)

    def claim_usdc_rewards(self, signer: Optional[LocalAccount] = None):
        signer = self._get_signer(signer)

    def claim_and_stake_usdc_rewards(self, signer: Optional[LocalAccount] = None):
        signer = self._get_signer(signer)

    def claim_foundation_rewards(self, signer: Optional[LocalAccount] = None):
        """
        Claims all available foundation rewards. Foundation rewards are tokens associated with the chain. For example, ARB on Arbitrum.
        """
        signer = self._get_signer(signer)

    def _get_claim_vrtx_contract_params(
        self, params: ClaimVrtxParams, signer: LocalAccount
    ) -> ClaimVrtxContractParams:
        epoch_merkle_proofs = self.context.indexer_client.get_vrtx_merkle_proofs(
            signer.address
        ).merkle_proofs[params.epoch]
        total_claimable_amount = int(epoch_merkle_proofs.total_amount)
        if params.amount is not None:
            amount_to_claim = params.amount
        else:
            assert self.context.contracts.vrtx_airdrop is not None
            amount_claimed = self.context.contracts.vrtx_airdrop.functions.getClaimed(
                signer.address
            ).cal()
            amount_to_claim = total_claimable_amount - amount_claimed[params.epoch]
        return ClaimVrtxContractParams(
            epoch=params.epoch,
            amount_to_claim=amount_to_claim,
            total_claimable_amount=total_claimable_amount,
            merkle_proof=epoch_merkle_proofs.proof,
        )

    def _get_claim_foundation_rewards_contract_params(
        self, signer: LocalAccount
    ) -> ClaimFoundationRewardsContractParams:
        return ClaimFoundationRewardsContractParams()
