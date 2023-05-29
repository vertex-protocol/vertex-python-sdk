from vertex_protocol.client.apis.subaccount.execute import SubaccountExecuteAPI
from vertex_protocol.client.apis.subaccount.query import SubaccountQueryAPI


class SubaccountAPI(SubaccountExecuteAPI, SubaccountQueryAPI):
    pass
