from typing import Optional, Union
from vertex_protocol.utils.model import VertexBaseModel


class SubaccountParams(VertexBaseModel):
    """
    A class used to represent parameters for a Subaccount in the Vertex system.

    Attributes:
        subaccount_owner (Optional[str]): The wallet address of the subaccount.
        subaccount_name (str): The subaccount name identifier.
    """

    subaccount_owner: Optional[str]
    subaccount_name: str


Subaccount = Union[str, bytes, SubaccountParams]
