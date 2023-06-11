def to_pow_10(x: int, pow: int) -> int:
    """
    Converts integer to power of 10 format.

    Args:
        x (int): Integer value.

        pow (int): Power of 10.

    Returns:
        int: Converted value.
    """
    return x * 10**pow


def to_x18(x: int) -> int:
    """
    Converts integer to power of 10^18 format.

    Args:
        x (int): Integer value.

    Returns:
        int: Converted value.
    """
    return to_pow_10(x, 18)


def from_pow_10(x: int, pow: int) -> float:
    """
    Reverts integer from power of 10 format.

    Args:
        x (int): Converted value.

        pow (int): Power of 10.

    Returns:
        float: Original value.
    """
    return float(x) / 10**pow


def from_x18(x: int) -> float:
    """
    Reverts integer from power of 10^18 format.

    Args:
        x (int): Converted value.

    Returns:
        float: Original value.
    """
    return from_pow_10(x, 18)
