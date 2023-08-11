def assert_book_not_empty(bids: list, asks: list, is_bid: bool):
    book_is_empty = (is_bid and len(bids) == 0) or (not is_bid and len(asks) == 0)
    if book_is_empty:
        raise Exception("Orderbook is empty.")
