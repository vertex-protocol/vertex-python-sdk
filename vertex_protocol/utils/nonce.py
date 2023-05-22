import datetime
import random


def gen_order_nonce(recv_time_ms=None, random_int=None) -> int:
    """Generates an order nonce based on recv_time_ms in milliseconds, defaulting to current_time + 90 seconds"""
    if recv_time_ms is None:
        recv_time_ms = int(
            (datetime.datetime.now() + datetime.timedelta(seconds=90)).timestamp()
            * 1000
        )
    if random_int is None:
        random_int = random.randint(0, 999)

    return (recv_time_ms << 20) + random_int
