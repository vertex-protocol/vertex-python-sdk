from enum import IntEnum


class OrderType(IntEnum):
    DEFAULT = 0
    IOC = 1
    FOK = 2
    POST_ONLY = 3


def get_expiration_timestamp(
    order_type: OrderType, expiration: int, reduce_only: bool = False
) -> int:
    """
    Encodes the order type into the expiration timestamp for special order types such as immediate-or-cancel.

    Args:
        order_type (OrderType): The type of order.

        expiration (int): The expiration timestamp in UNIX seconds.

        reduce_only (bool): When True, the order can only reduce the size of an existing position. Works only with IOC & FOK.

    Returns:
        int: The properly formatted timestamp needed for the specified order type.
    """
    expiration = int(expiration) | (order_type << 62)
    if reduce_only:
        expiration |= 1 << 61
    return expiration


def decode_expiration(expiration: int) -> tuple[OrderType, int]:
    """
    Decodes the expiration timestamp to retrieve the order type and original expiration timestamp.

    Args:
        expiration (int): The encoded expiration timestamp.

    Returns:
        Tuple[OrderType, int]: The decoded order type and the original expiration timestamp.
    """
    order_type: OrderType = OrderType(expiration >> 62)
    exp_timestamp = expiration & ((1 << 62) - 1)
    return order_type, exp_timestamp
