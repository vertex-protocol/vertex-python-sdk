from vertex_protocol.contracts import VertexContracts, VertexContractsContext
from vertex_protocol.contracts.loader import load_deployment
from vertex_protocol.contracts.types import VertexNetwork

rpc_node = "https://goerli-rollup.arbitrum.io/rpc"
network = VertexNetwork.ARBITRUM_GOERLI


def run():
    print("setting up vertex contracts")
    vertex_contracts = VertexContracts(
        node_url=rpc_node,
        contracts_context=VertexContractsContext(**load_deployment(network).dict()),
    )

    print("endpoint:", vertex_contracts.endpoint.address)
    print("querier:", vertex_contracts.querier.address)
    print("clearinghouse:", vertex_contracts.clearinghouse.address)
    print("spot_engine:", vertex_contracts.spot_engine.address)
    print("perp_engine:", vertex_contracts.perp_engine.address)
