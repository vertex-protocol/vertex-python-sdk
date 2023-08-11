from typing import Tuple


def assert_book_not_empty(
    bids: list[Tuple[str, str]], asks: list[Tuple[str, str]], is_bid: bool  # type: ignore
):
    book_is_empty = (is_bid and len(bids) == 0) or (not is_bid and len(asks) == 0)
    if book_is_empty:
        raise Exception("Orderbook is empty.")
