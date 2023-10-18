from typing import Dict
from ct import LIBRARY, ct_init
from yyjson import yyjson_doc, yyjson_mut_doc, yyjson_val
from binance_model import ExchangeInfo, KlineItem, OrderBookItem, OrderBook, \
    PositionInfo, BalanceInfo, OrderInfo
from http import HttpResponse, VERB_PUT, VERB_DELETE, create_query

# SEQ_FUNC CtBinanceAPI *seq_binance_client_new(const char *baseUrl,
#                                           const char *accessKey,
#                                           const char *secretKey);
from C import LIBRARY.seq_binance_client_new(cobj, cobj, cobj) -> cobj
# SEQ_FUNC void seq_binance_client_free(CtBinanceAPI *p);
from C import LIBRARY.seq_binance_client_free(cobj) -> None
# SEQ_FUNC seq_int_t seq_binance_client_do_request(CtBinanceAPI *p,
#                                                  const char *path,
#                                                  int verb,
#                                                  const char *paramStr,
#                                                  bool sign,
#                                                  CtHttpResponse *res)
from C import LIBRARY.seq_binance_client_do_request(cobj, cobj, int, cobj, bool, Ptr[HttpResponse]) -> int
# SEQ_FUNC seq_int_t seq_binance_client_do_get(CtBinanceAPI *p, const char *path,
#                                            const char *paramStr, bool sign,
#                                            CtHttpResponse *res);
from C import LIBRARY.seq_binance_client_do_get(cobj, cobj, cobj, bool, Ptr[HttpResponse]) -> int
# SEQ_FUNC seq_int_t seq_binance_client_do_post(CtBinanceAPI *p, const char *path,
#                                             const char *paramStr, bool sign,
#                                             CtHttpResponse *res);
from C import LIBRARY.seq_binance_client_do_post(cobj, cobj, cobj, bool, Ptr[HttpResponse]) -> int





# {"code":-1021,"msg":"Timestamp for this request was 1000ms ahead of the server's time."}


@tuple
class BinanceClient:
    p: cobj
    
    def __new__(base_url: str, access_key: str, secret_key: str):
        return BinanceClient(p=seq_binance_client_new(base_url.ptr, access_key.ptr,
                                                  secret_key.ptr))
        
    def __new__(testnet: bool, access_key: str, secret_key: str):
        base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        return BinanceClient(p=seq_binance_client_new(base_url.ptr, access_key.ptr,
                                                  secret_key.ptr))
        
    def fetch_public_time(self) -> int:
        ret = self.do_get("/fapi/v1/time", "", False)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        
        # {"serverTime":1697149330948}
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            server_ime = root["serverTime"].uint()
            # print('server_ime: ', server_ime)
        
        return server_ime
    
    def fetch_exchange_info(self, symbol: str) -> ExchangeInfo:
        ret = self.do_get("/fapi/v1/exchangeInfo", "", False)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        
        # {
        #     "symbols": [{
        #             "symbol": "BTCUSDT",
        #             "pair": "BTCUSDT",
        #             "contractType": "PERPETUAL",
        #             "deliveryDate": 4133404802000,
        #             "onboardDate": 1569398400000,
        #             "status": "TRADING",
        #             "maintMarginPercent": "2.5000",
        #             "requiredMarginPercent": "5.0000",
        #             "baseAsset": "BTC",
        #             "quoteAsset": "USDT",
        #             "marginAsset": "USDT",
        #             "pricePrecision": 2,
        #             "quantityPrecision": 3,
        #             "baseAssetPrecision": 8,
        #             "quotePrecision": 8,
        #             "underlyingType": "COIN",
        #             "underlyingSubType": [],
        #             "settlePlan": 0,
        #             "triggerProtect": "0.0500",
        #             "liquidationFee": "0.020000",
        #             "marketTakeBound": "0.30",
        #             "maxMoveOrderLimit": 1000,
        #             "filters": [{
        #                     "filterType": "PRICE_FILTER",
        #                     "maxPrice": "809484",
        #                     "minPrice": "261.10",
        #                     "tickSize": "0.10"
        #                 }, {
        #                     "filterType": "LOT_SIZE",
        #                     "maxQty": "1000",
        #                     "stepSize": "0.001",
        #                     "minQty": "0.001"
        #                 }, {
        #                     "filterType": "MARKET_LOT_SIZE",
        #                     "maxQty": "1000",
        #                     "stepSize": "0.001",
        #                     "minQty": "0.001"
        #                 }, {
        #                     "filterType": "MAX_NUM_ORDERS",
        #                     "limit": 200
        #                 }, {
        #                     "limit": 10,
        #                     "filterType": "MAX_NUM_ALGO_ORDERS"
        #                 }, {
        #                     "notional": "5",
        #                     "filterType": "MIN_NOTIONAL"
        #                 }, {
        #                     "multiplierUp": "1.5000",
        #                     "multiplierDecimal": "4",
        #                     "multiplierDown": "0.5000",
        #                     "filterType": "PERCENT_PRICE"
        #                 }
        #             ],
        #             "orderTypes": [
        #                 "LIMIT",
        #                 "MARKET",
        #                 "STOP",
        #                 "STOP_MARKET",
        #                 "TAKE_PROFIT",
        #                 "TAKE_PROFIT_MARKET",
        #                 "TRAILING_STOP_MARKET"
        #             ],
        #             "timeInForce": [
        #                 "GTC",
        #                 "IOC",
        #                 "FOK",
        #                 "GTX",
        #                 "GTD"
        #             ]
        #         }
        #     ]
        # }
        
        tick_size: float = 0
        stepSize: float = 0

        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            # ret_code = root["retCode"].int()
            # ret_msg = root["retMsg"].str()
            # if ret_code != 0:
            #     raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result_list = root["symbols"]
            arr_list = result_list.array_list()
            if len(arr_list) == 0:
                raise ValueError(f"error list length is 0")
            
            for i in arr_list:
                symbol_ = i["symbol"].str()
                if symbol.upper() != symbol_.upper():
                    continue
                filters_list = i["filters"].array_list()
                for j in filters_list:
                    filter_type = j["filterType"].str()
                    if filter_type == "PRICE_FILTER":
                        tick_size = float(j["tickSize"].str())
                    elif filter_type == "LOT_SIZE":
                        stepSize = float(j["stepSize"].str())
                # print('tick_size: ', tick_size)
                # print('stepSize: ', stepSize)
        
        return ExchangeInfo(symbol, tick_size, stepSize)
    
    def fetch_kline(self, symbol: str, interval: str, limit: int, \
        start: int, end: int) -> List[KlineItem]:
        """
        interval: 1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M
        """
        # symbol	STRING	YES	交易对
        # interval	ENUM	YES	时间间隔
        # startTime	LONG	NO	起始时间
        # endTime	LONG	NO	结束时间
        # limit	INT	NO	默认值:500 最大值:1500.
        
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        query_values["interval"] = interval
        if limit > 0:
            query_values["limit"] = str(limit)
        if start > 0:
            query_values["startTime"] = str(start)
        if end > 0:
            query_values["endTime"] = str(end)
        query_str = create_query(query_values)
        ret = self.do_get("/fapi/v1/klines", query_str, False)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        # [[1697151060000,"26826.60","26966.90","26738.40","26745.20","115.065",1697151119999,"3091232.87810",116,"80.740","2172848.23510","0"],[1697151120000,"26771.40","26966","26743.80","26966","165.071",1697151179999,"4437084.94670",70,"114.784","3091896.30480","0"],[1697151180000,"26919.30","26966","26750","26750","156.262",1697151239999,"4189805.69830",117,"45.466","1225563.38740","0"],[1697151240000,"26828.20","26965.90","26750","26750","239.620",1697151299999,"6432750.50860",95,"115.763","3119352.95670","0"],[1697151300000,"26794.90","26794.90","26751","26751","4.972",1697151359999,"133028.81490",6,"0.002","53.58980","0"]]
        
        res = List[KlineItem]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            
            arr_list = root.array_list()
            
            # [
                # [
                #     1499040000000,      // 开盘时间
                #     "0.01634790",       // 开盘价
                #     "0.80000000",       // 最高价
                #     "0.01575800",       // 最低价
                #     "0.01577100",       // 收盘价(当前K线未结束的即为最新价)
                #     "148976.11427815",  // 成交量
                #     1499644799999,      // 收盘时间
                #     "2434.19055334",    // 成交额
                #     308,                // 成交笔数
                #     "1756.87402397",    // 主动买入成交量
                #     "28.46694368",      // 主动买入成交额
                #     "17928899.62484339" // 请忽略该参数
                # ]
            # ]
            
            for i in arr_list:
                i_arr_list = i.array_list()
                if len(i_arr_list) != 12:
                    print(f'错误: i_arr_list != 12')
                    continue
                
                _timestamp = int(i_arr_list[0].uint())
                _open = float(i_arr_list[1].str())
                _high = float(i_arr_list[2].str())
                _low = float(i_arr_list[3].str())
                _close = float(i_arr_list[4].str())
                _volume = float(i_arr_list[5].str())
                # _timestampC = int(i_arr_list[6].uint())
                _turnover = float(i_arr_list[7].str())
                
                res.append(KlineItem(timestamp=_timestamp, open=_open, high=_high, \
                    low=_low, close=_close, volume=_volume, turnover=_turnover, \
                    confirm=True))
                
        return res
    
    def fetch_orderbook(self, symbol: str, limit: int) -> OrderBook:
        """
        symbol	STRING	YES	交易对
        limit	INT	NO	默认 500; 可选值:[5, 10, 20, 50, 100, 500, 1000]
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        if limit > 0:
            query_values["limit"] = str(limit)
        query_str = create_query(query_values)
        ret = self.do_get("/fapi/v1/depth", query_str, False)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        print(ret.body)
        # {
        #     "lastUpdateId": 34058189024,
        #     "E": 1697151922019,
        #     "T": 1697151922013,
        #     "bids": [
        #         [
        #             "26782.30",
        #             "0.010"
        #         ],
        #         [
        #             "26752.00",
        #             "942.141"
        #         ],
        #         [
        #             "26750.00",
        #             "0.005"
        #         ],
        #         [
        #             "26748.40",
        #             "29.120"
        #         ],
        #         [
        #             "26744.00",
        #             "4.092"
        #         ]
        #     ],
        #     "asks": [
        #         [
        #             "26804.60",
        #             "0.054"
        #         ],
        #         [
        #             "26805.90",
        #             "0.905"
        #         ],
        #         [
        #             "26810.60",
        #             "0.009"
        #         ],
        #         [
        #             "26839.40",
        #             "0.001"
        #         ],
        #         [
        #             "26844.90",
        #             "0.002"
        #         ]
        #     ]
        # }
        
        asks = List[OrderBookItem]()
        bids = List[OrderBookItem]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            
            b = root["bids"]
            b_list = b.array_list()
            for i in b_list:
                i_arr = i.array_list()
                price = float(i_arr[0].str())
                qty = float(i_arr[1].str())
                bids.append(OrderBookItem(price, qty))
            
            a = root["asks"]
            a_list = a.array_list()
            for i in a_list:
                i_arr = i.array_list()
                price = float(i_arr[0].str())
                qty = float(i_arr[1].str())
                asks.append(OrderBookItem(price, qty))
                
        return OrderBook(asks, bids)
    
    def fetch_position_mode(self, symbol: str) -> int:
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        query_str = create_query(query_values)
        
        print(query_str)
        # {"code":-2014,"msg":"API-key format invalid."}
        # {"code":-2015,"msg":"Invalid API-key, IP, or permissions for action"}
        
        ret = self.do_get("/fapi/v1/positionSide/dual", query_str, True)

        print(ret.body)

        # print(ret)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        return 0

    
    def switch_position_mode(self, symbol: str, dual_side_position: bool) -> bool:
        """
        切换持仓模式
        mode dualSidePosition	STRING	YES	"true": 双向持仓模式；"false": 单向持仓模式
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        query_values["dualSidePosition"] = "true" if dual_side_position else "false"
        query_str = create_query(query_values)
        
        # print(query_str)
        # 
        
        ret = self.do_post("/fapi/v1/positionSide/dual", query_str, True)
        
        # print(ret.body)
        # {"code":-4059,"msg":"No need to change position side."}
        # {"code": 200,"msg": "success"}
        
        # print(ret)
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")

        # 
        # print(ret.body)
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            code = root["code"].int()
            msg = root["msg"].str()
            if code != 200:
                raise ValueError(f"error code={code}, msg={msg}")
        
        return True
    
    def set_leverage(self, symbol: str, leverage: int) -> bool:
        """
        设置杠杆倍数
        leverage: 目标杠杆倍数：1 到 125 整数
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        query_values["leverage"] = str(leverage)
        query_str = create_query(query_values)
        
        # print(query_str)
        # {"symbol":"BTCUSDT","leverage":20,"maxNotionalValue":"20000000"}
        
        ret = self.do_post("/fapi/v1/leverage", query_str, True)
        # print(ret)
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")

        # print(ret.body)
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            leverage_ = root["leverage"].int()
            maxNotionalValue = int(root["maxNotionalValue"].str())
            if leverage_ != leverage:
                raise ValueError(f"error leverage={leverage_}, maxNotionalValue={maxNotionalValue}")
        
        return True
    
    @inline
    def _parse_order(self, val: yyjson_val) -> OrderInfo:
        order_id = val["orderId"].uint()
        client_order_id = val["clientOrderId"].str()
        symbol = val["symbol"].str()
        status = val["status"].str()
        price = val["price"].str()
        avg_price = val["avgPrice"].str()
        orig_qty = val["origQty"].str()
        executed_qty = val["executedQty"].str()
        cum_qty = val["cumQty"].safe_str()
        cum_quote = val["cumQuote"].str()
        time_in_force = val["timeInForce"].str()
        type = val["type"].str()
        reduce_only = val["reduceOnly"].bool()
        close_position = val["closePosition"].bool()
        side = val["side"].str()
        position_side = val["positionSide"].str()
        stop_price = val["stopPrice"].str()
        working_type = val["workingType"].str()
        price_protect = val["priceProtect"].bool()
        orig_type = val["origType"].str()
        price_match = val["priceMatch"].str()
        self_trade_prevention_mode = val["selfTradePreventionMode"].str()
        good_till_date = val["goodTillDate"].uint()
        update_time = val["updateTime"].uint()
        
        return OrderInfo(order_id=order_id, client_order_id=client_order_id, \
            symbol=symbol, status=status, price=price, avg_price=avg_price, \
            orig_qty=orig_qty, executed_qty=executed_qty, cum_qty=cum_qty, \
            cum_quote=cum_quote, time_in_force=time_in_force, type=type, \
            reduce_only=reduce_only, close_position=close_position, side=side, \
            position_side=position_side, stop_price=stop_price, \
            working_type=working_type, price_protect=price_protect, \
            orig_type=orig_type, price_match=price_match, \
            self_trade_prevention_mode=self_trade_prevention_mode, \
            good_till_date=good_till_date, update_time=update_time)
    
    def place_order(self, symbol: str, side: str, position_side: str, order_type: str, \
        qty: str, price: str, time_in_force: str="GTC", \
        client_order_id: str="", reduce_only: bool=False) -> OrderInfo:
        """
        下单
        symbol	STRING	YES	交易对
        side	ENUM	YES	买卖方向 SELL, BUY
        positionSide	ENUM	NO	持仓方向，单向持仓模式下非必填，默认且仅可填BOTH;在双向持仓模式下必填,且仅可选择 LONG 或 SHORT
        type	ENUM	YES	订单类型 LIMIT, MARKET, STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET
        reduceOnly	STRING	NO	true, false; 非双开模式下默认false；双开模式下不接受此参数； 使用closePosition不支持此参数。
        quantity	DECIMAL	NO	下单数量,使用closePosition不支持此参数。
        price	DECIMAL	NO	委托价格
        newClientOrderId	STRING	NO	用户自定义的订单号，不可以重复出现在挂单中。如空缺系统会自动赋值。必须满足正则规则 ^[\.A-Z\:/a-z0-9_-]{1,36}$
        stopPrice	DECIMAL	NO	触发价, 仅 STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET 需要此参数
        closePosition	STRING	NO	true, false；触发后全部平仓，仅支持STOP_MARKET和TAKE_PROFIT_MARKET；不与quantity合用；自带只平仓效果，不与reduceOnly 合用
        activationPrice	DECIMAL	NO	追踪止损激活价格，仅TRAILING_STOP_MARKET 需要此参数, 默认为下单当前市场价格(支持不同workingType)
        callbackRate	DECIMAL	NO	追踪止损回调比例，可取值范围[0.1, 5],其中 1代表1% ,仅TRAILING_STOP_MARKET 需要此参数
        timeInForce	ENUM	NO	有效方法
        workingType	ENUM	NO	stopPrice 触发类型: MARK_PRICE(标记价格), CONTRACT_PRICE(合约最新价). 默认 CONTRACT_PRICE
        priceProtect	STRING	NO	条件单触发保护："TRUE","FALSE", 默认"FALSE". 仅 STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET 需要此参数
        newOrderRespType	ENUM	NO	"ACK", "RESULT", 默认 "ACK"
        symbol	STRING	YES	交易对
        priceMatch	ENUM	NO	OPPONENT/ OPPONENT_5/ OPPONENT_10/ OPPONENT_20/QUEUE/ QUEUE_5/ QUEUE_10/ QUEUE_20；不能与price同时传
        selfTradePreventionMode	ENUM	NO	NONE / EXPIRE_TAKER/ EXPIRE_MAKER/ EXPIRE_BOTH； 默认NONE
        goodTillDate	LONG	NO	TIF为GTD时订单的自动取消时间， 当timeInforce为GTD时必传；传入的时间戳仅保留秒级精度，毫秒级部分会被自动忽略，时间戳需大于当前时间+600s且小于253402300799000
        recvWindow	LONG	NO	
        timestamp	LONG	YES	
        
        根据 order type的不同，某些参数强制要求，具体如下:

        Type	强制要求的参数
        LIMIT	timeInForce, quantity, price
        MARKET	quantity
        STOP, TAKE_PROFIT	quantity, price, stopPrice
        STOP_MARKET, TAKE_PROFIT_MARKET	stopPrice
        TRAILING_STOP_MARKET	callbackRate
        
        timeInForce: GTC,IOC,FOK,GTX
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        query_values["side"] = side
        query_values["positionSide"] = position_side
        query_values["type"] = order_type
        if qty != "":
            query_values["quantity"] = qty
        if price != "":
            query_values["price"] = price
        if client_order_id != "":
            query_values["newClientOrderId"] = client_order_id
        if reduce_only:
            query_values["reduceOnly"] = "true"
        if time_in_force != "":
            query_values["timeInForce"] = time_in_force
        
        query_str = create_query(query_values)
        
        ret = self.do_post("/fapi/v1/order", query_str, True)
        
        # print(ret)
        # {"code":-1102,"msg":"Mandatory parameter 'timeinforce' was not sent, was empty/null, or malformed."}
        # {"code":-1111,"msg":"Precision is over the maximum defined for this asset."}
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
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
        
        print(ret.body)
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            return self._parse_order(root)
    
    def cancel_order(self, symbol: str, order_id: int=0, \
        client_order_id: str="") -> OrderInfo:
        """
        撤单
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        if order_id != 0:
            query_values["orderId"] = str(order_id)
        if client_order_id != "":
            query_values["origClientOrderId"] = client_order_id
        
        query_str = create_query(query_values)
        
        ret = self.do_request("/fapi/v1/order", VERB_DELETE, query_str, True)
        
        # print(ret)
        # 
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
        # print(ret.body)
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            return self._parse_order(root)
    
    def cancel_orders(self, symbol: str) -> bool:   # List[OrderInfo]:
        """
        批量撤单
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        
        query_str = create_query(query_values)
        
        ret = self.do_request("/fapi/v1/allOpenOrders", VERB_DELETE, query_str, True)
        
        print(ret)
        # 
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
        # print(ret.body)
        # {"code":200,"msg":"The operation of cancel all open order is done."}
        
        # res = List[OrderInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            # arr_list = root.array_list()
            # for i in arr_list:
            #     res.append(self._parse_order(i))
            code = root["code"].int()
            msg = root["msg"].str()
            if code != 200:
                raise ValueError(f"error code={code}, msg={msg}")
        
        return True
    
    def fetch_balance(self) -> List[BalanceInfo]:
        """
        获取钱包余额
        """
        # query_values: Dict[str, str] = {}
        # query_values["accountType"] = account_type
        # query_values["coin"] = coin
        query_str = "" # create_query(query_values)
        ret = self.do_get("/fapi/v2/balance", query_str, True)
        
        # print(ret.body)
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
        # print(ret.body)
        
        # 
        res = List[BalanceInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            # [
            # {
            #     "accountAlias": "FzuXTiSgSgXqXq",
            #     "asset": "USDT",
            #     "balance": "92.89164902",
            #     "crossWalletBalance": "92.89164902",
            #     "crossUnPnl": "0.00000000",
            #     "availableBalance": "92.89164902",
            #     "maxWithdrawAmount": "92.89164902",
            #     "marginAvailable": true,
            #     "updateTime": 1694556226482
            # }
            # ]
            
            result_list = root.array_list()
            
            for i in result_list:
                # account_lias = i["accountAlias"].str()
                asset = i["asset"].str()
                balance = float(i["balance"].str())
                available_balance = float(i["availableBalance"].str())
                res.append(BalanceInfo(coin_name=asset, equity=balance, \
                            available_to_withdraw=available_balance, \
                            wallet_balance=balance, \
                            total_order_im=0, \
                            total_position_im=0))
            
        return res
    
    
    def fetch_orders(self, symbol: str, order_id: int=0, \
        client_order_id: str="") -> List[OrderInfo]:
        """
        获取当前订单
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        if order_id != 0:
            query_values["orderId"] = str(order_id)
        if client_order_id != "":
            query_values["origClientOrderId"] = client_order_id
        
        query_str = create_query(query_values)
        
        ret = self.do_get("/fapi/v1/openOrders", query_str, True)
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
        # print(ret.body)
        
        # 
        res = List[OrderInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            result_list = root.array_list()
            
            for i in result_list:
                res.append(self._parse_order(i))
            
        return res
    
    def fetch_order(self, symbol: str, order_id: int=0, \
        client_order_id: str="") -> OrderInfo:
        """
        获取当前订单
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        if order_id != 0:
            query_values["orderId"] = str(order_id)
        if client_order_id != "":
            query_values["origClientOrderId"] = client_order_id
        
        query_str = create_query(query_values)
        
        ret = self.do_get("/fapi/v1/order", query_str, True)
        
        # {"code":-2013,"msg":"Order does not exist."}
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
        print(ret.body)
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            return self._parse_order(root)
    
    def fetch_all_orders(self, symbol: str, order_id: int=0, \
        start_time: int=0, end_time: int=0, limit: int=0) -> List[OrderInfo]:
        """
        获取所有订单
        https://binance-docs.github.io/apidocs/futures/cn/#user_data-7
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        if order_id != 0:
            query_values["orderId"] = str(order_id)
        if start_time != 0:
            query_values["startTime"] = str(start_time)
        if end_time != 0:
            query_values["endTime"] = str(end_time)
        if limit != 0:
            query_values["limit"] = str(limit)
        
        query_str = create_query(query_values)
        
        ret = self.do_get("/fapi/v1/allOrders", query_str, True)
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
        # print(ret.body)
        
        # 
        res = List[OrderInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            result_list = root.array_list()
            
            for i in result_list:
                res.append(self._parse_order(i))
            
        return res
    
    def fetch_commission_rate(self, symbol: str) -> dict:
        """
        获取用户手续费率
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        
        query_str = create_query(query_values)
        
        ret = self.do_get("/fapi/v1/commissionRate", query_str, True)
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
        # print(ret.body)
        # {"symbol":"BTCUSDT","makerCommissionRate":"0.000200","takerCommissionRate":"0.000500"}
        
        # {
        #     "symbol": "BTCUSDT",
        #     "makerCommissionRate": "0.0002",  // 0.02%
        #     "takerCommissionRate": "0.0004"   // 0.04%
        # }
        res = dict()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            res["maker_commission_rate"] = root["makerCommissionRate"].str()
            res["taker_commission_rate"] = root["takerCommissionRate"].str()
            
        return res
    
    def fetch_positions(self, symbol: str) -> List[PositionInfo]:
        """
        获取持仓信息
        """
        query_values: Dict[str, str] = {}
        query_values["symbol"] = symbol
        
        query_str = create_query(query_values)
        
        ret = self.do_get("/fapi/v2/positionRisk", query_str, True)
        
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")
        
        print(ret.body)
        
        # 
        res = List[PositionInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            result_list = root.array_list()
            
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
            
            # {
            #     "symbol": "BTCUSDT",
            #     "positionAmt": "0.001",
            #     "entryPrice": "27010.7",
            #     "breakEvenPrice": "27021.50428",
            #     "markPrice": "26927.15357194",
            #     "unRealizedProfit": "-0.08354642",
            #     "liquidationPrice": "0",
            #     "leverage": "25",
            #     "maxNotionalValue": "3000000",
            #     "marginType": "cross",
            #     "isolatedMargin": "0.00000000",
            #     "isAutoAddMargin": "false",
            #     "positionSide": "LONG",
            #     "notional": "26.92715357",
            #     "isolatedWallet": "0",
            #     "updateTime": 1697338060675,
            #     "isolated": false,
            #     "adlQuantile": 1
            # },
            
            for i in result_list:
                entry_price = i["entryPrice"].str()
                break_even_price = i["breakEvenPrice"].str()
                margin_type = i["marginType"].str()
                is_auto_add_margin = i["isAutoAddMargin"].bool()
                isolated_margin = i["isolatedMargin"].str()
                leverage = i["leverage"].str()
                liquidation_price = i["liquidationPrice"].str()
                mark_rice = i["markPrice"].str()
                max_notional_value = i["maxNotionalValue"].str()
                position_amt = i["positionAmt"].str()
                notional = i["notional"].str()
                isolated_wallet = i["isolatedWallet"].str()
                symbol = i["symbol"].str()
                un_realized_profit = i["unRealizedProfit"].str()
                position_side = i["positionSide"].str() # LONG/SHORT
                update_time = i["updateTime"].uint()
                
                pos = PositionInfo(entry_price = entry_price, \
                    break_even_price = entry_price, margin_type = margin_type, \
                    is_auto_add_margin = is_auto_add_margin, \
                    isolated_margin = isolated_margin, leverage = leverage, \
                    liquidation_price = liquidation_price, mark_rice = mark_rice, \
                    max_notional_value = max_notional_value, \
                    position_amt = position_amt, notional = notional, \
                    isolated_wallet = isolated_wallet, symbol = symbol, \
                    un_realized_profit = un_realized_profit, \
                    position_side = position_side, update_time = update_time)
                res.append(pos)
            
        return res
    
    def listen_key(self) -> str:
        """
        生成listenKey (USER_STREAM)
        """
        ret = self.do_post("/fapi/v1/listenKey", "", True)
        print(ret)
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")

        # print(ret.body)
        # {"listenKey":"wQAdq89AmFLl0gC9vKSy2fKr8i4WMpCcBCrXklLuyrMD7pOEVUuPYAJVf30DhxGa"}
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            listen_key = root["listenKey"].str()
            return listen_key
        
    def put_listen_key(self) -> bool:
        """
        延长listenKey有效期 (USER_STREAM)
        """
        ret = self.do_request("/fapi/v1/listenKey", VERB_PUT, "", True)
        print(ret)
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}] data={ret.body}")

        print(ret.body)
        # {}
        
        return True
    
    def release(self) -> None:
        try:
            seq_binance_client_free(self.p)
        except:
            print('error')
    
    def do_request(self, path: str, verb: int, param: str, sign: bool) -> HttpResponse:
        res = HttpResponse()
        seq_binance_client_do_request(self.p, path.ptr, verb, param.ptr, sign, __ptr__(res))
        return res

    def do_get(self, path: str, param: str, sign: bool) -> HttpResponse:
        res = HttpResponse()
        seq_binance_client_do_get(self.p, path.ptr, param.ptr, sign, __ptr__(res))
        return res
    
    def do_post(self, path: str, body: str, sign: bool) -> HttpResponse:
        res = HttpResponse()
        seq_binance_client_do_post(self.p, path.ptr, body.ptr, sign, __ptr__(res))
        return res


if __name__ == "__main__":
    ct_init()
    
    # read
    # access_key = "ACKw0Lk84V6TV1iifPjsNjDLDAtiE1Ex9jf4tMCZEoGAkTMY0gDsPPMqomckfrF8"
    # secret_key = "FA3u3wORvDOg89qBb6ESkQhB9VHgRPvBVAaP6cAMbcWkjNjPTCDLqEAxbDMbrX3h"
    
    # read/write
    # access_key = "9iatcCB5T52TJnvZgyn6OLjQNOPOTnRX3SrjL227rRJfPW1JIhK2rf3ejJCbm5ZW"
    # secret_key = "xQ9mRMrZb90voFsOE3cmCRVf0QZLh45lWlgNui10suUAeOW2XsSTbG1LeM7wR8hs"
    
    # 可能是ip问题
    # {"code":-2015,"msg":"Invalid API-key, IP, or permissions for action, request ip: 172.233.90.165"}
    
    # b = BinanceClient(False, access_key, secret_key)
    
    # testnet
    access_key = "09ae2d615d4ad6a15a22469ae5109b4ab16918bb200fe5cc67d6ece93adf55b2"
    secret_key = "27dad28bf0aaf20aed72884e3b6159b453d8996a6d264d8bf18e737e15651a06"
    
    b = BinanceClient(True, access_key, secret_key)
    
    # time.sleep(3)
    
    symbol = "BTCUSDT"
    
    # try:
    #     server_time = b.fetch_public_time()
    #     print(server_time)
    # except ValueError as e:
    #     print(e)
        
    # try:
    #     exch_info = b.fetch_exchange_info(symbol=symbol)
    #     print(exch_info)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     kline = b.fetch_kline(symbol=symbol, interval="1m", limit=5, start=0, end=0)
    #     print(kline)
    # except ValueError as e:
    #     print(e)
        
    # try:
    #     ob = b.fetch_orderbook(symbol=symbol, limit=5)
    #     print(ob)
    # except ValueError as e:
    #     print(e)

    # try:
    #     a = b.fetch_position_mode(symbol=symbol)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     a = b.switch_position_mode(symbol=symbol, dual_side_position=True)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     a = b.set_leverage(symbol=symbol, leverage=15)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     a = b.place_order(symbol=symbol, side="BUY", position_side="LONG", \
    #         order_type="LIMIT", qty="0.001", price="20000", time_in_force="GTC", \
    #         client_order_id="", reduce_only=False)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     # 198574109438
    #     # UdiCIUrKYXUTlL6X3GpLaD
    #     a = b.cancel_order(symbol=symbol, order_id=0, client_order_id="UdiCIUrKYXUTlL6X3GpLaD")
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     a = b.cancel_orders(symbol=symbol)
    #     print(a)
    # except ValueError as e:
    #     print(e)
        
    # try:
    #     a = b.fetch_balance()
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     a = b.fetch_orders(symbol=symbol)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     a = b.fetch_order(symbol=symbol, order_id=198633222604)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     # fetch_all_orders(self, symbol: str, order_id: int=0, \
    #     # start_time: int=0, end_time: int=0, limit: int=0)
    #     a = b.fetch_all_orders(symbol=symbol, limit=5)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     a = b.fetch_commission_rate(symbol=symbol)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    # try:
    #     a = b.fetch_positions(symbol=symbol)
    #     print(a)
    # except ValueError as e:
    #     print(e)
    
    try:
        a = b.listen_key()
        # a = b.put_listen_key()
        print(a)
    except ValueError as e:
        print(e)
    
    b.release()
    