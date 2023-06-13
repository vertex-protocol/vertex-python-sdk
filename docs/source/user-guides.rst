User guides
===========

Signing
-------

Signing is handled internally when you instantiate the `VertexClient` (:mod:`vertex_protocol.client.VertexClient`) with a `signer`. Alternatively, 
you can construct the requisite signatures for each execute using a set utils provided by the SDK (see :mod:`vertex_protocol.contracts.eip712` for details).

.. note::

    Check out our docs to learn more about `signing requests <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/signing>`_ in Vertex.

EIP-712
^^^^^^^

Vertex executes are signed using `EIP-712 <https://eips.ethereum.org/EIPS/eip-712>`_ signatures. The following components are needed:

- **types**: The solidity object name and field types of the message being signed.
- **primaryType**: The name of the solidity object being signed.
- **domain**: A protocol-specific object that includes the verifying contract and `chain-id` of the network.
- **message**: The actual message being signed.

You can build the expected EIP-712 typed data for each execute via :mod:`vertex_protocol.contracts.eip712.build_eip712_typed_data()`

**Example:**

.. code-block:: python

    >>> import time
    >>> from vertex_protocol.contracts.types import VertexExecuteType
    >>> from vertex_protocol.engine_client.types import OrderParams, SubaccountParams
    >>> from vertex_protocol.utils import subaccount_to_bytes32, to_x18, to_pow_10, get_expiration_timestamp, gen_order_nonce, OrderType
    >>> from vertex_protocol.contracts.eip712 import build_eip712_typed_data
    >>> verifying_contract = "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6"
    >>> chain_id = 421613
    >>> sender = SubaccountParams(subaccount_owner="0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266", subaccount_name="default")
    >>> order_nonce = gen_order_nonce()
    >>> order_expiration = get_expiration_timestamp(OrderType.DEFAULT, int(time.time()) + 40)
    >>> order =  OrderParams(amount=to_x18(20000), priceX18=to_pow_10(1, 17), expiration=order_expiration, nonce=order_nonce, sender=sender)
    >>> order_typed_data = build_eip712_typed_data(VertexExecuteType.PLACE_ORDER, order.dict(), verifying_contract, chain_id)

The following object is generated and can be signed via :mod:`vertex_protocol.contracts.eip712.sign_eip712_typed_data()`:

.. code-block:: python

    {   
        'types': {
            'EIP712Domain': [
                {'name': 'name', 'type': 'string'},
                {'name': 'version', 'type': 'string'},
                {'name': 'chainId', 'type': 'uint256'},
                {'name': 'verifyingContract', 'type': 'address'}
            ],
            'Order': [
                {'name': 'sender', 'type': 'bytes32'},
                {'name': 'priceX18', 'type': 'int128'},
                {'name': 'amount', 'type': 'int128'},
                {'name': 'expiration', 'type': 'uint64'},
                {'name': 'nonce', 'type': 'uint64'}
            ]
        },
        'primaryType': 'Order',
        'domain': {
            'name': 'Vertex',
            'version': '0.0.1',
            'chainId': 421613,
            'verifyingContract': '0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6'
        },
        'message': {
            'sender': b'\xf3\x9f\xd6\xe5\x1a\xad\x88\xf6\xf4\xcej\xb8\x82ry\xcf\xff\xb9"fdefault\x00\x00\x00\x00\x00',
            'nonce': 1768628938411606731,
            'priceX18': 100000000000000000,
            'amount': 20000000000000000000000,
            'expiration': 1686695965
        }
    }

.. note::

    - You can retrieve the verifying contracts using :mod:`vertex_protocol.engine_client.EngineQueryClient.get_contracts()`. Provided via **client.context.engine_client.get_contracts()** on a `VertexClient` instance.
    - You can also just use the engine client's sign utility :mod:`vertex_protocol.engine_client.EngineExecuteClient.sign()`. Provided via **client.context.engine_client.sign()** on a `VertexClient` instance.