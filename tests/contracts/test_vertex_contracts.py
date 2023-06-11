from unittest.mock import MagicMock

from vertex_protocol.contracts import VertexContracts, VertexContractsContext


def test_vertex_contracts(
    url: str,
    mock_web3: MagicMock,
    mock_load_abi: MagicMock,
    contracts_context: VertexContractsContext,
):
    contracts = VertexContracts(node_url=url, contracts_context=contracts_context)

    assert contracts.endpoint
    assert contracts.querier
    assert not contracts.clearinghouse
    assert not contracts.perp_engine
    assert not contracts.spot_engine
