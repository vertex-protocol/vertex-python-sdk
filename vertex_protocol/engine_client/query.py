import requests
from urllib.parse import urlencode

from vertex_protocol.engine_client import EngineClientOpts
from vertex_protocol.engine_client.types.query import (
    AllProductsData,
    ContractsData,
    MarketLiquidityData,
    MarketPriceData,
    NoncesData,
    OrderData,
    QueryAllProductsParams,
    QueryContractsParams,
    QueryMarketLiquidityParams,
    QueryMarketPriceParams,
    QueryNoncesParams,
    QueryOrderParams,
    QueryRequest,
    QueryResponse,
    QueryStatusParams,
    QuerySubaccountInfoParams,
    QuerySubaccountInfoTx,
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

    def get_nonces(self, address: str) -> NoncesData:
        return self.query(QueryNoncesParams(address)).data

    def get_order(self, product_id: int, digest: str) -> OrderData:
        return self.query(QueryOrderParams(product_id=product_id, digest=digest)).data

    def get_subaccount_info(
        self, subaccount: str, txs: list[QuerySubaccountInfoTx] = None
    ) -> SubaccountInfoData:
        return self.query(
            QuerySubaccountInfoParams(subaccount=subaccount, txs=txs)
        ).data

    def get_subaccount_open_orders(
        self, product_id: int, sender: str
    ) -> SubaccountOpenOrdersData:
        return self.query(
            QuerySubaccountOpenOrdersParams(product_id=product_id, sender=sender)
        ).data

    def get_market_liquidity(self, product_id: int, depth: int) -> MarketLiquidityData:
        return self.query(
            QueryMarketLiquidityParams(product_id=product_id, depth=depth)
        ).data

    def get_all_products(self) -> AllProductsData:
        return self.query(QueryAllProductsParams()).data

    def get_market_price(self, product_id: int) -> MarketPriceData:
        return self.query(QueryMarketPriceParams(product_id=product_id)).data
