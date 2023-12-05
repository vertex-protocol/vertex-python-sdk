# Vertex Protocol Python SDK

This is the Python SDK for the [Vertex Protocol API](https://vertex-protocol.gitbook.io/docs/developer-resources/api).

See [SDK docs](https://vertex-protocol.github.io/vertex-python-sdk/index.html) to get started.

## Requirements

- Python 3.9 or above

## Installation

You can install the SDK via pip:

```bash
pip install vertex-protocol
```

## Basic usage

### Import the necessary utilities:

```python
from vertex_protocol.client import create_vertex_client, ClientMode
from vertex_protocol.contracts.types import DepositCollateralParams
from vertex_protocol.engine_client.types.execute import (
    OrderParams,
    PlaceOrderParams
)
from vertex_protocol.utils.expiration import OrderType, get_expiration_timestamp
from vertex_protocol.utils.math import to_pow_10, to_x18
from vertex_protocol.utils.nonce import gen_order_nonce
```

### Create the VertexClient providing your private key:

```python
print("setting up vertex client...")
private_key = "xxx"
client = create_vertex_client(ClientMode.MAINNET, private_key)
```

### Perform basic operations:

```python
# Depositing collaterals
print("approving allowance...")
approve_allowance_tx_hash = client.spot.approve_allowance(0, to_pow_10(100000, 6))
print("approve allowance tx hash:", approve_allowance_tx_hash)

print("querying my allowance...")
token_allowance = client.spot.get_token_allowance(0, client.context.signer.address)
print("token allowance:", token_allowance)

print("depositing collateral...")
deposit_tx_hash = client.spot.deposit(
   DepositCollateralParams(
      subaccount_name="default", product_id=0, amount=to_pow_10(100000, 6)
   )
)
print("deposit collateral tx hash:", deposit_tx_hash)

# Placing orders
print("placing order...")
owner = client.context.engine_client.signer.address
product_id = 1
order = OrderParams(
   sender=SubaccountParams(
      subaccount_owner=owner,
      subaccount_name="default",
   ),
   priceX18=to_x18(20000),
   amount=to_pow_10(1, 17),
   expiration=get_expiration_timestamp(OrderType.POST_ONLY, int(time.time()) + 40),
   nonce=gen_order_nonce(),
)
res = client.market.place_order({"product_id": product_id, "order": order})
print("order result:", res.json(indent=2))
```

See [Getting Started](https://vertex-protocol.github.io/vertex-python-sdk/getting-started.html) for more.

## Running locally

1. Clone [github repo](https://github.com/vertex-protocol/vertex-python-sdk)

2. Install poetry

```

$ curl -sSL https://install.python-poetry.org | python3 -

```

3. Setup a virtual environment and activate it

```

$ python3 -m venv venv
$ source ./venv/bin/activate

```

4. Install dependencies via `poetry install`
5. Setup an `.env` file and set the following envvars

```shell
CLIENT_MODE='mainnet|sepolia-testnet|devnet'
SIGNER_PRIVATE_KEY="0x..."
LINKED_SIGNER_PRIVATE_KEY="0x..." # not required
```

### Run tests

```
$ poetry run test
```

### Run sanity checks

- `poetry run client-sanity`: runs sanity checks for the top-level client.
- `poetry run engine-sanity`: runs sanity checks for the `engine-client`.
- `poetry run indexer-sanity`: runs sanity checks for the `indexer-client`.
- `poetry run contracts-sanity`: runs sanity checks for the contracts module.

### Build Docs

To build the docs locally run:

```
$ poetry run sphinx-build docs/source docs/build
```
