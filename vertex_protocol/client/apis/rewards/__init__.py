from vertex_protocol.client.apis.rewards.execute import RewardsExecuteAPI
from vertex_protocol.client.apis.rewards.query import RewardsQueryAPI


class Rewards(RewardsExecuteAPI, RewardsQueryAPI):
    pass
