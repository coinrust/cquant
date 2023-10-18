@tuple
class ExchangeInfo:
    symbol: str
    tick_size: float    # 价格 0.01
    step_size: float    # 数量 0.001
    
    def __new__(symbol: str, tick_size: float, step_size: float):
        return (symbol, tick_size, step_size)
    
    def __repr__(self) -> str:
        return f"<ExchangeInfo: symbol={self.symbol}, tick_size={self.tick_size}, step_size={self.step_size}>"  # noqa: E501


@tuple
class KlineItem:
    """
    K线的一条记录
    """
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    turnover: float
    confirm: bool
    
    def __new__(_timestamp: int, _open: float, _high: float, _low: float, \
        _close: float, _volume: float, _turnover: float, _confirm: bool):
        return KlineItem(timestamp=_timestamp, open=_open, high=_high, low=_low, \
            close=_close, volume=_volume, turnover=_turnover, confirm=_confirm)
    
    def __repr__(self) -> str:
        return f"<KlineItem: timestamp={self.timestamp}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume}, turnover={self.turnover}, confirm={self.confirm}>"  # noqa: E501


@tuple
class OrderBookItem:
    """
    订单薄的一条记录
    """
    price: float
    qty: float
    
    def __new__(_price: float, _qty: float):
        return OrderBookItem(price=_price, qty=_qty)
    
    def __repr__(self) -> str:
        return f"<OrderBookItem: price={self.price}, qty={self.qty}>"


@tuple
class OrderBook:
    """
    订单薄
    """
    asks: list[OrderBookItem]
    bids: list[OrderBookItem]
    
    def __new__(_asks: list[OrderBookItem], _bids: list[OrderBookItem]):
        return OrderBook(asks=_asks, bids=_bids)
    
    def __repr__(self) -> str:
        return f"<OrderBook: asks={self.asks}, bids={self.bids}>"


@tuple
class PositionInfo:
    # {
    #     "entryPrice": "0.00000",  // 开仓均价
    #     "breakEvenPrice": "0.0",  // 盈亏平衡价
    #     "marginType": "isolated", // 逐仓模式或全仓模式
    #     "isAutoAddMargin": "false",
    #     "isolatedMargin": "0.00000000", // 逐仓保证金
    #     "leverage": "10", // 当前杠杆倍数
    #     "liquidationPrice": "0", // 参考强平价格
    #     "markPrice": "6679.50671178",   // 当前标记价格
    #     "maxNotionalValue": "20000000", // 当前杠杆倍数允许的名义价值上限
    #     "positionAmt": "0.000", // 头寸数量，符号代表多空方向, 正数为多，负数为空
    #     "notional": "0",
    #     "isolatedWallet": "0",
    #     "symbol": "BTCUSDT", // 交易对
    #     "unRealizedProfit": "0.00000000", // 持仓未实现盈亏
    #     "positionSide": "BOTH", // 持仓方向
    #     "updateTime": 1625474304765   // 更新时间
    # }
    entry_price: str            # entryPrice
    break_even_price: str       # breakEvenPrice
    margin_type: str            # marginType
    is_auto_add_margin: bool    # isAutoAddMargin
    isolated_margin: str        # isolatedMargin
    leverage: str               # leverage
    liquidation_price: str      # liquidationPrice
    mark_rice: str              # markPrice
    max_notional_value: str     # maxNotionalValue
    position_amt: str           # positionAmt
    notional: str               # notional
    isolated_wallet: str        # isolatedWallet    0
    symbol: str                 # symbol
    un_realized_profit: str     # unRealizedProfit
    position_side: str          # positionSide  LONG/SHORT
    update_time: int            # updateTime
    
    def __new__():
        return PositionInfo()
        
    def __repr__(self) -> str:
        return f"<PositionInfo: entry_price={self.entry_price}, break_even_price={self.break_even_price}, margin_type={self.margin_type}, is_auto_add_margin={self.is_auto_add_margin}, isolated_margin={self.isolated_margin}, leverage={self.leverage}, liquidation_price={self.liquidation_price}, mark_rice={self.mark_rice}, max_notional_value={self.max_notional_value}, position_amt={self.position_amt}, notional={self.notional}, isolated_wallet={self.isolated_wallet}, symbol={self.symbol}, un_realized_profit={self.un_realized_profit}, position_side={self.position_side}, update_time={self.update_time}>"  # noqa: E501


@tuple
class OrderInfo:
    # {
    #     "orderId": 198567142495,
    #     "symbol": "BTCUSDT",
    #     "status": "NEW",
    #     "clientOrderId": "qGexY0GHGZPXW5I8sTsxcw",
    #     "price": "20000.00",
    #     "avgPrice": "0.00",
    #     "origQty": "0.001",
    #     "executedQty": "0.000",
    #     "cumQty": "0.000",
    #     "cumQuote": "0.00000",
    #     "timeInForce": "GTC",
    #     "type": "LIMIT",
    #     "reduceOnly": false,
    #     "closePosition": false,
    #     "side": "BUY",
    #     "positionSide": "LONG",
    #     "stopPrice": "0.00",
    #     "workingType": "CONTRACT_PRICE",
    #     "priceProtect": false,
    #     "origType": "LIMIT",
    #     "priceMatch": "NONE",
    #     "selfTradePreventionMode": "NONE",
    #     "goodTillDate": 0,
    #     "updateTime": 1697297963066
    # }
    order_id: int           # orderId
    client_order_id: str    # clientOrderId
    symbol: str             # symbol
    status: str             # status
    price: str              # price
    avg_price: str          # avgPrice
    orig_qty: str           # origQty
    executed_qty: str       # executedQty
    cum_qty: str            # cumQty
    cum_quote: str          # cumQuote
    time_in_force: str      # timeInForce
    type: str               # type
    reduce_only: bool       # reduceOnly
    close_position: bool    # closePosition
    side: str               # side
    position_side: str      # positionSide
    stop_price: str         # stopPrice
    working_type: str       # workingType
    price_protect: bool     # priceProtect
    orig_type: str          # origType
    price_match: str        # priceMatch
    self_trade_prevention_mode: str # selfTradePreventionMode
    good_till_date: int     # goodTillDate
    update_time: int        # updateTime
    
    def __new__():
        return OrderInfo()
    
    def __repr__(self) -> str:
        return f"<OrderInfo: order_id={self.order_id}, client_order_id={self.client_order_id}, symbol={self.symbol}, status={self.status}, price={self.price}, avg_price={self.avg_price}, orig_qty={self.orig_qty}, executed_qty={self.executed_qty}, cum_qty={self.cum_qty}, cum_quote={self.cum_quote}, time_in_force={self.time_in_force}, type={self.type}, reduce_only={self.reduce_only}, close_position={self.close_position}, side={self.side}, position_side={self.position_side}, update_time={self.update_time}>"  # noqa: E501


@tuple
class BalanceInfo:
    coin_name: str
    equity: float
    available_to_withdraw: float
    wallet_balance: float
    total_order_im: float
    total_position_im: float
    
    def __new__():
        return BalanceInfo()
    
    def __repr__(self) -> str:
        return f"<BalanceInfo: coin_name={self.coin_name} equity={self.equity}, available_to_withdraw={self.available_to_withdraw}, wallet_balance={self.wallet_balance}, total_order_im={self.total_order_im}, total_position_im={self.total_position_im}>"  # noqa: E501

