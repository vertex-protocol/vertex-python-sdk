from sanity import NETWORK
from vertex_protocol.contracts import VertexContracts, VertexContractsContext
from vertex_protocol.contracts.loader import load_deployment


def run():
    print("setting up vertex contracts")
    deployment = load_deployment(NETWORK)
    vertex_contracts = VertexContracts(
        node_url=deployment.node_url,
        contracts_context=VertexContractsContext(**deployment.dict()),
    )

    print("node url:", deployment.node_url)
    print("endpoint:", vertex_contracts.endpoint.address)
    print("querier:", vertex_contracts.querier.address)
    print("clearinghouse:", vertex_contracts.clearinghouse.address)
    print("spot_engine:", vertex_contracts.spot_engine.address)
    print("perp_engine:", vertex_contracts.perp_engine.address)
    print("n-submissions", vertex_contracts.endpoint.functions.nSubmissions().call())

    # wallet = vertex_contracts.w3.to_checksum_address(
    #     "0xcb60ca32b25b4e11cd1959514d77356d58d3e138"
    # )
    # print(
    #     "getClaimed", vertex_contracts.vrtx_airdrop.functions.getClaimed(wallet).call()
    # )
