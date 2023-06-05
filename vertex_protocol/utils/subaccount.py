from typing import Optional
from vertex_protocol.utils.model import VertexBaseModel


class SubaccountParams(VertexBaseModel):
    subaccount_owner: Optional[str]
    subaccount_name: str = "default"


Subaccount = str | bytes | SubaccountParams
