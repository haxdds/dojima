# dojima

![PyPI][(https://img.shields.io/pypi/v/dojima?color=red)](https://pypi.org/project/dojima/)
![PyPI - Python Version][(https://img.shields.io/pypi/pyversions/dojima?color=red)](https://pypi.org/project/dojima/)

A bare bones SDK for trading crypto derivatives on FTX US Derivatives (Formerly LedgerX).

Named after the [dojima rice exchange](https://en.wikipedia.org/wiki/D%C5%8Djima_Rice_Exchange), which was the world's first futures exchange.

-----

Allows you to trade crypto options, futures, and day ahead swaps on the https://derivs.ftx.us/.

Their API documentation: https://docs.ledgerx.com/docs

**Note: This code has not been tested!!! Use at your own risk!**

### Secrets

LedgerX doesn't provide API keys. Instead they give you a JWT key.
Follow this to get your key: https://docs.ledgerx.com/docs/api-key

I put my keys in a `constants.py` file which I import and pass into the `LedgerX` client.
But feel free to load your secrets how you like.

### Installation

Install from [pypi](https://pypi.org/project/dojima/) using pip.

```
pip install dojima
```

This also works for a poetry environment.

```
poetry add dojima
```

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

*Some things to know:*
* LedgerX uses `is_ask` parameter to determine which side the order should go on (don't ask me why). This means that `is_ask=True` is a `sell` and `is_ask=False` is a `buy`. 
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


