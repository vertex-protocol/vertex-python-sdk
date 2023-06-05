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
