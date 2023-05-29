from web3.contract import Contract


class VertexContracts:
    """
    Encapsulates the set of Vertex contracts required for querying and executing.
    """

    def __init__(
        self,
        querier: Contract,
        endpoint: Contract,
        clearinghouse: Contract,
        spot_engine: Contract,
        perp_engine: Contract,
    ):
        self.querier = querier
        self.endpoint = endpoint
        self.clearinghouse = clearinghouse
        self.spot_engine = spot_engine
        self.perp_engine = perp_engine
