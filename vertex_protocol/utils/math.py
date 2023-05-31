def to_pow_10(x: int, pow: int) -> int:
    return x * 10**pow


def to_x18(x: int) -> int:
    return to_pow_10(x, 18)


def from_pow_10(x: int, pow: int) -> float:
    return float(x) / 10**pow


def from_x18(x: int) -> float:
    return from_pow_10(x, 18)
