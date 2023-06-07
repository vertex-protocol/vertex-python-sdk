# Vertex Python SDK

```python
print("Hello Vertex")
```

# Development

1. Install poetry
   ```
   $ curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Setup a virtual environment and activate it

   ```
   $ python3 -m venv venv
   $ source ./venv/bin/activate
   ```

3. Install dependencies via `poetry install`
4. Setup an `.env` file and set the following envvars

   ```shell
   CLIENT_MODE='mainnet|testnet|devnet'
   SIGNER_PRIVATE_KEY="0x..."
   LINKED_SIGNER_PRIVATE_KEY="0x..." # not required
   ```

# Run tests

```
$ poetry run test
```

# Run sanity checks

- `poetry run client-sanity`: runs sanity checks for the top-level client.
- `poetry run engine-sanity`: runs sanity checks for the `engine-client`.
- `poetry run indexer-sanity`: runs sanity checks for the `indexer-client`.
- `poetry run contracts-sanity`: runs sanity checks for the contracts module.

# Docs

Regenerates SDK docs.

```
$ poetry run sphinx-build docs/source docs/build
```
