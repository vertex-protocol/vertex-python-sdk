from copy import deepcopy
import time
import requests
from functools import singledispatchmethod

from typing import Optional, Type, Union
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
    CancelAndPlaceParams,
    CancelOrdersParams,
    CancelProductOrdersParams,
    ExecuteParams,
    ExecuteRequest,
    ExecuteResponse,
    LinkSignerParams,
    LiquidateSubaccountParams,
    MintLpParams,
    OrderParams,
    PlaceMarketOrderParams,
    PlaceOrderParams,
    WithdrawCollateralParams,
    to_execute_request,
)
from vertex_protocol.contracts.types import VertexExecuteType
from vertex_protocol.engine_client.types.models import MarketLiquidity
from vertex_protocol.utils.bytes32 import subaccount_to_hex

from vertex_protocol.utils.exceptions import (
    BadStatusCodeException,
    ExecuteFailedException,
)
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import mul_x18, round_x18, to_x18
from vertex_protocol.utils.model import VertexBaseModel, is_instance_of_union
from vertex_protocol.utils.nonce import gen_order_nonce
from vertex_protocol.utils.subaccount import Subaccount, SubaccountParams


class EngineExecuteClient:
    """
    Client class for executing operations against the off-chain engine.
    """

    def __init__(
        self, opts: EngineClientOpts, querier: Optional[EngineQueryClient] = None
    ):
        """
        Initialize the EngineExecuteClient with provided options.

        Args:
            opts (EngineClientOpts): Options for the client.

            querier (EngineQueryClient, optional): An EngineQueryClient instance. If not provided, a new one is created.
        """
        self._querier = querier or EngineQueryClient(opts)
        self._opts: EngineClientOpts = EngineClientOpts.parse_obj(opts)
        self.url: str = self._opts.url
        self.session = requests.Session()

    def _inject_owner_if_needed(self, params: Type[BaseParams]) -> Type[BaseParams]:
        """
        Inject the owner if needed.

        Args:
            params (Type[BaseParams]): The parameters.

        Returns:
            Type[BaseParams]: The parameters with the owner injected if needed.
        """
        if isinstance(params.sender, SubaccountParams):
            params.sender.subaccount_owner = (
                params.sender.subaccount_owner or self.signer.address
            )
            params.sender = params.serialize_sender(params.sender)
        return params

    def _inject_nonce_if_needed(
        self, params: Type[BaseParams], use_order_nonce: bool
    ) -> Type[BaseParams]:
        """
        Inject the nonce if needed.

        Args:
            params (Type[BaseParams]): The parameters.

        Returns:
            Type[BaseParams]: The parameters with the nonce injected if needed.
        """
        if params.nonce is not None:
            return params
        params.nonce = self.order_nonce() if use_order_nonce else self.tx_nonce()
        return params

    def tx_nonce(self) -> int:
        """
        Get the transaction nonce. Used to perform executes such as `withdraw_collateral`.

        Returns:
            int: The transaction nonce.
        """
        return int(self._querier.get_nonces(self.signer.address).tx_nonce)

    def order_nonce(self, recv_time_ms: Optional[int] = None) -> int:
        """
        Generate the order nonce. Used for oder placements and cancellations.

        Args:
            recv_time_ms (int, optional): Received time in milliseconds.

        Returns:
            int: The generated order nonce.
        """
        return gen_order_nonce(recv_time_ms)

    def prepare_execute_params(self, params, use_order_nonce: bool):
        """
        Prepares the parameters for execution by ensuring that both owner and nonce are correctly set.

        Args:
            params (Type[BaseParams]): The original parameters.

        Returns:
            Type[BaseParams]: A copy of the original parameters with owner and nonce injected if needed.
        """
        params = deepcopy(params)
        params = self._inject_owner_if_needed(params)
        params = self._inject_nonce_if_needed(params, use_order_nonce)
        return params

    @singledispatchmethod
    def execute(self, params: Union[ExecuteParams, ExecuteRequest]) -> ExecuteResponse:
        """
        Executes the operation defined by the provided parameters.

        Args:
            params (ExecuteParams): The parameters for the operation to execute. This can represent a variety of operations, such as placing orders, cancelling orders, and more.

        Returns:
            ExecuteResponse: The response from the executed operation.
        """
        req: ExecuteRequest = (
            params if is_instance_of_union(params, ExecuteRequest) else to_execute_request(params)  # type: ignore
        )
        return self._execute(req)

    @execute.register
    def _(self, req: dict) -> ExecuteResponse:
        """
        Overloaded method to execute the operation defined by the provided request.

        Args:
            req (dict): The request data for the operation to execute. Can be a dictionary or an instance of ExecuteRequest.

        Returns:
            ExecuteResponse: The response from the executed operation.
        """
        parsed_req: ExecuteRequest = VertexBaseModel.parse_obj(req)  # type: ignore
        return self._execute(parsed_req)

    def _execute(self, req: ExecuteRequest) -> ExecuteResponse:
        """
        Internal method to execute the operation. Sends request to the server.

        Args:
            req (ExecuteRequest): The request data for the operation to execute.

        Returns:
            ExecuteResponse: The response from the executed operation.

        Raises:
            BadStatusCodeException: If the server response status code is not 200.
            ExecuteFailedException: If there's an error in the execution or the response status is not "success".
        """
        res = self.session.post(f"{self.url}/execute", json=req.dict())
        if res.status_code != 200:
            raise BadStatusCodeException(res.text)
        try:
            execute_res = ExecuteResponse(**res.json(), req=req.dict())
        except Exception:
            raise ExecuteFailedException(res.text)
        if execute_res.status != "success":
            raise ExecuteFailedException(res.text)
        return execute_res

    @property
    def endpoint_addr(self) -> str:
        if self._opts.endpoint_addr is None:
            raise AttributeError("Endpoint address not set.")
        return self._opts.endpoint_addr

    @endpoint_addr.setter
    def endpoint_addr(self, addr: str) -> None:
        self._opts.endpoint_addr = addr

    @property
    def book_addrs(self) -> list[str]:
        if self._opts.book_addrs is None:
            raise AttributeError("Book addresses are not set.")
        return self._opts.book_addrs

    @book_addrs.setter
    def book_addrs(self, book_addrs: list[str]) -> None:
        self._opts.book_addrs = book_addrs

    @property
    def chain_id(self) -> int:
        if self._opts.chain_id is None:
            raise AttributeError("Chain ID is not set.")
        return self._opts.chain_id

    @chain_id.setter
    def chain_id(self, chain_id: Union[int, str]) -> None:
        self._opts.chain_id = int(chain_id)

    @property
    def signer(self) -> LocalAccount:
        if self._opts.signer is None:
            raise AttributeError("Signer is not set.")
        assert isinstance(self._opts.signer, LocalAccount)
        return self._opts.signer

    @signer.setter
    def signer(self, signer: LocalAccount) -> None:
        self._opts.signer = signer

    @property
    def linked_signer(self) -> LocalAccount:
        if self._opts.linked_signer is not None:
            assert isinstance(self._opts.linked_signer, LocalAccount)
            return self._opts.linked_signer
        if self._opts.signer is not None:
            assert isinstance(self._opts.signer, LocalAccount)
            return self.signer
        raise AttributeError("Signer is not set.")

    @linked_signer.setter
    def linked_signer(self, linked_signer: LocalAccount) -> None:
        if self._opts.signer is None:
            raise AttributeError(
                "Must set a `signer` first before setting `linked_signer`."
            )
        self._opts.linked_signer = linked_signer

    def book_addr(self, product_id: int) -> str:
        """
        Retrieves the book address corresponding to the provided product ID.

        Needed for signing order placement executes for different products.

        Args:
            product_id (int): The ID of the product.

        Returns:
            str: The book address associated with the given product ID.

        Raises:
            ValueError: If the provided product_id is greater than or equal to the number of book addresses available.
        """
        if product_id >= len(self.book_addrs):
            raise ValueError(f"Invalid product_id {product_id} provided.")
        return self.book_addrs[product_id]

    def get_order_digest(self, order: OrderParams, product_id: int) -> str:
        """
        Generates the order digest for a given order and product ID.

        Args:
            order (OrderParams): The order parameters.

            product_id (int): The ID of the product.

        Returns:
            str: The generated order digest.
        """
        return self.build_digest(
            VertexExecuteType.PLACE_ORDER,
            order.dict(),
            self.book_addr(product_id),
            self.chain_id,
        )

    def _sign(
        self, execute: VertexExecuteType, msg: dict, product_id: Optional[int] = None
    ) -> str:
        """
        Internal method to create an EIP-712 signature for the given operation type and message.

        Args:
            execute (VertexExecuteType): The Vertex execute type to sign.

            msg (dict): The message to be signed.

            product_id (int, optional): Required for 'PLACE_ORDER' operation, specifying the product ID.

        Returns:
            str: The generated EIP-712 signature.

        Raises:
            ValueError: If the operation type is 'PLACE_ORDER' and no product_id is provided.

        Notes:
            The contract used for verification varies based on the operation type:
                - For 'PLACE_ORDER', it's derived from the book address associated with the product_id.
                - For other operations, it's the endpoint address.
        """
        is_place_order = execute == VertexExecuteType.PLACE_ORDER
        if is_place_order and product_id is None:
            raise ValueError("Missing `product_id` to sign place_order execute")
        verifying_contract = (
            self.book_addr(product_id)
            if is_place_order and product_id
            else self.endpoint_addr
        )
        return self.sign(
            execute, msg, verifying_contract, self.chain_id, self.linked_signer
        )

    def build_digest(
        self,
        execute: VertexExecuteType,
        msg: dict,
        verifying_contract: str,
        chain_id: int,
    ) -> str:
        """
        Build an EIP-712 compliant digest from given parameters.

        Must provide the same input to build an EIP-712 typed data as the one provided for signing via `.sign(...)`

        Args:
            execute (VertexExecuteType): The Vertex execute type to build digest for.

            msg (dict): The EIP712 message.

            verifying_contract (str): The contract used for verification.

            chain_id (int): The network chain ID.

        Returns:
            str: The digest computed from the provided parameters.
        """
        return get_eip712_typed_data_digest(
            build_eip712_typed_data(execute, msg, verifying_contract, chain_id)
        )

    def _assert_book_not_empty(
        self, bids: list[MarketLiquidity], asks: list[MarketLiquidity], is_bid: bool
    ):
        book_is_empty = (is_bid and len(bids) == 0) or (not is_bid and len(asks) == 0)
        if book_is_empty:
            raise Exception("Orderbook is empty.")

    def sign(
        self,
        execute: VertexExecuteType,
        msg: dict,
        verifying_contract: str,
        chain_id: int,
        signer: LocalAccount,
    ) -> str:
        """
        Signs the EIP-712 typed data using the provided signer account.

        Args:
            execute (VertexExecuteType): The type of operation.

            msg (dict): The message to be signed.

            verifying_contract (str): The contract used for verification.

            chain_id (int): The network chain ID.

            signer (LocalAccount): The account used to sign the data.

        Returns:
            str: The generated EIP-712 signature.
        """
        return sign_eip712_typed_data(
            typed_data=build_eip712_typed_data(
                execute, msg, verifying_contract, chain_id
            ),
            signer=signer,
        )

    def place_order(self, params: PlaceOrderParams) -> ExecuteResponse:
        """
        Execute a place order operation.

        Args:
            params (PlaceOrderParams): Parameters required for placing an order.
            The parameters include the order details and the product_id.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        params = PlaceOrderParams.parse_obj(params)
        params.order = self.prepare_execute_params(params.order, True)
        params.signature = params.signature or self._sign(
            VertexExecuteType.PLACE_ORDER, params.order.dict(), params.product_id
        )
        return self.execute(params)

    def place_market_order(self, params: PlaceMarketOrderParams) -> ExecuteResponse:
        """
        Places an FOK order using top of the book price with provided slippage.

        Args:
            params (PlaceMarketOrderParams): Parameters required for placing a market order.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        orderbook = self._querier.get_market_liquidity(params.product_id, 1)
        is_bid = int(params.market_order.amount) > 0
        self._assert_book_not_empty(orderbook.bids, orderbook.asks, is_bid)
        slippage = to_x18(params.slippage or 0.005)  # defaults to 0.5%
        market_price_x18 = (
            mul_x18(orderbook.bids[0][0], to_x18(1) + slippage)
            if is_bid
            else mul_x18(orderbook.asks[0][0], to_x18(1) - slippage)
        )
        price_increment_x18 = self._querier._get_subaccount_product_position(
            subaccount_to_hex(params.market_order.sender), params.product_id
        ).product.book_info.price_increment_x18
        order = OrderParams(
            sender=params.market_order.sender,
            amount=params.market_order.amount,
            nonce=params.market_order.nonce,
            priceX18=round_x18(market_price_x18, price_increment_x18),
            expiration=get_expiration_timestamp(
                OrderType.FOK,
                int(time.time()) + 1000,
            ),
        )
        return self.place_order(
            PlaceOrderParams(  # type: ignore
                product_id=params.product_id,
                order=order,
                spot_leverage=params.spot_leverage,
                signature=params.signature,
            )
        )

    def cancel_orders(self, params: CancelOrdersParams) -> ExecuteResponse:
        """
        Execute a cancel orders operation.

        Args:
            params (CancelOrdersParams): Parameters required for canceling orders.
            The parameters include the order digests to be cancelled.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        params = self.prepare_execute_params(CancelOrdersParams.parse_obj(params), True)
        params.signature = params.signature or self._sign(
            VertexExecuteType.CANCEL_ORDERS, params.dict()
        )
        return self.execute(params)

    def cancel_product_orders(
        self, params: CancelProductOrdersParams
    ) -> ExecuteResponse:
        """
        Execute a cancel product orders operation.

        Args:
            params (CancelProductOrdersParams): Parameters required for bulk canceling orders of specific products.
            The parameters include a list of product ids to bulk cancel orders for.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        params = self.prepare_execute_params(
            CancelProductOrdersParams.parse_obj(params), True
        )
        params.signature = params.signature or self._sign(
            VertexExecuteType.CANCEL_PRODUCT_ORDERS, params.dict()
        )
        return self.execute(params)

    def cancel_and_place(self, params: CancelAndPlaceParams) -> ExecuteResponse:
        """
        Execute a cancel and place operation.

        Args:
            params (CancelAndPlaceParams): Parameters required for cancel and place.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        cancel_orders: CancelOrdersParams = self.prepare_execute_params(
            CancelOrdersParams.parse_obj(params.cancel_orders), True
        )
        cancel_orders.signature = cancel_orders.signature or self._sign(
            VertexExecuteType.CANCEL_ORDERS, cancel_orders.dict()
        )
        place_order: PlaceOrderParams = PlaceOrderParams.parse_obj(params.place_order)
        place_order.order = self.prepare_execute_params(place_order.order, True)
        place_order.signature = place_order.signature or self._sign(
            VertexExecuteType.PLACE_ORDER,
            place_order.order.dict(),
            place_order.product_id,
        )
        return self.execute(
            CancelAndPlaceParams(cancel_orders=cancel_orders, place_order=place_order)
        )

    def withdraw_collateral(self, params: WithdrawCollateralParams) -> ExecuteResponse:
        """
        Execute a withdraw collateral operation.

        Args:
            params (WithdrawCollateralParams): Parameters required for withdrawing collateral.
            The parameters include the collateral details.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        params = self.prepare_execute_params(
            WithdrawCollateralParams.parse_obj(params), False
        )
        params.signature = params.signature or self._sign(
            VertexExecuteType.WITHDRAW_COLLATERAL, params.dict()
        )
        return self.execute(params)

    def liquidate_subaccount(
        self, params: LiquidateSubaccountParams
    ) -> ExecuteResponse:
        """
        Execute a liquidate subaccount operation.

        Args:
            params (LiquidateSubaccountParams): Parameters required for liquidating a subaccount.
            The parameters include the liquidatee details.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        params = self.prepare_execute_params(
            LiquidateSubaccountParams.parse_obj(params), False
        )
        params.signature = params.signature or self._sign(
            VertexExecuteType.LIQUIDATE_SUBACCOUNT,
            params.dict(),
        )
        return self.execute(params)

    def mint_lp(self, params: MintLpParams) -> ExecuteResponse:
        """
        Execute a mint LP tokens operation.

        Args:
            params (MintLpParams): Parameters required for minting LP tokens.
            The parameters include the LP details.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        params = self.prepare_execute_params(MintLpParams.parse_obj(params), False)
        params.signature = params.signature or self._sign(
            VertexExecuteType.MINT_LP,
            params.dict(),
        )
        return self.execute(params)

    def burn_lp(self, params: BurnLpParams) -> ExecuteResponse:
        """
        Execute a burn LP tokens operation.

        Args:
            params (BurnLpParams): Parameters required for burning LP tokens.
            The parameters include the LP details.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        params = self.prepare_execute_params(BurnLpParams.parse_obj(params), False)
        params.signature = params.signature or self._sign(
            VertexExecuteType.BURN_LP,
            params.dict(),
        )
        return self.execute(params)

    def link_signer(self, params: LinkSignerParams) -> ExecuteResponse:
        """
        Execute a link signer operation.

        Args:
            params (LinkSignerParams): Parameters required for linking a signer.
            The parameters include the signer details.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        params = self.prepare_execute_params(LinkSignerParams.parse_obj(params), False)
        params.signature = params.signature or self._sign(
            VertexExecuteType.LINK_SIGNER,
            params.dict(),
        )
        return self.execute(params)

    def close_position(
        self, subaccount: Subaccount, product_id: int
    ) -> ExecuteResponse:
        """
        Execute a place order operation to close a position for the provided `product_id`.

        Attributes:
            subaccount (Subaccount): The subaccount to close position for.
            product_id (int): The ID of the product to close position for.

        Returns:
            ExecuteResponse: Response of the execution, including status and potential error message.
        """
        subaccount = subaccount_to_hex(subaccount)
        position = self._querier._get_subaccount_product_position(
            subaccount, product_id
        )
        balance, product = position.balance, position.product
        closing_spread_x18 = to_x18(0.005)
        closing_price_x18 = (
            mul_x18(product.oracle_price_x18, to_x18(1) - closing_spread_x18)
            if int(balance.balance.amount) > 0
            else mul_x18(product.oracle_price_x18, to_x18(1) + closing_spread_x18)
        )
        return self.place_order(
            PlaceOrderParams(  # type: ignore
                product_id=product_id,
                order=OrderParams(  # type: ignore
                    sender=subaccount,
                    amount=-round_x18(
                        balance.balance.amount,
                        product.book_info.size_increment,
                    ),
                    priceX18=round_x18(
                        closing_price_x18,
                        product.book_info.price_increment_x18,
                    ),
                    expiration=get_expiration_timestamp(
                        OrderType.FOK,
                        int(time.time()) + 1000,
                    ),
                ),
            )
        )
