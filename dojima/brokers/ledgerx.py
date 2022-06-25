from datetime import datetime
from typing import Optional, Union, List

from requests import Session, HTTPError

APIData = Union[dict, List[dict]]


class LedgerX:
    """
    A REST client for interacting with the LedgerX (Now FTX US Derivatives)
    API for trading crypto options, futures and swaps.

    https://derivs.ftx.us/
    """

    def __init__(self, jwt_token: str) -> None:
        self._jwt_token = jwt_token
        self._session = Session()

    def get_contracts(
        self,
        active: Optional[bool] = None,
        contract_type: Optional[str] = None,
        derivative_type: Optional[str] = None,
        asset: Optional[str] = None,
        before_ts: Optional[datetime] = None,
        after_ts: Optional[datetime] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> APIData:
        """
        Returns a list of contracts.
        https://docs.ledgerx.com/reference/listcontracts

        Args:
            active: true for active contracts only, false for all contracts.
            contract_type: Filter by contract type (Call, Put).
            derivative_type: Filter by derivative type (options_contract, day_ahead_swap, future_contract).
            asset: Filter by asset (USD, ETH, CBTC).
            before_ts: Filter for records created before datetime (UTC).
            after_ts: Filter for records created after datetime (UTC).
            limit: The maximum number of results to return.
            offset: The initial index from which to return the results.

        Returns:
            The list of contracts
        """
        data = {
            "active": active,
            "contract_type": contract_type,
            "derivative_type": derivative_type,
            "asset": asset,
            "before_ts": before_ts,
            "after_ts": after_ts,
            "limit": limit,
            "offset": offset,
        }

        response = self._request(
            "GET", "https://api.ledgerx.com/trading/contracts", data
        )

        return response.get("data")

    def get_traded_contracts(
        self,
        derivative_type: Optional[str] = None,
        asset: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> APIData:
        """
        Returns a list of contracts that you have traded.
        https://docs.ledgerx.com/reference/tradedcontracts

        Args:
            derivative_type: Filter by derivative type.
            asset: Filter by asset.
            limit: The maximum number of results to return.
            offset: The initial index from which to return the results.

        Returns:
            The list of contracts traded.
        """
        data = {
            "derivative_type": derivative_type,
            "asset": asset,
            "limit": limit,
            "offset": offset,
        }

        response = self._request(
            "GET", "https://api.ledgerx.com/trading/contracts/traded", data
        )

        return response.get("data")

    def get_contract_details(self, contract_id: Union[str, int]) -> APIData:
        """
        Returns contract details for a single contract ID.
        https://docs.ledgerx.com/reference/retrievecontract

        Args:
            contract_id: ID of record to fetch.

        Returns:
            Contract details.
        """
        response = self._request(
            "GET", f"https://api.ledgerx.com/trading/contracts/{contract_id}"
        )

        return response.get("data")

    def get_contract_position(self, contract_id: Union[str, int]) -> APIData:
        """
        Returns your position for a given contract.
        https://api.ledgerx.com/trading/contracts/{id}/position

        Args:
            contract_id: ID of record to fetch.

        Returns:
            Position details.
        """
        response = self._request(
            "GET", f"https://api.ledgerx.com/trading/contracts/{contract_id}/position"
        )

        return response.get("data")

    def get_contract_ticker(
        self,
        contract_id: Union[str, int],
        time: Optional[datetime] = None,
        asset: Optional[str] = None,
    ) -> APIData:
        """
        Snapshot information about the current best bid/ask, 24h volume, and last trade.

        **This endpoint has a rate limit of 10 requests per minute.**
        For real-time updates, it is recommended to connect to the Websocket Market Data Feed.

        https://docs.ledgerx.com/reference/contractticker

        Args:
            contract_id: Contract ID. Also supports day-ahead keyword to get info about the next-day swap.
            time: Get contract snapshot at a specific time. Defaults to current time if not provided.
            asset: If getting day-ahead ticker, must specify which asset (USD, ETH, CBTC).

        Returns:
            Ticker information for the specified contract. All prices in cents.
        """

        data = {
            "time": time,
            "asset": asset,
        }

        response = self._request(
            "GET",
            f"https://api.ledgerx.com/trading/contracts/{contract_id}/ticker",
            data,
        )

        return response.get("data")

    def get_positions(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> APIData:
        """
        Returns all your positions.
        https://docs.ledgerx.com/reference/listpositions

        Args:
            limit: The maximum number of results to return.
            offset: The initial index from which to return the results.

        Returns:
            List of positions.
        """

        data = {
            "limit": limit,
            "offset": offset,
        }

        response = self._request(
            "GET", f"https://api.ledgerx.com/trading/positions", data
        )

        return response.get("data")

    def get_trades_for_position(self, contract_id: Union[str, int]) -> APIData:
        """
        Returns a list of your trades for a given position.
        https://docs.ledgerx.com/reference/tradesposition

        Args:
            contract_id: ID of record to fetch.

        Returns:
            List of trades.
        """

        response = self._request(
            "GET", f"https://api.ledgerx.com/trading/positions/{contract_id}/trades"
        )

        return response.get("data")

    def get_open_orders(self) -> APIData:
        """
        Get all resting limit orders directly from the exchange.
        https://docs.ledgerx.com/reference/open-orders

        Returns:
            A list of your open orders.
        """

        response = self._request("GET", "https://trade.ledgerx.com/api/open-orders")

        return response.get("data")

    def create_order(
        self,
        contract_id: Union[str, int],
        order_type: str,
        is_ask: bool,
        size: int,
        price: int,
        volatile: Optional[bool] = False,
        swap_purpose: str = "undisclosed",
    ) -> APIData:
        """
        Place an order.
        This endpoint returns the message id, or mid, of the order.
        Subsequent fills or cancels for this original order will be sent over the websocket feed with the same mid.

        This endpoint has a rate limit of 200 requests per minute.

        https://docs.ledgerx.com/reference/create-order

        Args:
            contract_id: ID of the contract to place the order on.
            order_type: limit
            is_ask: Order side. true to sell; false to buy.
            size: How many units of the contract to transact.
            price: The limit price in cents (USD) per contract. Must be a whole dollar amount.
            volatile: true to auto-cancel order at 4PM. false to persist order until filled.
            swap_purpose: bf_hedge for bona-fide hedge; non_bf_hedge; undisclosed.

        Returns:
            Returns the message id, or mid, of the order.
        """

        data = {
            "contract_id": contract_id,
            "order_type": order_type,
            "is_ask": is_ask,
            "size": size,
            "price": price,
            "volatile": volatile,
            "swap_purpose": swap_purpose,
        }

        response = self._request("POST", "https://trade.ledgerx.com/api/orders", data)

        return response.get("data")

    def delete_all_orders(self) -> APIData:
        """
        Delete all outstanding orders associated with your MPID (the whole organization)

        https://docs.ledgerx.com/reference/cancel-all

        Returns:
            Success (200), Unauthorized (401)
        """

        response = self._request("DELETE", "https://trade.ledgerx.com/api/orders")

        return response.get("data")

    def delete_single_order(self, mid: str, contract_id: Union[str, int]) -> APIData:
        """
        Cancel a single resting limit order

        https://docs.ledgerx.com/reference/cancel-single

        Args:
            mid: The message id (mid) of the original order.
            contract_id: The contract ID of the original order.

        Returns:
            Success (200), Bad Request (400)
        """

        data = {"contract_id": contract_id}

        response = self._request(
            "DELETE", f"https://trade.ledgerx.com/api/orders/{mid}", data
        )

        return response.get("data")

    def patch_order(
        self, mid: str, contract_id: Union[str, int], price: int, size: int
    ) -> APIData:
        """
        Cancel and replace order.

        Atomically swap an existing resting limit order with a new resting limit order.
        Price, side and size may be changed.

        https://docs.ledgerx.com/reference/cancel-replace

        Args:
            mid: The message id (mid) of the original order.
            contract_id: The contract ID of the original order.
            price: The limit price of the new order in cents (USD) per contract. Must be a whole dollar amount.
            size: How many units of the contract to transact for the new order.

        Returns:
            Success (200), Bad Request (400)
        """

        data = {"contract_id": contract_id, "price": price, "size": size}

        response = self._request(
            "DELETE", f"https://trade.ledgerx.com/api/orders/{mid}/edit", data
        )

        return response.get("data")

    def get_current_book_state(self, contract_id: Union[str, int]) -> APIData:
        """
        Request the current book state for a contract

        This endpoint has rate limits of 500 requests per minute and 3000 requests per 10 minutes.

        https://docs.ledgerx.com/reference/book-state-contract

        Args:
            contract_id: ID of record to fetch.

        Returns:
            Returns the current book state for a contract
        """

        response = self._request(
            "GET", f"https://trade.ledgerx.com/api/book-states/{contract_id}"
        )

        return response.get("data")

    def _request(self, method: str, url: str, data: Optional[dict] = None) -> APIData:
        """Utility method for submitting HTTP requests.

        Args:
            method: The type of HTTP request ("POST", "GET", "DELETE", etc)
            url: The endpoint URL.
            data: The payload parameters, if any.

        Returns:
            The API response.
        """
        headers = {"Authorization": "JWT " + self._jwt_token}

        opts = {
            "headers": headers,
            "allow_redirects": False,
        }

        if method.upper() in ["GET", "DELETE"]:
            opts["params"] = data
        else:
            opts["json"] = data

        response = self._session.request(method, url, **opts)

        try:
            response.raise_for_status()
        except HTTPError as error:
            print("error: ", error)
            return {}

        if response.text != "":
            return response.json()
        else:
            # return status code for empty response
            return {"data": {"status": response.status_code}}