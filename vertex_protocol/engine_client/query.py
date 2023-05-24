import requests
from urllib.parse import urlencode

from vertex_protocol.engine_client import EngineClientOpts
from vertex_protocol.engine_client.types.query import (
    AllProductsData,
    ContractsData,
    FeeRatesData,
    HealthGroupsData,
    LinkedSignerData,
    MarketLiquidityData,
    MarketPriceData,
    MaxLpMintableData,
    MaxOrderSizeData,
    MaxWithdrawableData,
    NoncesData,
    OrderData,
    QueryAllProductsParams,
    QueryContractsParams,
    QueryFeeRatesParams,
    QueryHealthGroupsParams,
    QueryLinkedSignerParams,
    QueryMarketLiquidityParams,
    QueryMarketPriceParams,
    QueryMaxLpMintableParams,
    QueryMaxOrderSizeParams,
    QueryMaxWithdrawableParams,
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
from vertex_protocol.utils.exceptions import (
    BadStatusCodeException,
    QueryFailedException,
)


class EngineQueryClient:
    def __init__(self, opts: EngineClientOpts):
        """
        Initialize EngineQueryClient with provided options
        """
        self._opts = EngineClientOpts.parse_obj(opts)
        self.url = self._opts.url

    def query(self, req: QueryRequest) -> QueryResponse:
        req_params = {k: v for k, v in req.dict().items() if v is not None}
        res = requests.get(f"{self.url}/query?{urlencode(req_params)}")
        if res.status_code != 200:
            raise BadStatusCodeException(res.text)
        query_res = QueryResponse(**res.json())
        if query_res.status != "success":
            raise QueryFailedException(res.text)
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

    def get_max_order_size(self, params: QueryMaxOrderSizeParams) -> MaxOrderSizeData:
        return self.query(QueryMaxOrderSizeParams.parse_obj(params)).data

    def get_max_withdrawable(
        self, product_id: int, sender: str, spot_leverage: bool = None
    ) -> MaxWithdrawableData:
        return self.query(
            QueryMaxWithdrawableParams(
                product_id=product_id, sender=sender, spot_leverage=spot_leverage
            )
        ).data

    def get_max_lp_mintable(
        self, product_id: int, sender: str, spot_leverage: bool = None
    ) -> MaxLpMintableData:
        return self.query(
            QueryMaxLpMintableParams(
                product_id=product_id, sender=sender, spot_leverage=spot_leverage
            )
        ).data

    def get_fee_rates(self, sender: str) -> FeeRatesData:
        return self.query(QueryFeeRatesParams(sender=sender)).data

    def get_health_groups(self) -> HealthGroupsData:
        return self.query(QueryHealthGroupsParams()).data

    def get_linked_signer(self, subaccount: str) -> LinkedSignerData:
        return self.query(QueryLinkedSignerParams(subaccount=subaccount))
