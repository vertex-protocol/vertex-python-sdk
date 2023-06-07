import datetime
import random


def gen_order_nonce(
    recv_time_ms: int | None = None, random_int: int | None = None
) -> int:
    """
    Generates an order nonce based on a received timestamp and a random integer.

    Args:
        recv_time_ms (int, optional): Received timestamp in milliseconds. Defaults to the current time plus 90 seconds.

        random_int (int, optional): An integer for the nonce. Defaults to a random integer between 0 and 999.

    Returns:
        int: The generated order nonce.
    """
    if recv_time_ms is None:
        recv_time_ms = int(
            (datetime.datetime.now() + datetime.timedelta(seconds=90)).timestamp()
            * 1000
        )
    if random_int is None:
        random_int = random.randint(0, 999)

    return (recv_time_ms << 20) + random_int
