import requests
from urllib.parse import urlencode

from vertex_protocol.engine_client import EngineClientOpts
from vertex_protocol.engine_client.types.query import (
    NoncesData,
    QueryNoncesParams,
    QueryRequest,
    QueryResponse,
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
            raise Exception(res.content)
        query_res = QueryResponse(**res.content)
        if query_res.status != "success":
            raise Exception(res.content)
        return query_res

    def nonces(self, params: QueryNoncesParams) -> NoncesData:
        return self.query(params).data
