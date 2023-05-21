from typing import Type
from eth_account.signers.local import LocalAccount
from vertex_protocol.contracts.eip712.sign import (
    sign_eip712_typed_data,
    build_eip712_typed_data,
)
from vertex_protocol.engine_client.types import (
    EngineClientOpts,
)
from vertex_protocol.engine_client.types.execute import BaseParams, PlaceOrderParams
from vertex_protocol.engine_client.types.execute import SubaccountParams
from vertex_protocol.utils.engine import VertexExecute


class EngineExecuteClient:
    def __init__(self, opts: EngineClientOpts):
        """
        Initialize EngineExecuteClient with provided options
        """
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

    @property
    def endpoint_addr(self) -> str:
        if self._opts.endpoint_addr is None:
            raise ValueError("Endpoint address not set")
        return self._opts.endpoint_addr

    @property
    def book_addrs(self) -> str:
        if self._opts.book_addrs is None:
            raise ValueError("Book addresses are not set")
        return self._opts.book_addrs

    @property
    def chain_id(self) -> str:
        if self._opts.chain_id is None:
            raise ValueError("Chain ID is not set")
        return self._opts.chain_id

    @property
    def signer(self) -> LocalAccount:
        if self._opts.signer is None:
            raise ValueError("Signer is not set")
        return self._opts.signer

    @property
    def linked_signer(self) -> LocalAccount:
        if self._opts.linked_signer is not None:
            return self._opts.linked_signer
        if self._opts.signer is not None:
            return self.signer
        raise ValueError("Linked signer is not set")

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
            raise ValueError("Must set a `signer` first")
        self._opts.linked_signer = linked_signer

    def book_addr(self, product_id: int) -> str:
        if product_id >= len(self.book_addrs):
            raise ValueError(f"Invalid product_id {product_id}")
        return self.book_addrs[product_id]

    def sign(self, execute: VertexExecute, verifying_contract: str, msg: dict) -> str:
        return sign_eip712_typed_data(
            typed_data=build_eip712_typed_data(
                execute, verifying_contract, self.chain_id, msg
            ),
            signer=self.linked_signer,
        )

    def place_order(self, params: PlaceOrderParams):
        params.order = self._inject_owner_if_needed(params.order)
        params = PlaceOrderParams.parse_obj(params)
        pass
