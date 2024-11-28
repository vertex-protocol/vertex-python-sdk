from typing import Optional

from pydantic import validator

from vertex_protocol.engine_client.types.models import ResponseStatus
from vertex_protocol.trigger_client.types.models import TriggerOrderData
from vertex_protocol.utils.bytes32 import bytes32_to_hex
from vertex_protocol.utils.execute import BaseParams, SignatureParams
from vertex_protocol.utils.model import VertexBaseModel


class ListTriggerOrdersTx(BaseParams):
    recvTime: int


class ListTriggerOrdersParams(VertexBaseModel):
    """
    Parameters for listing trigger orders
    """

    type = "list_trigger_orders"
    tx: ListTriggerOrdersTx
    product_id: Optional[int]
    pending: bool
    max_update_time: Optional[str]
    max_digest: Optional[str]
    digests: Optional[list[str]]
    limit: Optional[int]
    signature: Optional[str]


class TriggerOrder(VertexBaseModel):
    order: TriggerOrderData
    status: str
    updated_at: int


class TriggerOrdersData(VertexBaseModel):
    """
    Data model for trigger orders
    """

    orders: list[TriggerOrder]


class ListTriggerOrdersRequest(ListTriggerOrdersParams):
    tx: ListTriggerOrdersTx

    @validator("tx")
    def serialize(cls, v: ListTriggerOrdersTx) -> ListTriggerOrdersTx:
        if isinstance(v.sender, bytes):
            v.serialize_dict(["sender"], bytes32_to_hex)
        v.serialize_dict(["recvTime"], str)
        return v


class TriggerQueryResponse(VertexBaseModel):
    """
    Represents a response to a query request.

    Attributes:
        status (ResponseStatus): The status of the query response.

        data (Optional[QueryResponseData]): The data returned from the query, or an error message if the query failed.

        error (Optional[str]): The error message, if any error occurred during the query.

        error_code (Optional[int]): The error code, if any error occurred during the query.

        request_type (Optional[str]): Type of the request.
    """

    status: ResponseStatus
    data: Optional[TriggerOrdersData]
    error: Optional[str]
    error_code: Optional[int]
    request_type: Optional[str]
