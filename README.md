# dojima

A bare bones SDK for trading crypto derivatives on FTX US Derivatives (Formerly LedgerX).

-----

Allows you to trade crypto options, futures, and day ahead swaps on the https://derivs.ftx.us/.

Their API documentation: https://docs.ledgerx.com/docs

### Secrets

LedgerX doesn't provide API keys. Instead they give you a JWT key.
Follow this to get your key: https://docs.ledgerx.com/docs/api-key

I put my keys in a `constants.py` file which I import and pass into the `LedgerX` client.
But feel free to load your secrets how you like.

### Usage

**Instantiating Client**
```python
from dojima.brokers import LedgerX

# example
client = LedgerX(jwt_token=LEDGERX_JWT)
```

**Get Contracts Available**

```python
contracts = client.get_contracts(
    active="true", derivative_type="future_contract", limit=5
)

print(contracts)

```

**Get Quote Data for Contract**

```python

data = client.get_contract_ticker(contract_id=123123)

print(data)
```

**Place Order**

Some things to know:
* LedgerX uses `is_ask` to determine which side the order should go on. `is_ask=True` is a `sell` and `is_ask=False` is a `buy`. (don't ask me why)
* Only `limit` orders are supported as far as I know.
* All prices are in cents, rounded to nearest dollar. (Also don't ask me why)

```python

order = client.create_order(contract_id=123123, is_ask=True, order_type='limit`, size=1, price=12300)

```

**Get Current Orderbook State**

```python

book = client.get_current_book_state(contract_id=123123)

print(book)

```


