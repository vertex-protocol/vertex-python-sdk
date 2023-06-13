User reference
==============

Core client
-----------
You must initialize the Vertex client via the `create_vertex_client` util for proper setup:

.. note::

    You can instantiate the client by providing either a private key, or an instance of `LocalAccount`.

.. code-block:: python
    
    >>> from eth_account import Account
    >>> from eth_account.signers.local import LocalAccount
    >>> from vertex_protocol.client import create_vertex_client
    >>> client_from_private_key = create_vertex_client("mainnet", "xxx")
    >>> signer: LocalAccount = Account.from_key("xxx")
    >>> client_from_signer = create_vertex_client("mainnet", signer)

See :mod:`vertex_protocol.client.create_vertex_client()` for details.

.. note::

    **Your private key is only used to sign transactions locally.** You can optionally interact with the EIP-712 utilities directly (see :ref:`eip-712`) to construct the required signatures for each of Vertex's executes. 

The core Vertex client is sub-divided into the following APIs:

Market API
----------
The Market API allows you to manage and execute orders on the Vertex Protocol. Here, you can explore:

- `Placing an order <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/executes/place-order>`_:

.. code-block:: python

    >>> from vertex-protocol.engine_client.types import OrderParams, PlaceOrderParams
    >>> order = OrderParams(...)
    >>> client.market.place_order(PlaceOrderParams(order=order, ...))

- `Canceling an order <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/executes/cancel-orders>`_:

.. code-block:: python

    >>> from vertex-protocol.engine_client.types import CancelOrdersParams
    >>> client.market.cancel_orders(CancelOrdersParams(...))

- `Cancelling all orders <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/executes/cancel-product-orders>`_:

.. code-block:: Python

    >>> from vertex-protocol.engine_client.types import CancelProductOrdersParams
    >>> client.market.cancel_product_orders(CancelProductOrdersParams(...))

- `Minting LP <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/executes/mint-lp>`_:

    >>> from vertex-protocol.engine_client.types import MintLpParams
    >>> client.market.mint_lp(MintLpParams(...))

- `Burning LP <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/executes/burn-lp>`_:

    >>> from vertex-protocol.engine_client.types import BurnLpParams
    >>> client.market.burn_lp(BurnLpParams(...))

You also have available the following queries:

- `Retrieves all market states from the off-chain engine <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/queries/all-products>`_:

.. code-block:: python

    >>> client.market.get_all_engine_markets()

- `Retrieves liquidity per price tick from the engine <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/queries/market-liquidity>`_:

.. code-block:: python

    >>> client.market.get_market_liquidity()

- `Retrieves the latest off-chain orderbook price for a specific product <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/queries/market-price>`_:

.. code-block:: python

    >>> client.market.get_latest_market_price(1)

- `Retrieves subaccount open orders <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/queries/subaccount-orders>`_:

.. code-block:: python

    >>> sender = "0xe526299d13c956ed6b9b3e03086a152c6396947364656661756c740000000000"
    >>> client.market.get_subaccount_open_orders(1, sender)

-  `Retrieves subaccount historical orders <https://vertex-protocol.gitbook.io/docs/developer-resources/api/indexer-api/orders>`_:

.. code-block:: python

    >>> from vertex_protocol.indexer_client.types import IndexerSubaccountHistoricalOrdersParams
    >>> sender = "0xe526299d13c956ed6b9b3e03086a152c6396947364656661756c740000000000"
    >>> params = IndexerSubaccountHistoricalOrdersParams(subaccount=sender)
    >>> client.market.get_subaccount_historical_orders(params)

- `Retrieves historical orders by digest <https://vertex-protocol.gitbook.io/docs/developer-resources/api/indexer-api/orders>`_:

.. code-block:: python

    >>> digests = ["0xf4f7a8767faf0c7f72251a1f9e5da590f708fd9842bf8fcdeacbaa0237958fff"]
    >>> client.market.get_historical_orders_by_digest(digests)

- `Retrieves the max amount of LP mintable possible for a subaccount <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/queries/max-lp-mintable>`_:

.. code-block:: python

    >>> sender = "0xe526299d13c956ed6b9b3e03086a152c6396947364656661756c740000000000"
    >>> client.market.get_max_lp_mintable(1, sender)

- `Retrieves candlesticks for a product <https://vertex-protocol.gitbook.io/docs/developer-resources/api/indexer-api/candlesticks>`_:

.. code-block:: python

    >>> from vertex_protocol.indexer_client.types import IndexerCandlesticksParams, IndexerCandlesticksGranularity
    >>> params = IndexerCandlesticksParams(product_id=1, granularity=IndexerCandlesticksGranularity.FIVE_MINUTES)
    >>> client.market.get_candlesticks(params)

- `Retrieves the latest funding rate for a specific perp product <https://vertex-protocol.gitbook.io/docs/developer-resources/api/indexer-api/funding-rate>`_:

.. code-block:: python

    >>> client.market.get_perp_funding_rate(2)

- `Retrieves the latest oracle prices for provided products <https://vertex-protocol.gitbook.io/docs/developer-resources/api/indexer-api/oracle-price>`_:

.. code-block:: python

    >>> client.market.get_oracle_prices([1, 2, 3, 4])

- `Retrieves $VRTX token rewards for a wallet <https://vertex-protocol.gitbook.io/docs/developer-resources/api/indexer-api/rewards>`_:

.. code-block:: python

    >>> wallet = "0xf8d240d9514c9a4715d66268d7af3b53d6196425"
    >>> client.market.get_token_rewards(wallet)

.. note::

    See :mod:`vertex_protocol.client.apis.MarketAPI` to explore all available operations.

Spot API
--------
The Spot API allows you to manage your spot collaterals. Here, you can explore:

- `Making a deposit <https://vertex-protocol.gitbook.io/docs/developer-resources/api/depositing>`_:

.. code-block:: python

    >>> from vertex_protocol.utils.math import to_pow_10
    >>> from vertex_protocol.contracts.types import DepositCollateralParams
    >>> deposit_tx_hash = client.spot.deposit(
            DepositCollateralParams(
                subaccount_name="default", product_id=0, amount=to_pow_10(100000, 6)
            )
        )

See :mod:`vertex_protocol.client.apis.SpotExecuteAPI.deposit()` for details.

- `Withdrawing collateral <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/executes/withdraw-collateral>`_:

.. code-block:: python

    >>> from vertex_protocol.engine_client.types import WithdrawCollateralParams
    >>> sender = "0xe526299d13c956ed6b9b3e03086a152c6396947364656661756c740000000000"
    >>> withdraw_collateral_params = WithdrawCollateralParams(
            productId=0, amount=to_pow_10(10000, 6), sender=sender
        )
    >>> client.spot.withdraw(withdraw_collateral_params)

.. note::

    See :mod:`vertex_protocol.client.apis.SpotAPI` to explore all available operations.

Perp API
--------
The Perp API for actions and queries specific to Perps. Here, you can explore:

- `Retrieves the latest index and mark price for a specific perp product <https://vertex-protocol.gitbook.io/docs/developer-resources/api/indexer-api/perp-prices>`_:

.. code-block:: python

    >>> client.perp.get_prices(2)

.. note::

    See :mod:`vertex_protocol.client.apis.PerpAPI` to explore all available operations.

Subaccount API
--------------
The Subaccount API allows you to manage your subaccounts. Here, you can explore:

- `Link a signer to a subaccount <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/executes/link-signer>`_:

.. code-block:: python

    >>> from vertex_protocol.engine_client.types import LinkSignerParams
    >>> params = LinkSignerParams(signer="0xeae27ae6412147ed6d5692fd91709dad6dbfc34264656661756c740000000000")
    >>> client.subaccount.link_signer(params)

- `Retrieves the sate of a subaccount in the off-chain engine <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/queries/subaccount-info>`_:

.. code-block:: python

    >>> sender = "0xe526299d13c956ed6b9b3e03086a152c6396947364656661756c740000000000"
    >>> client.subaccount.get_engine_subaccount_summary(sender)


- `Retrieves subaccount fee rates <https://vertex-protocol.gitbook.io/docs/developer-resources/api/websocket-rest-api/queries/fee-rates>`_:

.. code-block:: python

    >>> sender = "0xe526299d13c956ed6b9b3e03086a152c6396947364656661756c740000000000"
    >>> client.subaccount.get_subaccount_fee_rates(sender)

.. note::

    See :mod:`vertex_protocol.client.apis.SubaccountAPI` to explore all available operations.

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

.. note::

    See :mod:`vertex_protocol.engine_client` to explore all available operations.

Indexer Client
--------------
The Indexer Client provides functionalities for interacting with the Vertex Protocol indexer. This can be particularly useful for fetching historical data. Here you can explore:

.. code-block:: python

    >>> # Retrieves subaccount historical matches.
    >>> client.context.indexer_client.get_matches(...)
    >>> # Retrieves linked signer rate limits
    >>> client.context.indexer_client.get_linked_signer_rate_limits(...)

.. note::

    See :mod:`vertex_protocol.indexer_client` to explore all available operations.

Vertex Contracts
----------------

A utility module to interact directly with Vertex contracts. You can interface with this module via the client's context (see :mod:`vertex_protocol.client.VertexClientContext`). 

.. code-block:: python

    >>> # approving allowance
    >>> client.context.contracts.approve_allowance(...)
    >>> # executing a contract function, retrieves the OffchainBook for product_id 1
    >>> client.context.contract.endpoint.functions.getBook(1).call()

.. note::

    See :mod:`vertex_protocol.contracts.VertexContracts` to explore all available operations.

Vertex utils
----------------

A set of utility helpers. See :mod:`vertex_protocol.utils`.

See  :doc:`api-reference` for detailed information about each module. 
