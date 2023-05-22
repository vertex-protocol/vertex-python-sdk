import requests

from typing import Optional, Type
from eth_account.signers.local import LocalAccount
from vertex_protocol.contracts.eip712.sign import (
    sign_eip712_typed_data,
    build_eip712_typed_data,
)
from vertex_protocol.engine_client.query import EngineQueryClient
from vertex_protocol.engine_client.types import (
    EngineClientOpts,
)
from vertex_protocol.engine_client.types.execute import (
    BaseParams,
    BurnLpParams,
    BurnLpRequest,
    CancelOrdersParams,
    CancelOrdersRequest,
    CancelProductOrdersParams,
    CancelProductOrdersRequest,
    ExecuteRequest,
    ExecuteResponse,
    LinkSignerParams,
    LinkSignerRequest,
    LiquidateSubaccountParams,
    LiquidateSubaccountRequest,
    MintLpParams,
    MintLpRequest,
    OrderParams,
    PlaceOrderParams,
    PlaceOrderRequest,
    WithdrawCollateralParams,
    WithdrawCollateralRequest,
)
from vertex_protocol.engine_client.types.execute import SubaccountParams
from vertex_protocol.engine_client.types.query import QueryNoncesParams
from vertex_protocol.utils.engine import VertexExecute
from vertex_protocol.utils.nonce import gen_order_nonce


class EngineExecuteClient:
    def __init__(self, opts: EngineClientOpts, querier: Optional[EngineQueryClient]):
        """
        Initialize EngineExecuteClient with provided options
        """
        self._querier = querier or EngineQueryClient(opts)
        self._opts = EngineClientOpts.parse_obj(opts)
        self.url = self._opts.url

    def _inject_owner_if_needed(self, params: Type[BaseParams]) -> Type[BaseParams]:
        if (
            isinstance(params.sender, SubaccountParams)
            and params.sender.subaccount_owner is None
        ):
            params.sender.subaccount_owner = self.signer.address
            params.sender = params.sender_to_bytes32(params.sender)
        return params

    def _inject_nonce_if_needed(self, params: Type[BaseParams]) -> Type[BaseParams]:
        if params.nonce is not None:
            return params
        if type(params) == OrderParams:
            params.nonce = self.order_nonce()
        else:
            params.nonce = self.tx_nonce()
        return params

    def tx_nonce(self) -> int:
        return self._querier.nonces(
            QueryNoncesParams(address=self.signer.address)
        ).tx_nonce

    def order_nonce(self, recv_time_ms: Optional[int]) -> int:
        return gen_order_nonce(recv_time_ms)

    def prepare_execute_params(self, params: Type[BaseParams]) -> Type[BaseParams]:
        params = self._inject_owner_if_needed(params)
        params = self._inject_nonce_if_needed(params)
        return params

    def execute(self, req: ExecuteRequest) -> ExecuteResponse:
        res = requests.post(f"{self.url}/execute", json=req.dict())
        if res.status_code != 200:
            raise Exception(res.content)
        execute_res = ExecuteResponse(**res.content)
        if execute_res.status != "success":
            raise Exception(execute_res.error)
        return execute_res

    @property
    def endpoint_addr(self) -> str:
        if self._opts.endpoint_addr is None:
            raise AttributeError("Endpoint address not set.")
        return self._opts.endpoint_addr

    @property
    def book_addrs(self) -> str:
        if self._opts.book_addrs is None:
            raise AttributeError("Book addresses are not set.")
        return self._opts.book_addrs

    @property
    def chain_id(self) -> str:
        if self._opts.chain_id is None:
            raise AttributeError("Chain ID is not set.")
        return self._opts.chain_id

    @property
    def signer(self) -> LocalAccount:
        if self._opts.signer is None:
            raise AttributeError("Signer is not set.")
        return self._opts.signer

    @property
    def linked_signer(self) -> LocalAccount:
        if self._opts.linked_signer is not None:
            return self._opts.linked_signer
        if self._opts.signer is not None:
            return self.signer
        raise AttributeError("Linked signer is not set.")

    @endpoint_addr.setter
    def endpoint_addr(self, addr: str) -> None:
        self._opts.endpoint_addr = addr

    @book_addrs.setter
    def book_addrs(self, book_addrs: list[str]) -> None:
        self._opts.book_addrs = book_addrs

    @chain_id.setter
    def chain_id(self, chain_id: str) -> None:
        self._opts.chain_id = chain_id

    @signer.setter
    def signer(self, signer: LocalAccount) -> None:
        self._opts.signer = signer

    @linked_signer.setter
    def linked_signer(self, linked_signer: LocalAccount) -> None:
        if self._opts.signer is None:
            raise AttributeError(
                "Must set a `signer` first before setting `linked_signer`."
            )
        self._opts.linked_signer = linked_signer

    def book_addr(self, product_id: int) -> str:
        if product_id >= len(self.book_addrs):
            raise ValueError(f"Invalid product_id {product_id} provided.")
        return self.book_addrs[product_id]

    def sign(self, execute: VertexExecute, msg: dict, product_id: Optional[int]) -> str:
        if execute.PLACE_ORDER and product_id is None:
            raise ValueError("Missing `product_id` to sign place_order execute")
        verifying_contract = (
            self.book_addr(product_id)
            if execute == VertexExecute.PLACE_ORDER
            else self.endpoint_addr
        )
        return sign_eip712_typed_data(
            typed_data=build_eip712_typed_data(
                execute, verifying_contract, self.chain_id, msg
            ),
            signer=self.linked_signer,
        )

    def place_order(self, params: PlaceOrderParams) -> ExecuteResponse:
        params.order = self.prepare_execute_params(params.order)
        params.signature = params.signature or self.sign(
            VertexExecute.PLACE_ORDER, params.order, params.product_id
        )
        return self.execute(
            PlaceOrderRequest(place_order=PlaceOrderParams.parse_obj(params))
        )

    def cancel_orders(self, params: CancelOrdersParams) -> ExecuteResponse:
        params = self.prepare_execute_params(params)
        params.signature = params.signature or self.sign(
            VertexExecute.CANCEL_ORDERS, params.dict()
        )
        return self.execute(
            CancelOrdersRequest(cancel_orders=CancelOrdersParams.parse_obj(params))
        )

    def cancel_product_orders(
        self, params: CancelProductOrdersParams
    ) -> ExecuteResponse:
        params = self.prepare_execute_params(params)
        params.signature = params.signature or self.sign(
            VertexExecute.CANCEL_PRODUCT_ORDERS, params.dict()
        )
        return self.execute(
            CancelProductOrdersRequest(
                cancel_product_orders=CancelProductOrdersParams.parse_obj(params)
            )
        )

    def withdraw_collateral(self, params: WithdrawCollateralParams) -> ExecuteResponse:
        params = self.prepare_execute_params(params)
        params.signature = params.signature or self.sign(
            VertexExecute.WITHDRAW_COLLATERAL, params.dict()
        )
        return self.execute(
            WithdrawCollateralRequest(
                withdraw_collateral=WithdrawCollateralParams.parse_obj(params)
            )
        )

    def liquidate_subaccount(
        self, params: LiquidateSubaccountParams
    ) -> ExecuteResponse:
        params = self.prepare_execute_params(params)
        params.signature = params.signature or self.sign(
            VertexExecute.LIQUIDATE_SUBACCOUNT, params.dict()
        )
        return self.execute(
            LiquidateSubaccountRequest(
                liquidate_subaccount=LiquidateSubaccountParams.parse_obj(params)
            )
        )

    def mint_lp(self, params: MintLpParams) -> ExecuteResponse:
        params = self.prepare_execute_params(params)
        params.signature = params.signature or self.sign(
            VertexExecute.MINT_LP, params.dict()
        )
        return self.execute(MintLpRequest(mint_lp=MintLpParams.parse_obj(params)))

    def burn_lp(self, params: BurnLpParams) -> ExecuteResponse:
        params = self.prepare_execute_params(params)
        params.signature = params.signature or self.sign(
            VertexExecute.BURN_LP, params.dict()
        )
        return self.execute(BurnLpRequest(burn_lp=BurnLpParams.parse_obj(params)))

    def link_signer(self, params: LinkSignerParams) -> ExecuteResponse:
        params = self.prepare_execute_params(params)
        params.signature = params.signature or self.sign(
            VertexExecute.LINK_SIGNER, params.dict()
        )
        return self.execute(
            LinkSignerRequest(link_signer=LinkSignerParams.parse_obj(params))
        )
