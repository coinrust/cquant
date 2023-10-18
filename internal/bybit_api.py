from typing import Dict
from ct import LIBRARY
from yyjson import yyjson_doc, yyjson_mut_doc, yyjson_val
from bybit_model import ServerTime, ExchangeInfo, KlineItem, OrderBookItem, OrderBook, \
    PositionInfo, OrderResponse, BalanceInfo, OrderInfo
from http import HttpResponse, VERB_PUT, create_query


# const char *baseUrl, const char *accessKey, const char *secretKey
from C import LIBRARY.seq_bybit_client_new(cobj, cobj, cobj) -> cobj
from C import LIBRARY.seq_bybit_client_free(cobj) -> None
# from C import LIBRARY.seq_bybit_client_do_get(cobj, cobj, cobj, bool) -> cobj
from C import LIBRARY.seq_bybit_client_do_get(cobj, cobj, cobj, bool, Ptr[HttpResponse]) -> int
# from C import LIBRARY.seq_bybit_client_do_post(cobj, cobj, cobj, bool) -> cobj
from C import LIBRARY.seq_bybit_client_do_post(cobj, cobj, cobj, bool, Ptr[HttpResponse]) -> int


@tuple
class BybitClient:
    p: cobj
    
    def __new__(base_url: str, access_key: str, secret_key: str):
        return BybitClient(p=seq_bybit_client_new(base_url.ptr, access_key.ptr,
                                                  secret_key.ptr))
        
    def __new__(testnet: bool, access_key: str, secret_key: str):
        base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
        return BybitClient(p=seq_bybit_client_new(base_url.ptr, access_key.ptr,
                                                  secret_key.ptr))
        
    def fetch_public_time(self) -> ServerTime:
        ret = self.do_get("/v3/public/time", "", False)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        
        # {"retCode":0,"retMsg":"OK","result":{"timeSecond":"1696233582","timeNano":"1696233582169993116"},"retExtInfo":{},"time":1696233582169}
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            rusult = root["result"]
            time_second = int(rusult["timeSecond"].str())
            time_nano = int(rusult["timeNano"].str())
            # print('time_nano: ', time_nano)
        
        return ServerTime(time_second, time_nano)
    
    def fetch_exchange_info(self, category: str, symbol: str) -> ExchangeInfo:
        query_values: Dict[str, str] = {}
        query_values["category"] = category
        query_values["symbol"] = symbol
        query_str = create_query(query_values)
        ret = self.do_get("/v5/market/instruments-info", query_str, False)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        
        # {
        #     "retCode": 0,
        #     "retMsg": "OK",
        #     "result": {
        #         "category": "linear",
        #         "list": [{
        #                 "symbol": "BTCUSDT",
        #                 "contractType": "LinearPerpetual",
        #                 "status": "Trading",
        #                 "baseCoin": "BTC",
        #                 "quoteCoin": "USDT",
        #                 "launchTime": "1585526400000",
        #                 "deliveryTime": "0",
        #                 "deliveryFeeRate": "",
        #                 "priceScale": "2",
        #                 "leverageFilter": {
        #                     "minLeverage": "1",
        #                     "maxLeverage": "100.00",
        #                     "leverageStep": "0.01"
        #                 },
        #                 "priceFilter": {
        #                     "minPrice": "0.10",
        #                     "maxPrice": "199999.80",
        #                     "tickSize": "0.10"
        #                 },
        #                 "lotSizeFilter": {
        #                     "maxOrderQty": "100.000",
        #                     "minOrderQty": "0.001",
        #                     "qtyStep": "0.001",
        #                     "postOnlyMaxOrderQty": "1000.000"
        #                 },
        #                 "unifiedMarginTrade": true,
        #                 "fundingInterval": 480,
        #                 "settleCoin": "USDT",
        #                 "copyTrading": "normalOnly"
        #             }
        #         ],
        #         "nextPageCursor": ""
        #     },
        #     "retExtInfo": {},
        #     "time": 1696236288675
        # }
        
        tick_size: float = 0
        stepSize: float = 0

        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result_list = root["result"]["list"]
            arr_list = result_list.array_list()
            if len(arr_list) == 0:
                raise ValueError(f"error list length is 0")
            
            for i in arr_list:
                symbol_ = i["symbol"].str()
                if symbol.upper() != symbol_.upper():
                    continue
                # price_scale = float(result_item_obj["priceScale"].str())
                # print('price_scale: ', price_scale)
                tick_size = float(i["priceFilter"]["tickSize"].str()) # 0.10
                # print('tick_size: ', tick_size)
                
                stepSize = float(i["lotSizeFilter"]["qtyStep"].str()) # 0.001
                # print('stepSize: ', stepSize)
        
        return ExchangeInfo(symbol, tick_size, stepSize)
    
    def fetch_kline(self, category: str, symbol: str, interval: str, limit: int, \
        start: int, end: int) -> List[KlineItem]:
        query_values: Dict[str, str] = {}
        query_values["category"] = category
        query_values["symbol"] = symbol
        query_values["interval"] = interval
        if limit > 0:
            query_values["limit"] = str(limit)
        if start > 0:
            query_values["start"] = str(start)
        if end > 0:
            query_values["end"] = str(end)
        query_str = create_query(query_values)
        ret = self.do_get("/v5/market/kline", query_str, False)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        # {"retCode":0,"retMsg":"OK","result":{"symbol":"BTCUSDT","category":"linear","list":[["1687589640000","30709.9","30710.4","30709.9","30710.3","3.655","112245.7381"],["1687589580000","30707.9","30710","30704.7","30709.9","21.984","675041.8648"],["1687589520000","30708","30714.7","30705","30707.9","33.378","1025097.6459"],["1687589460000","30689.9","30710.3","30689.9","30708","51.984","1595858.2778"],["1687589400000","30678.6","30690.9","30678.5","30689.9","38.747","1188886.4093"]]},"retExtInfo":{},"time":1687589659062}
        
        res = List[KlineItem]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result_list = root["result"]["list"]
            arr_list = result_list.array_list()
            
            for i in arr_list:
                i_arr_list = i.array_list()
                if len(i_arr_list) != 7:
                    print(f'错误: i_arr_list != 7')
                    continue
                
                _timestamp = int(i_arr_list[0].str())
                _open = float(i_arr_list[1].str())
                _high = float(i_arr_list[2].str())
                _low = float(i_arr_list[3].str())
                _close = float(i_arr_list[4].str())
                _volume = float(i_arr_list[5].str())
                _turnover = float(i_arr_list[6].str())
                
                res.append(KlineItem(timestamp=_timestamp, open=_open, high=_high, \
                    low=_low, close=_close, volume=_volume, turnover=_turnover, \
                    confirm=True))
                
        return res
    
    def fetch_orderbook(self, category: str, symbol: str, limit: int) -> OrderBook:
        query_values: Dict[str, str] = {}
        query_values["category"] = category
        query_values["symbol"] = symbol
        if limit > 0:
            query_values["limit"] = str(limit)
        query_str = create_query(query_values)
        ret = self.do_get("/v5/market/orderbook", query_str, False)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        # {
        #     "result": {
        #         "a": [["30604.8", "174.267"], ["30648.6", "0.002"], ["30649.1", "0.001"], ["30650", "1.119"], ["30650.3", "0.01"], ["30650.8", "0.001"], ["30651.6", "0.001"], ["30652", "0.001"], ["30652.4", "0.062"], ["30652.5", "0.001"]],
        #         "b": [["30598.7", "142.31"], ["30578.2", "0.004"], ["30575.3", "0.001"], ["30571.8", "0.001"], ["30571.1", "0.002"], ["30568.5", "0.002"], ["30566.6", "0.005"], ["30565.6", "0.01"], ["30565.5", "0.061"], ["30563", "0.001"]],
        #         "s": "BTCUSDT",
        #         "ts": 1689132447413,
        #         "u": 5223166
        #     },
        #     "retCode": 0,
        #     "retExtInfo": {},
        #     "retMsg": "OK",
        #     "time": 1689132448224
        # }
        
        # res = OrderBook
        asks = List[OrderBookItem]()
        bids = List[OrderBookItem]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result = root["result"]
            a = result["a"]
            a_list = a.array_list()
            for i in a_list:
                i_arr = i.array_list()
                price = float(i_arr[0].str())
                qty = float(i_arr[1].str())
                asks.append(OrderBookItem(price, qty))
            
            b = result["b"]
            b_list = b.array_list()
            for i in b_list:
                i_arr = i.array_list()
                price = float(i_arr[0].str())
                qty = float(i_arr[1].str())
                bids.append(OrderBookItem(price, qty))
                
        return OrderBook(asks, bids)

    
    def switch_position_mode(self, category: str, symbol: str, mode: str) -> bool:
        """
        切换持仓模式
        mode: 0-PositionModeMergedSingle 3-PositionModeBothSides
        """
        with yyjson_mut_doc() as doc:
            doc.add_str("category", category)
            doc.add_str("symbol", symbol)
            doc.add_str("mode", mode)
            body_str = doc.mut_write()
        
        # print(body_str)
        # {"category":"linear","symbol":"BTCUSDT","mode":"0"}
        
        ret = self.do_post("/v5/position/switch-mode", body_str, True)
        # print(ret)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")

        # /*
        # * {"retCode":10004,"retMsg":"error sign! origin_string[1687600745297PglQBNdPTZK6MycUpT15000]","result":{},"retExtInfo":{},"time":1687600744856}
        # * {"retCode":10001,"retMsg":"params error: position_mode invalid","result":{},"retExtInfo":{},"time":1687601751714}
        # * {"retCode":110025,"retMsg":"Position mode is not modified","result":{},"retExtInfo":{},"time":1687601811928}
        # * {"retCode":0,"retMsg":"OK","result":{},"retExtInfo":{},"time":1687601855987}
        # * {"retCode":110025,"retMsg":"Position mode is not modified","result":{},"retExtInfo":{},"time":1696337560088}
        # */
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
        
        return True
    
    def set_leverage(self, category: str, symbol: str, buy_leverage: str, \
        sell_leverage: str) -> bool:
        """
        设置杠杆倍数
        """
        with yyjson_mut_doc() as doc:
            doc.add_str("category", category)
            doc.add_str("symbol", symbol)
            doc.add_str("buyLeverage", buy_leverage)
            doc.add_str("sellLeverage", sell_leverage)
            body_str = doc.mut_write()
        
        # print(body_str)
        
        ret = self.do_post("/v5/position/set-leverage", body_str, True)
        # print(ret)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")

        # /*
        # * {"retCode":0,"retMsg":"OK","result":{},"retExtInfo":{},"time":1696339881214}
        # * {"retCode":110043,"retMsg":"Set leverage not modified","result":{},"retExtInfo":{},"time":1696339921712}
        # */
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
        
        return True
    
    def place_order(self, category: str, symbol: str, side: str, order_type: str, \
        qty: str, price: str, time_in_force: str="", position_idx: int=0, \
        order_link_id: str="", reduce_only: bool=False) -> OrderResponse:
        """
        下单
        """
        with yyjson_mut_doc() as doc:
            doc.add_str("category", category)
            doc.add_str("symbol", symbol)
            doc.add_str("side", side)
            doc.add_str("orderType", order_type)
            doc.add_str("qty", qty)
            if price != "":
                doc.add_str("price", price)
            if time_in_force != "":
                doc.add_str("timeInForce", time_in_force)
            if position_idx != "0":
                doc.add_str("positionIdx", str(position_idx))
            if order_link_id != "":
                doc.add_str("orderLinkId", order_link_id)
            if reduce_only:
                doc.add_str("reduceOnly", "true")
            body_str = doc.mut_write()
        
        # print(body_str)
        
        ret = self.do_post("/v5/order/create", body_str, True)
        # print(ret)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # * {"retCode":10001,"retMsg":"params error: side invalid","result":{},"retExtInfo":{},"time":1687610278834}
        # * {"retCode":10001,"retMsg":"position idx not match position mode","result":{},"retExtInfo":{},"time":1687610314417}
        # * {"retCode":10001,"retMsg":"The number of contracts exceeds minimum limit allowed","result":{},"retExtInfo":{},"time":1687610435384}
        # * {"retCode":110003,"retMsg":"Order price is out of permissible range","result":{},"retExtInfo":{},"time":1687610383879}
        # * {"retCode":110017,"retMsg":"Reduce-only rule not satisfied","result":{},"retExtInfo":{},"time":1689175546336}
        # * {"retCode":0,"retMsg":"OK","result":{"orderId":"b719e004-0846-4b58-8405-a307133c5146","orderLinkId":""},"retExtInfo":{},"time":1689176180262}
        # * {"retCode":0,"retMsg":"OK","result":{"orderId":"44ce1d85-3458-4ec3-af76-41a4cf80c9b3","orderLinkId":""},"retExtInfo":{},"time":1696404669448}
        
        # print(ret.body)
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result = root["result"]
            _order_id = result["orderId"].str()
            _order_link_id = result["orderLinkId"].str()
        
        return OrderResponse(order_id=_order_id, order_link_id=_order_link_id)
    
    def cancel_order(self, category: str, symbol: str, order_id: str, \
        order_link_id: str="") -> OrderResponse:
        """
        撤单
        """
        with yyjson_mut_doc() as doc:
            doc.add_str("category", category)
            doc.add_str("symbol", symbol)
            if order_id != "":
                doc.add_str("orderId", order_id)
            if order_link_id != "":
                doc.add_str("orderLinkId", order_link_id)
            body_str = doc.mut_write()
        
        # print(body_str)
        
        ret = self.do_post("/v5/order/cancel", body_str, True)
        # print(ret)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        
        # * {"retCode":10001,"retMsg":"params error: OrderId or orderLinkId is required","result":{},"retExtInfo":{},"time":1687611859585}
        # * {"retCode":110001,"retMsg":"Order does not exist","result":{},"retExtInfo":{},"time":1689203937336}
        # * {"retCode":0,"retMsg":"OK","result":{"orderId":"1c64212f-8b16-4d4b-90c1-7a4cb55f240a","orderLinkId":""},"retExtInfo":{},"time":1689204723386}
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result = root["result"]
            _order_id = result["orderId"].str()
            _order_link_id = result["orderLinkId"].str()
        
        return OrderResponse(order_id=_order_id, order_link_id=_order_link_id)
    
    def cancel_orders(self, category: str, symbol: str, base_coin: str="", \
        settle_coin: str="") -> List[OrderResponse]:
        """
        批量撤单
        """
        with yyjson_mut_doc() as doc:
            doc.add_str("category", category)
            doc.add_str("symbol", symbol)
            if base_coin != "":
                doc.add_str("baseCoin", base_coin)
            if settle_coin != "":
                doc.add_str("settleCoin", settle_coin)
            body_str = doc.mut_write()
        
        # print(body_str)
        
        ret = self.do_post("/v5/order/cancel-all", body_str, True)
        # print(ret)
        if ret.status != 200:
            raise ValueError(f"error status={ret.status}")
        
        # print(ret.body)
        
        # * {"retCode":0,"retMsg":"OK","result":{"list":[]},"retExtInfo":{},"time":1687612231164}
        res = List[OrderResponse]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result_list = root["result"]["list"]
            for i in result_list:
                _order_id = i["orderId"].str()
                _order_link_id = i["orderLinkId"].str()
                res.append(OrderResponse(order_id=_order_id, order_link_id=_order_link_id))
        
        return res
    
    def fetch_balance(self, account_type: str, coin: str) -> List[BalanceInfo]:
        """
        获取钱包余额
        <param name="accountType">
        統一帳戶: UNIFIED(現貨/USDT和USDC永續/期權), CONTRACT(反向)
        普通帳戶: CONTRACT(期貨), SPOT(現貨)
        </param>
        <param name="coin">USDT,USDC</param>
        """
        query_values: Dict[str, str] = {}
        query_values["accountType"] = account_type
        query_values["coin"] = coin
        query_str = create_query(query_values)
        ret = self.do_get("/v5/account/wallet-balance", query_str, True)
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}]")
        
        # print(ret.body)
        
        # {"retCode":0,"retMsg":"OK","result":{"list":[{"accountType":"CONTRACT","accountIMRate":"","accountMMRate":"","totalEquity":"","totalWalletBalance":"","totalMarginBalance":"","totalAvailableBalance":"","totalPerpUPL":"","totalInitialMargin":"","totalMaintenanceMargin":"","accountLTV":"","coin":[{"coin":"USDT","equity":"20.21","usdValue":"","walletBalance":"20.21","borrowAmount":"","availableToBorrow":"","availableToWithdraw":"20.21","accruedInterest":"","totalOrderIM":"0","totalPositionIM":"0","totalPositionMM":"","unrealisedPnl":"0","cumRealisedPnl":"0"}]}]},"retExtInfo":{},"time":1687608906096}
        res = List[BalanceInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result_list = root["result"]["list"].array_list()
            
            for i in result_list:
                account_type = i["accountType"].str()
                if account_type == "CONTRACT":
                    coin_list = i["coin"].array_list()
                    for c in coin_list:
                        # {
                        #     "coin": "USDT",
                        #     "equity": "1201.92852562",
                        #     "usdValue": "",
                        #     "walletBalance": "1201.92852562",
                        #     "borrowAmount": "",
                        #     "availableToBorrow": "",
                        #     "availableToWithdraw": "1201.92852562",
                        #     "accruedInterest": "",
                        #     "totalOrderIM": "0",
                        #     "totalPositionIM": "0",
                        #     "totalPositionMM": "",
                        #     "unrealisedPnl": "0",
                        #     "cumRealisedPnl": "701.92852562"
                        # }
                        
                        coin_name = c["coin"].str()
                        if coin_name != coin:
                            continue
                        equity = float(c["equity"].str())
                        available_to_withdraw = float(c["availableToWithdraw"].str())
                        wallet_balance = float(c["walletBalance"].str())
                        total_order_im = float(c["totalOrderIM"].str())
                        total_position_im = float(c["totalPositionIM"].str())
                        res.append(BalanceInfo(coin_name=coin_name, equity=equity, \
                            available_to_withdraw=available_to_withdraw, \
                            wallet_balance=wallet_balance, \
                            total_order_im=total_order_im, \
                            total_position_im=total_position_im))
                        
                        # BalanceResponse res;
                        # res.balance.currency = coinName;
                        # res.balance.equity = parseDouble(c["equity"].get_string().value());
                        # res.balance.available = parseDouble(c["availableToWithdraw"].get_string().value());
                        # res.balance.total = parseDouble(c["walletBalance"].get_string().value());
                        # res.balance.orderMargin = 0;
                        # res.balance.positionMargin = 0;
                        # res.balance.frozen = 0;
                elif account_type == "SPOT":
                    coin_list = i["coin"].array_list()
                    # {
                    #     "coin": "USDT",
                    #     "equity": "",
                    #     "usdValue": "",
                    #     "walletBalance": "25.0003",
                    #     "free": "18.7558",
                    #     "locked": "6.2445",
                    #     "availableToWithdraw": "",
                    #     "availableToBorrow": "",
                    #     "borrowAmount": "",
                    #     "accruedInterest": "",
                    #     "totalOrderIM": "",
                    #     "totalPositionIM": "",
                    #     "totalPositionMM": "",
                    #     "unrealisedPnl": "",
                    #     "cumRealisedPnl": ""
                    # }
                
                # res.append(pos)
            
        return res
    
    
    def fetch_orders(self, category: str, symbol: str, order_link_id: str, \
        limit: int, cursor: str) -> List[OrderInfo]:
        """
        获取当前订单
        https://bybit-exchange.github.io/docs/zh-TW/v5/order/open-order
        """
        query_values: Dict[str, str] = {}
        query_values["category"] = category
        query_values["symbol"] = symbol
        if order_link_id != "":
            query_values["orderLinkId"] = order_link_id
        if limit > 0:
            query_values["limit"] = str(limit)
        if cursor != "":
            query_values["cursor"] = cursor
        query_str = create_query(query_values)
        ret = self.do_get("/v5/order/realtime", query_str, True)
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}]")
        
        # print(ret.body)
        
        # {"retCode":0,"retMsg":"OK","result":{"list":[],"nextPageCursor":"","category":"linear"},"retExtInfo":{},"time":1696392159183}
        # {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or recv_window param. req_timestamp[1696396708819],server_timestamp[1696396707813],recv_window[15000]","result":{},"retExtInfo":{},"time":1696396707814}
        
        res = List[OrderInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            # {
            #     "retCode": 0,
            #     "retMsg": "OK",
            #     "result": {
            #         "list": [{
            #                 "orderId": "58364642-a4d6-4c2d-be9b-ce66e2b460b3",
            #                 "orderLinkId": "",
            #                 "blockTradeId": "",
            #                 "symbol": "BTCUSDT",
            #                 "price": "30000.00",
            #                 "qty": "0.001",
            #                 "side": "Buy",
            #                 "isLeverage": "",
            #                 "positionIdx": 0,
            #                 "orderStatus": "New",
            #                 "cancelType": "UNKNOWN",
            #                 "rejectReason": "EC_NoError",
            #                 "avgPrice": "0",
            #                 "leavesQty": "0.001",
            #                 "leavesValue": "30",
            #                 "cumExecQty": "0.000",
            #                 "cumExecValue": "0",
            #                 "cumExecFee": "0",
            #                 "timeInForce": "GTC",
            #                 "orderType": "Limit",
            #                 "stopOrderType": "UNKNOWN",
            #                 "orderIv": "",
            #                 "triggerPrice": "0.00",
            #                 "takeProfit": "0.00",
            #                 "stopLoss": "0.00",
            #                 "tpTriggerBy": "UNKNOWN",
            #                 "slTriggerBy": "UNKNOWN",
            #                 "triggerDirection": 0,
            #                 "triggerBy": "UNKNOWN",
            #                 "lastPriceOnCreated": "",
            #                 "reduceOnly": false,
            #                 "closeOnTrigger": false,
            #                 "smpType": "None",
            #                 "smpGroup": 0,
            #                 "smpOrderId": "",
            #                 "tpslMode": "",
            #                 "tpLimitPrice": "",
            #                 "slLimitPrice": "",
            #                 "placeType": "",
            #                 "createdTime": "1689168691367",
            #                 "updatedTime": "1689168691370"
            #             }
            #         ],
            #         "nextPageCursor": "page_args%3D58364642-a4d6-4c2d-be9b-ce66e2b460b3%26",
            #         "category": "linear"
            #     },
            #     "retExtInfo": {},
            #     "time": 1689168699997
            # }
            
            result_list = root["result"]["list"].array_list()
            
            for i in result_list:
                # position_idx: int   # positionIdx
                # order_id: str       # orderId
                # symbol: str
                # side: str
                # type: str
                # price: float
                # qty: float
                # cum_exec_qty: float # cumExecQty
                # status: str         # orderStatus
                # created_time: str   # createdTime
                # updated_time: str   # updatedTime
                # avg_price: float    # avgPrice
                # cum_exec_fee: float # cumExecFee
                # time_in_force: str  # timeInForce
                # reduce_only: bool   # reduceOnly
                # order_link_id: str  # orderLinkId
                position_idx = i["positionIdx"].int()
                order_id = i["orderId"].str()
                _symbol = i["symbol"].str()
                side = i["side"].str()
                order_type = i["orderType"].str()
                price = float(i["price"].str())
                qty = float(i["qty"].str())
                cum_exec_qty = float(i["cumExecQty"].str())
                order_status = i["orderStatus"].str()
                created_time = i["createdTime"].str()
                updated_time = i["updatedTime"].str()
                avg_price = float(i["avgPrice"].str())
                cum_exec_fee = float(i["cumExecFee"].str())
                time_in_force = i["timeInForce"].str()
                reduce_only = i["reduceOnly"].bool()
                order_link_id = i["orderLinkId"].str()
                
                res.append(OrderInfo(position_idx=position_idx,
                    order_id=order_id,
                    symbol=_symbol,
                    side=side,
                    type=order_type,
                    price=price,
                    qty=qty,
                    cum_exec_qty=cum_exec_qty,
                    status=order_status,
                    created_time=created_time,
                    updated_time=updated_time,
                    avg_price=avg_price,
                    cum_exec_fee=cum_exec_fee,
                    time_in_force=time_in_force,
                    reduce_only=reduce_only,
                    order_link_id=order_link_id))
            
        return res
    
    def fetch_history_orders(self, category: str, symbol: str, order_id: str, \
        order_link_id: str, order_filter: str="", order_status: str="", \
        start_time_ms: int=0, end_time_ms: int=0, limit: int=0, cursor: str="") -> List[OrderInfo]:
        """
        获取历史订单
        https://bybit-exchange.github.io/docs/zh-TW/v5/order/order-list
        """
        query_values: Dict[str, str] = {}
        query_values["category"] = category
        query_values["symbol"] = symbol
        if order_id != "":
            query_values["orderId"] = order_id
        if order_link_id != "":
            query_values["orderLinkId"] = order_link_id
        if order_filter != "":
            query_values["orderFilter"] = order_filter
        if order_status != "":
            query_values["orderStatus"] = order_status
        if start_time_ms > 0:
            query_values["startTimeMs"] = start_time_ms
        if end_time_ms > 0:
            query_values["endTimeMs"] = end_time_ms
        if limit > 0:
            query_values["limit"] = limit
        if cursor != "":
            query_values["cursor"] = cursor
        query_str = create_query(query_values)
        ret = self.do_get("/v5/order/history", query_str, True)
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}]")
        
        print(ret.body)
        
        # 
        
        res = List[OrderInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result_list = root["result"]["list"].array_list()
            
            for i in result_list:
                # position_idx: int   # positionIdx
                # order_id: str       # orderId
                # symbol: str
                # side: str
                # type: str
                # price: float
                # qty: float
                # cum_exec_qty: float # cumExecQty
                # status: str         # orderStatus
                # created_time: str   # createdTime
                # updated_time: str   # updatedTime
                # avg_price: float    # avgPrice
                # cum_exec_fee: float # cumExecFee
                # time_in_force: str  # timeInForce
                # reduce_only: bool   # reduceOnly
                # order_link_id: str  # orderLinkId
                position_idx = i["positionIdx"].int()
                order_id = i["orderId"].str()
                _symbol = i["symbol"].str()
                side = i["side"].str()
                order_type = i["orderType"].str()
                price = float(i["price"].str())
                qty = float(i["qty"].str())
                cum_exec_qty = float(i["cumExecQty"].str())
                order_status = i["orderStatus"].str()
                created_time = i["createdTime"].str()
                updated_time = i["updatedTime"].str()
                avg_price = float(i["avgPrice"].str())
                cum_exec_fee = float(i["cumExecFee"].str())
                time_in_force = i["timeInForce"].str()
                reduce_only = i["reduceOnly"].bool()
                order_link_id = i["orderLinkId"].str()
                
                res.append(OrderInfo(position_idx=position_idx,
                    order_id=order_id,
                    symbol=_symbol,
                    side=side,
                    type=order_type,
                    price=price,
                    qty=qty,
                    cum_exec_qty=cum_exec_qty,
                    status=order_status,
                    created_time=created_time,
                    updated_time=updated_time,
                    avg_price=avg_price,
                    cum_exec_fee=cum_exec_fee,
                    time_in_force=time_in_force,
                    reduce_only=reduce_only,
                    order_link_id=order_link_id))
            
        return res
    
    def fetch_positions(self, category: str, symbol: str) -> List[PositionInfo]:
        query_values: Dict[str, str] = {}
        query_values["category"] = category
        query_values["symbol"] = symbol
        # baseCoin, settleCoin, limit, cursor
        query_str = create_query(query_values)
        ret = self.do_get("/v5/position/list", query_str, True)
        if ret.status != 200:
            raise ValueError(f"error status=[{ret.status}]")
        
        # {"retCode":10002,"retMsg":"invalid request, please check your server timestamp or recv_window param. req_timestamp[1696255257619],server_timestamp[1696255255967],recv_window[15000]","result":{},"retExtInfo":{},"time":1696255255967}
        
        # print(ret.body)
        
        res = List[PositionInfo]()
        
        with yyjson_doc(ret.body) as doc:
            root = doc.root()
            ret_code = root["retCode"].int()
            ret_msg = root["retMsg"].str()
            if ret_code != 0:
                raise ValueError(f"error retCode={ret_code}, retMsg={ret_msg}")
            
            result_list = root["result"]["list"].array_list()
            
            for i in result_list:
                _symbol = i["symbol"].str()
                if _symbol != symbol:
                    continue
                
                # {
                #     "positionIdx": 0,
                #     "riskId": 1,
                #     "riskLimitValue": "2000000",
                #     "symbol": "BTCUSDT",
                #     "side": "None",
                #     "size": "0.000",
                #     "avgPrice": "0",
                #     "positionValue": "0",
                #     "tradeMode": 0,
                #     "positionStatus": "Normal",
                #     "autoAddMargin": 0,
                #     "adlRankIndicator": 0,
                #     "leverage": "1",
                #     "positionBalance": "0",
                #     "markPrice": "26515.73",
                #     "liqPrice": "",
                #     "bustPrice": "0.00",
                #     "positionMM": "0",
                #     "positionIM": "0",
                #     "tpslMode": "Full",
                #     "takeProfit": "0.00",
                #     "stopLoss": "0.00",
                #     "trailingStop": "0.00",
                #     "unrealisedPnl": "0",
                #     "cumRealisedPnl": "-19.59637027",
                #     "seq": 8172241025,
                #     "createdTime": "1682125794703",
                #     "updatedTime": "1694995200083"
                # }
                
                _position_idx = i["positionIdx"].int()
                # _risk_id = i["riskId"].int()
                _side = i["side"].str()
                _size = i["size"].str()
                _avg_price = i["avgPrice"].str()
                _position_value = i["positionValue"].str()
                _leverage = i["leverage"].float()
                _mark_price = i["markPrice"].str()
                # _liq_price = i["liqPrice"].str()
                # _bust_price = i["bustPrice"].str()
                _position_mm = i["positionMM"].str()
                _position_im = i["positionIM"].str()
                _take_profit = i["takeProfit"].str()
                _stop_loss = i["stopLoss"].str()
                _unrealised_pnl = i["unrealisedPnl"].str()
                _cum_realised_pnl = i["cumRealisedPnl"].str()
                # _seq = i["seq"].int()
                _created_time = i["createdTime"].str()
                _updated_time = i["updatedTime"].str()
                pos = PositionInfo(position_idx=_position_idx, symbol=_symbol, \
                    side=_side, size=_size, avg_price=_avg_price, \
                    position_value=_position_value, leverage=_leverage, \
                    mark_price=_mark_price, position_mm=_position_mm, \
                    position_im=_position_im, take_profit=_take_profit, \
                    stop_loss=_stop_loss, unrealised_pnl=_unrealised_pnl, \
                    created_time=_created_time, updated_time=_updated_time)
                res.append(pos)
            
        return res
    
    def release(self) -> None:
        try:
            seq_bybit_client_free(self.p)
        except:
            print('error')

    def do_get(self, path: str, param: str, sign: bool) -> ct_http_response:
        res = ct_http_response()
        seq_bybit_client_do_get(self.p, path.ptr, param.ptr, sign, __ptr__(res))
        return res
    
    def do_post(self, path: str, body: str, sign: bool) -> ct_http_response:
        res = ct_http_response()
        seq_bybit_client_do_post(self.p, path.ptr, body.ptr, sign, __ptr__(res))
        return res

