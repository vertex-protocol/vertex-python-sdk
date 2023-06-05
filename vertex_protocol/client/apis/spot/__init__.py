from vertex_protocol.client.apis.spot.execute import SpotExecuteAPI
from vertex_protocol.client.apis.spot.query import SpotQueryAPI


class SpotAPI(SpotExecuteAPI, SpotQueryAPI):
    pass
