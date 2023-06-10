Getting Started
===============

Introduction
------------

This SDK offers methods to perform all operations on Vertex such as making a deposit, placing orders, viewing open orders, obtaining an order digest, cancelling an order, withdrawing collateral and more.

Basic Usage
-----------

Before you start, import the necessary libraries and functions:

.. code-block:: python

    import time
    from vertex_protocol.client import create_vertex_client
    from vertex_protocol.engine_client.types.execute import (
        OrderParams,
        PlaceOrderParams,
        WithdrawCollateralParams,
        CancelOrdersParams
    )
    from vertex_protocol.utils.bytes32 import subaccount_to_bytes32, subaccount_to_hex
    from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
    from vertex_protocol.utils.math import to_pow_10, to_x18
    from vertex_protocol.utils.nonce import gen_order_nonce
    from vertex_protocol.utils.subaccount import SubaccountParams

The following sections outline the main functionalities.

Making a Deposit
----------------

.. code-block:: python

    >>> private_key = "xxx"

    >>> print("setting up vertex client...")
    >>> client = create_vertex_client("testnet", private_key)

    >>> print("depositing collateral...")
    >>> deposit_tx_hash = client.spot.deposit(
        {"subaccount_name": "default", "product_id": 0, "amount": to_pow_10(100000, 6)}
    )
    >>> print("deposit collateral tx hash:", deposit_tx_hash)

Placing an Order
----------------

.. code-block:: python

    >>> owner = client.context.engine_client.signer.address
    >>> print("placing order...")
    >>> product_id = 1
    >>> order = OrderParams(
            sender=SubaccountParams(
                subaccount_owner=owner,
                subaccount_name="default",
            ),
            priceX18=to_x18(20000),
            amount=to_pow_10(1, 17),
            expiration=get_expiration_timestamp(OrderType.POST_ONLY, int(time.time()) + 40),
            nonce=gen_order_nonce(),
        )
    >>> res = client.market.place_order(PlaceOrderParams(product_id=1, order=order))
    >>> print("order result:", res.json(indent=2))

Viewing Open Orders
-------------------

.. code-block:: python

    >>> sender = subaccount_to_hex(order.sender)
    >>> print("querying open orders...")
    >>> open_orders = client.market.get_subaccount_open_orders(1, sender)
    >>> print("open orders:", open_orders.json(indent=2))

Getting Order Digest
--------------------

.. code-block:: python

    >>> order.sender = subaccount_to_bytes32(order.sender)
    >>> order_digest = client.context.engine_client.get_order_digest(order, product_id)
    >>> print("order digest:", order_digest)

Cancelling an Order
-------------------

.. code-block:: python

    >>> print("cancelling order...")
    >>> res = client.market.cancel_orders(
            CancelOrdersParams(productIds=[product_id], digests=[order_digest], sender=sender)
        )
    >>> print("cancel order result:", res.json(indent=2))

Withdrawing Collateral
----------------------

.. code-block:: python

    >>> print("withdrawing collateral...")
    >>> withdraw_collateral_params = WithdrawCollateralParams(
            productId=0, amount=to_pow_10(10000, 6), sender=sender
        )
    >>> res = client.spot.withdraw(withdraw_collateral_params)
    >>> print("withdraw result:", res.json(indent=2))


Now you should be able to perform basic operations with the Vertex Protocol Python SDK. Remember to always keep your signer's private key securely stored and never expose it to the public.
