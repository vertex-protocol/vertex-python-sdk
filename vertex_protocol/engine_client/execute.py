import requests
from functools import singledispatchmethod

from typing import Type
from eth_account.signers.local import LocalAccount
from vertex_protocol.contracts.eip712.sign import (
    get_eip712_typed_data_digest,
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
    CancelOrdersParams,
    CancelProductOrdersParams,
    ExecuteParams,
    ExecuteRequest,
    ExecuteResponse,
    LinkSignerParams,
    LiquidateSubaccountParams,
    MintLpParams,
    OrderParams,
    PlaceOrderParams,
    WithdrawCollateralParams,
    to_execute_request,
)
from vertex_protocol.engine_client.types.execute import SubaccountParams
from vertex_protocol.engine_client.types.query import QueryNoncesParams
from vertex_protocol.utils.engine import VertexExecute
from vertex_protocol.utils.model import VertexBaseModel
from vertex_protocol.utils.nonce import gen_order_nonce


class EngineExecuteClient:
    def __init__(self, opts: EngineClientOpts, querier: EngineQueryClient = None):
        """
        Initialize EngineExecuteClient with provided options
        """
        self._querier = querier or EngineQueryClient(opts)
        self._opts = EngineClientOpts.parse_obj(opts)
        self.url = self._opts.url

    def _inject_owner_if_needed(self, params: Type[BaseParams]) -> Type[BaseParams]:
        if isinstance(params.sender, SubaccountParams):
            params.sender.subaccount_owner = (
                params.sender.subaccount_owner or self.signer.address
            )
            params.sender = params.serialize_sender(params.sender)
        return params

    def _inject_nonce_if_needed(self, params: Type[BaseParams]) -> Type[BaseParams]:
        if params.nonce is not None:
            return params
        params.nonce = self.tx_nonce()
        return params

    def tx_nonce(self) -> int:
        return int(self._querier.get_nonces(self.signer.address).tx_nonce)

    def order_nonce(self, recv_time_ms: int = None) -> str:
        return gen_order_nonce(recv_time_ms)

    def prepare_execute_params(self, params: Type[BaseParams]) -> Type[BaseParams]:
        params = self._inject_owner_if_needed(params)
        params = self._inject_nonce_if_needed(params)
        return params

    @singledispatchmethod
    def execute(self, params: ExecuteParams) -> ExecuteResponse:
        return self._execute(to_execute_request(params))

    @execute.register
    def _(self, req: dict | ExecuteRequest) -> ExecuteResponse:
        return self._execute(VertexBaseModel.parse_obj(req))

    def _execute(self, req: ExecuteRequest) -> ExecuteResponse:
        res = requests.post(f"{self.url}/execute", json=req.dict())
        try:
            execute_res = ExecuteResponse(**res.json(), req=req.dict())
        except Exception:
            raise Exception(res.text)
        if res.status_code != 200 or execute_res.status != "success":
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
    def chain_id(self) -> int:
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
        raise AttributeError("Signer is not set.")

    @endpoint_addr.setter
    def endpoint_addr(self, addr: str) -> None:
        self._opts.endpoint_addr = addr

    @book_addrs.setter
    def book_addrs(self, book_addrs: list[str]) -> None:
        self._opts.book_addrs = book_addrs

    @chain_id.setter
    def chain_id(self, chain_id: int | str) -> None:
        self._opts.chain_id = int(chain_id)

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

    def get_order_digest(self, order: OrderParams, product_id: int) -> str:
        return self.build_digest(
            VertexExecute.PLACE_ORDER,
            order.dict(),
            self.book_addr(product_id),
            self.chain_id,
        )

    def _sign(self, execute: VertexExecute, msg: dict, product_id: int = None) -> str:
        is_place_order = execute == VertexExecute.PLACE_ORDER
        if is_place_order and product_id is None:
            raise ValueError("Missing `product_id` to sign place_order execute")
        verifying_contract = (
            self.book_addr(product_id) if is_place_order else self.endpoint_addr
        )
        return self.sign(
            execute, msg, verifying_contract, self.chain_id, self.linked_signer
        )

    def build_digest(
        self, execute: VertexExecute, msg: dict, verifying_contract: str, chain_id: int
    ) -> str:
        return get_eip712_typed_data_digest(
            build_eip712_typed_data(execute, msg, verifying_contract, chain_id)
        )

    def sign(
        self,
        execute: VertexExecute,
        msg: dict,
        verifying_contract: str,
        chain_id: int,
        signer: LocalAccount,
    ) -> str:
        return sign_eip712_typed_data(
            typed_data=build_eip712_typed_data(
                execute, msg, verifying_contract, chain_id
            ),
            signer=signer,
        )

    def place_order(self, params: PlaceOrderParams) -> ExecuteResponse:
        params = PlaceOrderParams.parse_obj(params)
        params.order = self.prepare_execute_params(params.order)
        params.signature = params.signature or self._sign(
            VertexExecute.PLACE_ORDER, params.order.dict(), params.product_id
        )
        return self.execute(params)

    def cancel_orders(self, params: CancelOrdersParams) -> ExecuteResponse:
        params = self.prepare_execute_params(CancelOrdersParams.parse_obj(params))
        params.signature = params.signature or self._sign(
            VertexExecute.CANCEL_ORDERS, params.dict()
        )
        return self.execute(params)

    def cancel_product_orders(
        self, params: CancelProductOrdersParams
    ) -> ExecuteResponse:
        params = self.prepare_execute_params(
            CancelProductOrdersParams.parse_obj(params)
        )
        params.signature = params.signature or self._sign(
            VertexExecute.CANCEL_PRODUCT_ORDERS, params.dict()
        )
        return self.execute(params)

    def withdraw_collateral(self, params: WithdrawCollateralParams) -> ExecuteResponse:
        params = self.prepare_execute_params(WithdrawCollateralParams.parse_obj(params))
        params.signature = params.signature or self._sign(
            VertexExecute.WITHDRAW_COLLATERAL, params.dict()
        )
        return self.execute(params)

    def liquidate_subaccount(
        self, params: LiquidateSubaccountParams
    ) -> ExecuteResponse:
        params = self.prepare_execute_params(
            LiquidateSubaccountParams.parse_obj(params)
        )
        params.signature = params.signature or self._sign(
            VertexExecute.LIQUIDATE_SUBACCOUNT,
            params.dict(),
        )
        return self.execute(params)

    def mint_lp(self, params: MintLpParams) -> ExecuteResponse:
        params = self.prepare_execute_params(MintLpParams.parse_obj(params))
        params.signature = params.signature or self._sign(
            VertexExecute.MINT_LP,
            params.dict(),
        )
        return self.execute(params)

    def burn_lp(self, params: BurnLpParams) -> ExecuteResponse:
        params = self.prepare_execute_params(BurnLpParams.parse_obj(params))
        params.signature = params.signature or self._sign(
            VertexExecute.BURN_LP,
            params.dict(),
        )
        return self.execute(params)

    def link_signer(self, params: LinkSignerParams) -> ExecuteResponse:
        params = self.prepare_execute_params(LinkSignerParams.parse_obj(params))
        params.signature = params.signature or self._sign(
            VertexExecute.LINK_SIGNER,
            params.dict(),
        )
        return self.execute(params)
