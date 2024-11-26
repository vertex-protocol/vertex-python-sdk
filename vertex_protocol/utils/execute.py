from typing import Optional, Union
from eth_account.signers.local import LocalAccount
from vertex_protocol.utils.backend import VertexClientOpts
from vertex_protocol.utils.nonce import gen_order_nonce


class VertexBaseExecute:
    def __init__(self, opts: VertexClientOpts):
        self._opts = opts

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

    def order_nonce(self, recv_time_ms: Optional[int] = None) -> int:
        """
        Generate the order nonce. Used for oder placements and cancellations.

        Args:
            recv_time_ms (int, optional): Received time in milliseconds.

        Returns:
            int: The generated order nonce.
        """
        return gen_order_nonce(recv_time_ms)
