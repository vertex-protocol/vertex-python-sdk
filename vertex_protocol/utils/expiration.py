from enum import IntEnum


class OrderType(IntEnum):
    DEFAULT = 0
    IOC = 1
    FOK = 2
    POST_ONLY = 3


def get_expiration_timestamp(order_type: OrderType, expiration: int) -> int:
    """
    Special order types, such as immediate-or-cancel, are encoded into the expiration field.
    This is a utility to create the proper timestamp needed

    :param order_type: The type of order
    :param expiration: The expiration timestamp in UNIX seconds
    :return: int
    """
    return int(expiration) | (order_type << 62)


def expiration_to_order_type(expiration: int) -> OrderType:
    return expiration >> 62
