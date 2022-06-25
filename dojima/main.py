from dojima.brokers import LedgerX
from constants import LEDGERX_JWT


def main():
    # example
    client = LedgerX(jwt_token=LEDGERX_JWT)

    contracts = client.get_contracts(
        active="true", derivative_type="future_contract", limit=5
    )

    print(contracts)


if __name__ == "__main__":
    main()
