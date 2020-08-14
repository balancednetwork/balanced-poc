from iconservice import *
from .utils.checks import *
from .scorelib import *

TAG = 'BalancedDEX'

ICX = 1000000000000000000
MIN_PRICE = 10 * ICX

# An interface of token to distribute daily rewards
class TokenInterface(InterfaceScore):
    @interface
    def transfer(self, _to: Address, _value: int, _data: bytes=None):
        pass

    @interface
    def balanceOf(self, _owner: Address) -> int:
        pass

    @interface
    def symbol(self, _owner: Address) -> str:
        pass


class DEX(IconScoreBase):
    _TOTAL_EXCHANGED = 'total_exchanged'
    _MARKETS = 'markets'
    _ORDERS = 'orders'
    _COMPLETED = 'completed'
    _CANCELLED = 'cancelled'
    _ORDER_OWNER = 'order_owner'
    _ORDER_BOOK = 'buy_order_book'
    _EXCHANGE_ON = 'exchange_on'

    @eventlog(indexed=3)
    def Transfer(self, _from: Address, _to: Address, _value: int, _data: bytes):
        pass

    @eventlog(indexed=2)
    def FundTransfer(self, destination: Address, amount: int, note: str):
        pass

    @eventlog(indexed=2)
    def TokenTransfer(self, recipient: Address, amount: int, note: str):
        pass

    @eventlog(indexed=3)
    def SellOrderCreated(self, market: str, amount: int, price: int, time_stamp: int, tx_hash: str):
        pass

    @eventlog(indexed=3)
    def BuyOrderCreated(self, market: str, amount: int, price: int, time_stamp: int, tx_hash: str):
        pass

    @eventlog(indexed=3)
    def SellOrderFilled(self, market: str, amount: int, price: int, time_stamp: int, tx_hash: str):
        pass

    @eventlog(indexed=3)
    def BuyOrderFilled(self, market: str, amount: int, price: int, time_stamp: int, tx_hash: str):
        pass

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._total_exchanged = VarDB(self._TOTAL_EXCHANGED, db, value_type=int)
        self._markets = ArrayDB(self._MARKETS, db, value_type=str)
        self._orders = DictDB(self._ORDERS, db, value_type=str, depth=2)
        self._bid_books = [RedBlackTreeDB(f'bid_{market}', db, value_type=int) for market in self._markets]
        self._ask_books = [RedBlackTreeDB(f'ask_{market}', db, value_type=int) for market in self._markets]
        self._completed = ArrayDB(self._COMPLETED, db, value_type=str)
        self._cancelled = ArrayDB(self._CANCELLED, db, value_type=str)
        self._order_owner = DictDB(self._ORDER_OWNER, db, value_type=Address)
        self._exchange_on = VarDB(self._EXCHANGE_ON, db, value_type=bool)

    def on_install(self) -> None:
        super().on_install()
        self._exchange_on.set(False)

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def name(self) -> str:
        return "BalancedDEX"

    @external
    def exchange_on(self) -> None:
        """
        Allows the exchange to start accepting orders.
        """
        if self.msg.sender != self.owner:
            revert(f'Only the exchange owner can turn it on.')
        if not self._exchange_on.get():
            self._exchange_on.set(True)

    @external(readonly=True)
    def get_exchange_on(self) -> bool:
        """
        Returns the on/off state of the exchange.
        """
        return self._exchange_on.get()

    @external
    def add_market(self, _market_name: str, _base: Address, _quote: Address,
                   _base_prec: int, _quote_prec: int) -> None:
        """

        """

    @external(readonly=True)
    def total_exchanged(self) -> int:
        """
        Returns the total amount of TAP exchanged.
        :return: Total TAP exchanged.
        :rtype: int
        """
        return self._total_exchanged.get()

    @external
    def tokenFallback(self, _from: Address, _value: int, _data: bytes) -> None:
        """
        Directs incoming tokens to either create or fill an order.
        :param _from: Token orgination address.
        :type _from: :class:`iconservice.base.address.Address`
        :param _value: Number of tokens sent.
        :type _value: int
        :param _data: Method and parameters to call once tokens are received.
        :type _data: bytes
        """
        if self.msg.sender != self._token_score.get():
            revert(f'This DEX can only handle symbol tokens.')
        Logger.debug(f'({_value}) symbol tokens received from {_from}.', TAG)
        try:
            Logger.debug(f'Decoding the _data sent with the tokens.', TAG)
            d = json_loads(_data.decode("utf-8"))
        except BaseException as e:
            Logger.debug(f'Invalid data with token transfer. Exception: {e}', TAG)
            revert(f'Invalid data: {_data}, returning symbol. Exception: {e}')
        if set(d.keys()) != set(["method", "params"]):
            revert('Invalid parameters.')
        if d["method"] == "list_for_sale":
            self._list_for_sale(_from,
                               _value,
                               d["params"].get("price", -1))
        elif d["method"] == "sell":
            self._sell(_from,
                      _value,
                      d["params"].get("price", -1),
                      d["params"].get("tx_hash", ""))
        else:
            revert(f'No valid method called, data: {_data}')

    def _get_matches(self, _market: int, _order_type: int, _price: int, _amount: int) -> dict:
        """
        """

    def _sell(self, _from: Address, _amount: int, _price: int, _tx_hash: str) -> None:
        """
        Fills a buy order in the order book.
        :param _from: Token orgination address.
        :type _from: :class:`iconservice.base.address.Address`
        :param _amount: Number of tokens sent.
        :type _amount: int
        :param _price: Confirmation of order book offer price.
        :type _price: int
        :param _tx_hash: Order identifier.
        :type _tx_hash: str
        """
        pass

    def _list_for_sale(self, _from: str, _amount: int, _price: int) -> None:
        """
        Creates a sell order in the order book.
        :param _from: Token orgination address.
        :type _from: :class:`iconservice.base.address.Address`
        :param _amount: Number of tokens sent.
        :type _amount: int
        :param _price: Asking price.
        :type _price: int
        """
        pass

    @external
    @payable
    def offer_to_buy(self, _amount: int) -> None:
        """
        Creates a buy order in the order book.
        :param _amount: Number of tokens desired.
        :type _amount: int
        """
        pass

    @external
    @payable
    def buy(self, _amount: int, _tx_hash: str) -> None:
        """
        Fills a sell order in the order book.
        :param _amount: Number of tokens sent.
        :type _amount: int
        :param _tx_hash: order identifier.
        :type _tx_hash: str
        """
        pass

    def _remove_from_book(self, _book: str, _tx_hash: str) -> None:
        """
        Removes an entry from the specified order book.
        :param _book: One of the order books.
        :type _book: str
        :param _tx_hash: order identifier.
        :type _tx_hash: str
        """
        pass

    @external
    def stop_exchange(self) -> None:
        """
        Turns off the exchange and returns all orders.
        """
        pass

    @external
    def remove_order(self, _tx_hash: str) -> None:
        """
        Removes an order from the sell or buy order book.
        :param _tx_hash: order identifier.
        :type _tx_hash: str
        """
        pass

    def _return_ICX(self, _tx_hash: str) -> None:
        """
        Returns ICX held associated with the order identifier _tx_hash.
        :param _tx_hash: order identifier.
        :type _tx_hash: str
        """
        self._send_ICX(self._order_owner[_tx_hash],
                      self._order_book[_tx_hash]["price"],
                      "Order cancelled. ICX returned.")
        self._remove_from_book("buy", _tx_hash)
        self._removed.put(_tx_hash)
        self._order_book[_tx_hash]["removed_time"] = self.now()

    def _send_token(self, _to: Address, amount: int, msg: str) -> None:
        """
        Sends IRC2 token to an address.
        :param _to: Token destination address.
        :type _to: :class:`iconservice.base.address.Address`
        :param _amount: Number of tokens sent.
        :type _amount: int
        :param msg: Message for the event log.
        :type msg: str
        """
        try:
            token_score = self.create_interface_score(self._token_score.get(),
                                                      TokenInterface)
            token_score.transfer(_to, amount)
            symbol = token_score.symbol()
            self.TokenTransfer(_to, amount, msg + f' {amount} {symbol} sent to {_to}.')
        except BaseException as e:
            revert(f'{amount} {symbol} not sent to {_to}. '
                   f'Exception: {e}')

    def _send_ICX(self, _to: Address, amount: int, msg: str) -> None:
        """
        Sends ICX to an address.
        :param _to: ICX destination address.
        :type _to: :class:`iconservice.base.address.Address`
        :param _amount: Number of ICX sent.
        :type _amount: int
        :param msg: Message for the event log.
        :type msg: str
        """
        try:
            self.icx.transfer(_to, amount)
            self.FundTransfer(_to, amount, msg + f' {amount} ICX sent to {_to}.')
        except BaseException as e:
            revert(f'{amount} ICX not sent to {_to}. '
                   f'Exception: {e}')

    def fallback(self):
        pass
