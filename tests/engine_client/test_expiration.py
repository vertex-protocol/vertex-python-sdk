from vertex_protocol.utils.expiration import (
    OrderType,
    decode_expiration,
    get_expiration_timestamp,
)


def test_expiration_encoding():
    unix_epoch = 1685939478

    for order_type in [
        OrderType.DEFAULT,
        OrderType.IOC,
        OrderType.FOK,
        OrderType.POST_ONLY,
    ]:
        encoded_expiration = get_expiration_timestamp(order_type, unix_epoch)
        decoded_order_type, decoded_unix_epoch = decode_expiration(encoded_expiration)

        assert decoded_unix_epoch == unix_epoch
        assert decoded_order_type == order_type


def test_reduce_only():
    unix_epoch = 1685939478

    def is_reduce_only(expiration: int):
        return (expiration & (1 << 61)) != 0

    reduced_only_expiration = get_expiration_timestamp(
        OrderType.FOK, unix_epoch, reduce_only=True
    )
    non_reduced_only_expiration = get_expiration_timestamp(OrderType.FOK, unix_epoch)

    assert is_reduce_only(reduced_only_expiration)
    assert not is_reduce_only(non_reduced_only_expiration)
    assert not is_reduce_only(
        get_expiration_timestamp(OrderType.FOK, unix_epoch, bool(None))
    )
