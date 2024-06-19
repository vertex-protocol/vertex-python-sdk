from enum import IntEnum
import time


class TimeInSeconds(IntEnum):
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    YEAR = 31536000


def millis_to_seconds(millis: int) -> int:
    return millis // 1000


def now_in_seconds() -> int:
    return millis_to_seconds(int(time.time() * 1000))
