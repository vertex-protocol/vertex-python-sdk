import requests
from vertex_protocol.contracts.types import VertexTxType
from vertex_protocol.trigger_client.types import TriggerClientOpts
from vertex_protocol.trigger_client.types.query import (
    ListTriggerOrdersParams,
    ListTriggerOrdersRequest,
    TriggerQueryResponse,
)
from vertex_protocol.utils.exceptions import (
    BadStatusCodeException,
    QueryFailedException,
)
from vertex_protocol.utils.execute import VertexBaseExecute


class TriggerQueryClient(VertexBaseExecute):
    """
    Client class for querying the trigger service.
    """

    def __init__(self, opts: TriggerClientOpts):
        self._opts: TriggerClientOpts = TriggerClientOpts.parse_obj(opts)
        self.url: str = self._opts.url
        self.session = requests.Session()  # type: ignore

    def tx_nonce(self, _: str) -> int:
        raise NotImplementedError

    def query(self, req: dict) -> TriggerQueryResponse:
        """
        Send a query to the trigger service.

        Args:
            req (QueryRequest): The query request parameters.

        Returns:
            QueryResponse: The response from the engine.

        Raises:
            BadStatusCodeException: If the response status code is not 200.
            QueryFailedException: If the query status is not "success".
        """
        res = self.session.post(f"{self.url}/query", json=req)
        if res.status_code != 200:
            raise BadStatusCodeException(res.text)
        try:
            query_res = TriggerQueryResponse(**res.json())
        except Exception:
            raise QueryFailedException(res.text)
        if query_res.status != "success":
            raise QueryFailedException(res.text)
        return query_res

    def list_trigger_orders(
        self, params: ListTriggerOrdersParams
    ) -> TriggerQueryResponse:
        params = ListTriggerOrdersParams.parse_obj(params)
        params.signature = params.signature or self._sign(
            VertexTxType.LIST_TRIGGER_ORDERS, params.tx.dict()
        )
        return self.query(ListTriggerOrdersRequest.parse_obj(params).dict())
