from vertex_protocol.contracts import VertexContracts, VertexContractsContext
from vertex_protocol.contracts.loader import load_deployment
from vertex_protocol.contracts.types import VertexNetwork

network = VertexNetwork.ARBITRUM_GOERLI


def run():
    print("setting up vertex contracts")
    deployment = load_deployment(network)
    vertex_contracts = VertexContracts(
        node_url=deployment.node_url,
        contracts_context=VertexContractsContext(**deployment.dict()),
    )

    print("endpoint:", vertex_contracts.endpoint.address)
    print("querier:", vertex_contracts.querier.address)
    print("clearinghouse:", vertex_contracts.clearinghouse.address)
    print("spot_engine:", vertex_contracts.spot_engine.address)
    print("perp_engine:", vertex_contracts.perp_engine.address)
