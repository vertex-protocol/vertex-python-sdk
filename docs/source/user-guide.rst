User Guide
==========

The core Vertex client is sub-divided in the following APIs:

Market API
----------
The Market API allows you to manage and execute orders on the Vertex Protocol. Here, you can explore:

- Placing an order: Use `client.market.place_order()`
- Canceling an order: Use `client.market.cancel_orders()`
- Viewing open orders: Use `client.market.get_subaccount_open_orders()`
- Getting order digest: Use `client.context.engine_client.get_order_digest()`
- Fetching market liquidity: Use `client.market.get_market_liquidity()`
- And many more operations.

Spot API
--------
The Spot API allows you to manage your spot transactions. Here, you can explore:

- Making a deposit: Use `client.spot.deposit()`
- Withdrawing collateral: Use `client.spot.withdraw()`
- Checking token balance: Use `client.spot.get_token_wallet_balance()`
- And many more operations.

Perp API
--------
The Perp API allows you to manage your perpetual transactions. Here, you can explore:

- Querying perp prices: Use `client.perp.get_prices()`
- Getting funding rate: Use `client.perp.get_perp_funding_rate()`
- And many more operations.

Subaccount API
--------------
The Subaccount API allows you to manage your subaccounts. Here, you can explore:

- Fetching subaccount summary: Use `client.subaccount.get_engine_subaccount_summary()`
- Fetching subaccount fee rates: Use `client.subaccount.get_subaccount_fee_rates()`
- And many more operations.

Engine Client
-------------
The Engine Client provides low-level functionalities that are integral to interacting with the Vertex Protocol, including:

- Signing transactions: 

.. code-block:: python

    >>> client.context.engine_client.sign(...)

- Getting the signer address: 

.. code-block:: python

    >>> client.context.engine_client.signer.address

- Getting an order digest: 

.. code-block:: python

    >>> client.context.engine_client.get_order_digest()

Indexer Client
--------------
The Indexer Client provides functionalities for interacting with the Vertex Protocol indexer. This can be particularly useful for fetching historical data. Here you can explore:

- Querying candlestick data: Use `client.market.get_candlesticks()`
- Querying product snapshots: Use `client.market.get_product_snapshots()`
- And many more operations.

See  :doc:`api-reference` for detailed information about each module. 
