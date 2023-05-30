import json
from pathlib import Path
from vertex_protocol.contracts.types import (
    VertexAbiName,
    VertexDeployment,
    VertexNetwork,
)
from vertex_protocol.utils.model import to_enum


def load_abi(abi_name: VertexAbiName) -> list[dict]:
    file_path = Path(__file__).parent / "abis" / f"{to_enum(abi_name)}.json"
    return _load_json(file_path)


def load_deployment(network: VertexNetwork) -> VertexDeployment:
    file_path = (
        Path(__file__).parent / "deployments" / f"deployment.{to_enum(network)}.json"
    )
    return VertexDeployment(**_load_json(file_path))


def _load_json(file_path: Path) -> dict:
    with open(file_path, "r") as f:
        data = json.load(f)
    return data
