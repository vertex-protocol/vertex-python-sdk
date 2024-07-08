from vertex_protocol.client.apis.base import VertexBaseAPI


class RewardsQueryAPI(VertexBaseAPI):
    def get_claim_and_stake_estimated_vrtx(self, wallet: str):
        """
        Estimates the amount of USDC -> VRTX swap when claiming + staking USDC rewards
        """
        pass
