# Vertex Python's SDK

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
   PRIVATE_KEY="xxx"
   ```

# Run tests

```
$ poetry run test
```

# Run sanity checks

- `poetry run engine-sanity`: runs sanity checks for the `engine-client`.
- `poetry run indexer-sanity`: runs sanity checks for the `indexer-client`.
- `poetry run client-sanity`: runs sanity checks for the top-level client.
