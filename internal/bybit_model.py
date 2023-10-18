@tuple
class ServerTime:
    # {"timeSecond":"1696143222","timeNano":"1696143222859435119"}
    timeSecond: int
    timeNano: int
    
    def __new__(timeSecond: int, timeNano: int):
        return (timeSecond, timeNano)
    
    def __repr__(self) -> str:
        return f"<ServerTime: timeSecond={self.timeSecond}, timeNano={self.timeNano}>"


@tuple
class ExchangeInfo:
    symbol: str
    tick_size: float    # 价格 0.01
    step_size: float    # 数量 0.001
    
    def __new__(symbol: str, tick_size: float, step_size: float):
        return ExchangeInfo(symbol, tick_size, step_size)
    
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
    position_idx: int
    # riskId: int
    symbol: str
    side: str   # "None"
    size: str
    avg_price: str
    position_value: str
    # tradeMode: int    # 0
    # positionStatus: str # Normal
    # autoAddMargin: int    # 0
    # adlRankIndicator: int # 0
    leverage: float         # 1
    # positionBalance: str    # 0
    mark_price: str          # 26515.73
    # liq_price: str           # ""
    # bust_price: str          # "0.00"
    position_mm: str         # "0"
    position_im: str         # "0"
    # tpslMode: str           # "Full"
    take_profit: str         # "0.00"
    stop_loss: str           # "0.00"
    # trailingStop: str       # "0.00"
    unrealised_pnl: str      # "0"
    cum_realised_pnl: str     # "-19.59637027"
    # seq: int                # 8172241025
    created_time: str        # "1682125794703"
    updated_time: str        # "updatedTime"
    
    def __new__():
        return PositionInfo()
    
    # def __new__(_position_idx: int, _symbol: str, _side: str, _size: str, 
    #             _avg_price: str, _position_value: str, _leverage: float, _mark_price: str, \
    #             _position_mm: str, _position_im: str, _take_profit: str, \
    #             _stop_loss: str, _unrealised_pnl: str, _created_time: str, \
    #             _updated_time: str) -> PositionInfo:
    #     return PositionInfo(position_idx=_position_idx, symbol=_symbol, side=_side, \
    #         size=_size, avg_price=_avg_price, leverage=_leverage, 
    #         mark_price=_mark_price, position_mm=_position_mm, \
    #         position_im=_position_im, take_profit=_take_profit, stop_loss=_stop_loss, \
    #         unrealised_pnl=_unrealised_pnl, created_time=_created_time, \
    #         updated_time=_updated_time)
        
    def __repr__(self) -> str:
        return f"<PositionInfo: symbol={self.symbol}, position_idx={self.position_idx}, side={self.side}, size={self.size}, avg_price={self.avg_price}, position_value={self.position_value}, leverage={self.leverage}, mark_price={self.mark_price}, position_mm={self.position_mm}, position_im={self.position_im}, take_profit={self.take_profit}, stop_loss={self.stop_loss}, unrealised_pnl={self.unrealised_pnl}, cum_realised_pnl={self.cum_realised_pnl}, created_time={self.created_time}, updated_time={self.updated_time}>"  # noqa: E501


@tuple
class OrderResponse:
    order_id: str
    order_link_id: str
    
    def __new__():
        return OrderResponse()
    
    def __repr__(self) -> str:
        return f"<OrderResponse: order_id={self.order_id}, order_link_id={self.order_link_id}>"  # noqa: E501


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
    
    
@tuple
class OrderInfo:
    # position_idx:
    # 0 - 单向持仓
    # 1 - 买侧双向持仓
    # 2 - 卖侧双向持仓
    position_idx: int   # positionIdx
    order_id: str       # orderId
    symbol: str         # BTCUSDT
    side: str           # Buy/Sell
    type: str           # orderType Limit/Market
    price: float
    qty: float
    cum_exec_qty: float # cumExecQty
    status: str         # orderStatus
    created_time: str   # createdTime
    updated_time: str   # updatedTime
    avg_price: float    # avgPrice
    cum_exec_fee: float # cumExecFee
    # time_in_force:
    # GTC - Good Till Cancel 成交为止, 一直有效直到被取消
    # IOC - Immediate or Cancel 无法立即成交(吃单)的部分就撤销
    # FOK - Fill or Kill 无法全部立即成交就撤销
    # PostOnly - 只做Maker单, 如果会成为Taker单则取消
    time_in_force: str  # timeInForce
    reduce_only: bool   # reduceOnly
    order_link_id: str  # orderLinkId
    
    def __new__():
        return OrderInfo()
    
    def __repr__(self) -> str:
        return f"<OrderInfo: position_idx={self.position_idx}, order_id={self.order_id}, symbol={self.symbol}, side={self.side}, type={self.type}, price={self.price}, qty={self.qty}, cum_exec_qty={self.cum_exec_qty}, status={self.status}, created_time={self.created_time}, updated_time={self.updated_time}, avg_price={self.avg_price}, cum_exec_fee={self.cum_exec_fee}, time_in_force={self.time_in_force}, reduce_only={self.reduce_only}, order_link_id={self.order_link_id}>"  # noqa: E501

