import requests
from functools import singledispatchmethod
from typing import Union
from vertex_protocol.contracts.types import VertexExecuteType
from vertex_protocol.trigger_client.types.execute import (
    TriggerExecuteParams,
    TriggerExecuteRequest,
    PlaceTriggerOrderParams,
    CancelTriggerOrdersParams,
    CancelProductTriggerOrdersParams,
    to_trigger_execute_request,
)
from vertex_protocol.engine_client.types.execute import ExecuteResponse
from vertex_protocol.trigger_client.types import TriggerClientOpts
from vertex_protocol.utils.exceptions import (
    BadStatusCodeException,
    ExecuteFailedException,
)
from vertex_protocol.utils.execute import VertexBaseExecute
from vertex_protocol.utils.model import VertexBaseModel, is_instance_of_union


class TriggerExecuteClient(VertexBaseExecute):
    def __init__(self, opts: TriggerClientOpts):
        super().__init__(opts)
        self._opts: TriggerClientOpts = TriggerClientOpts.parse_obj(opts)
        self.url: str = self._opts.url
        self.session = requests.Session()

    def tx_nonce(self, _: str) -> int:
        raise NotImplementedError

    @singledispatchmethod
    def execute(
        self, params: Union[TriggerExecuteParams, TriggerExecuteRequest]
    ) -> ExecuteResponse:
        """
        Executes the operation defined by the provided parameters.

        Args:
            params (ExecuteParams): The parameters for the operation to execute. This can represent a variety of operations, such as placing orders, cancelling orders, and more.

        Returns:
            ExecuteResponse: The response from the executed operation.
        """
        req: TriggerExecuteRequest = (
            params if is_instance_of_union(params, TriggerExecuteRequest) else to_trigger_execute_request(params)  # type: ignore
        )
        return self._execute(req)

    @execute.register
    def _(self, req: dict) -> ExecuteResponse:
        """
        Overloaded method to execute the operation defined by the provided request.

        Args:
            req (dict): The request data for the operation to execute. Can be a dictionary or an instance of ExecuteRequest.

        Returns:
            ExecuteResponse: The response from the executed operation.
        """
        parsed_req: TriggerExecuteRequest = VertexBaseModel.parse_obj(req)  # type: ignore
        return self._execute(parsed_req)

    def _execute(self, req: TriggerExecuteRequest) -> ExecuteResponse:
        """
        Internal method to execute the operation. Sends request to the server.

        Args:
            req (TriggerExecuteRequest): The request data for the operation to execute.

        Returns:
            ExecuteResponse: The response from the executed operation.

        Raises:
            BadStatusCodeException: If the server response status code is not 200.
            ExecuteFailedException: If there's an error in the execution or the response status is not "success".
        """
        res = self.session.post(f"{self.url}/execute", json=req.dict())
        if res.status_code != 200:
            raise BadStatusCodeException(res.text)
        try:
            execute_res = ExecuteResponse(**res.json(), req=req.dict())
        except Exception:
            raise ExecuteFailedException(res.text)
        if execute_res.status != "success":
            raise ExecuteFailedException(res.text)
        return execute_res

    def place_trigger_order(self, params: PlaceTriggerOrderParams) -> ExecuteResponse:
        params = PlaceTriggerOrderParams.parse_obj(params)
        params.order = self.prepare_execute_params(params.order, True, True)
        params.signature = params.signature or self._sign(
            VertexExecuteType.PLACE_ORDER, params.order.dict(), params.product_id
        )
        return self.execute(params)

    def cancel_trigger_orders(
        self, params: CancelTriggerOrdersParams
    ) -> ExecuteResponse:
        params = self.prepare_execute_params(
            CancelTriggerOrdersParams.parse_obj(params), True
        )
        params.signature = params.signature or self._sign(
            VertexExecuteType.CANCEL_ORDERS, params.dict()
        )
        return self.execute(params)

    def cancel_product_trigger_orders(
        self, params: CancelProductTriggerOrdersParams
    ) -> ExecuteResponse:
        params = self.prepare_execute_params(
            CancelProductTriggerOrdersParams.parse_obj(params), True
        )
        params.signature = params.signature or self._sign(
            VertexExecuteType.CANCEL_PRODUCT_ORDERS, params.dict()
        )
        return self.execute(params)
