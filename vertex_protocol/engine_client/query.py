import requests
from urllib.parse import urlencode

from vertex_protocol.engine_client import EngineClientOpts
from vertex_protocol.engine_client.types.query import (
    ContractsData,
    NoncesData,
    OrderData,
    QueryContractsParams,
    QueryNoncesParams,
    QueryOrderParams,
    QueryRequest,
    QueryResponse,
    QueryStatusParams,
    QuerySubaccountInfoParams,
    QuerySubaccountOpenOrdersParams,
    StatusData,
    SubaccountInfoData,
    SubaccountOpenOrdersData,
)


class EngineQueryClient:
    def __init__(self, opts: EngineClientOpts):
        """
        Initialize EngineQueryClient with provided options
        """
        self._opts = EngineClientOpts.parse_obj(opts)
        self.url = self._opts.url

    def query(self, req: QueryRequest) -> QueryResponse:
        res = requests.get(f"{self.url}/query?{urlencode(req.dict())}")
        if res.status_code != 200:
            raise Exception(res.text)
        query_res = QueryResponse(**res.json())
        if query_res.status != "success":
            raise Exception(res.text)
        return query_res

    def get_status(self) -> StatusData:
        return self.query(QueryStatusParams()).data

    def get_contracts(self) -> ContractsData:
        return self.query(QueryContractsParams()).data

    def get_nonces(self, params: QueryNoncesParams) -> NoncesData:
        return self.query(QueryNoncesParams.parse_obj(params)).data

    def get_order(self, params: QueryOrderParams) -> OrderData:
        return self.query(QueryOrderParams.parse_obj(params)).data

    def get_subaccount_info(
        self, params: QuerySubaccountInfoParams
    ) -> SubaccountInfoData:
        return self.query(QuerySubaccountInfoParams.parse_obj(params)).data

    def get_subaccount_open_orders(
        self, params: QuerySubaccountOpenOrdersParams
    ) -> SubaccountOpenOrdersData:
        return self.query(QuerySubaccountOpenOrdersParams.parse_obj(params)).data
