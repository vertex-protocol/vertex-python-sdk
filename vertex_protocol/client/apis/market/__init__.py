from vertex_protocol.client.apis.market.execute import MarketExecuteAPI
from vertex_protocol.client.apis.market.query import MarketQueryAPI


class MarketAPI(MarketExecuteAPI, MarketQueryAPI):
    pass
