import time
from ct import seq_nanoid, seq_hmac_encode, safe_c_str
from log import logvd, logvi
from yyjson import yyjson_mut_doc
from websocket import WebSocket, register_websocket, TLS1_2_VERSION


class BinanceWebsockt(WebSocket):
    # _ws: cobj
    listen_key: str
    topics: list[str]

    def __init__(self, testnet: bool, listen_key: str):
        host = "stream.binancefuture.com" if testnet else "fstream.binance.com"
        if listen_key != "":
            path = f"/ws/{listen_key}"
        else:
            path = "/stream"
        port = "443"
        self.listen_key = listen_key
        self.topics = []
        super().__init__(host=host, port=port, path=path, tls_version=TLS1_2_VERSION)
        logvi(f"ws={self._ws}")
        register_websocket(self)
    
    def subscribe(self, topics: list[str]):
        """
        设置订阅
        """
        for i in topics:
            self.topics.append(i)
    
    def on_connect(self):
        logvi('on_connect')
        
        # 认证
        self._auth()
        
        # 订阅
        self._subscribe()
        
    def _auth(self):
        pass
    
    def _subscribe(self):
        # topics = ["btcusdt@aggTrade", "btcusdt@depth"]
        if len(self.topics) == 0:
            return
        
        # topics = ["btcusdt@aggTrade"]
        
        # kline
        # <symbol>@kline_<interval>
        # 1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M
        
        if self.listen_key == "":
            with yyjson_mut_doc() as doc:
                doc.add_int("id", 1)
                # method = "SUBSCRIBE" if self.listen_key == "" else "REQUEST"
                doc.add_str("method", "SUBSCRIBE")
                # doc.add_str("method", method)
                doc.arr_with_str("params", self.topics)
                
                data = doc.mut_write()
            
            logvi(f"subscribe: {data}")
            
            self.send(data)
    
    def on_heartbeat(self):
        logvi('on_heartbeat')
        # text = "ping"
        # print("send ping: ", text)
        # self.send_ping(text)
        if self.listen_key != "":
            with yyjson_mut_doc() as doc:
                doc.add_int("id", 1)
                method = "SUBSCRIBE"
                # doc.add_str("method", "SUBSCRIBE")
                doc.add_str("method", method)
                doc.arr_with_str("params", self.topics)
                
                data = doc.mut_write()
            
            logvi(f"subscribe: {data}")
            
            self.send(data)
        
    def on_message(self, data: cobj, len: int):
        # print('on_message', data, len)
        # 0xffff88111040 153
        # s = str(data, len)
        # print('on_message', s)
        # n = strlen(cobj)
        # print("2", n)
        s = str.from_ptr(data)
        logvi(f"on_message: {s}")
        # {"stream":"btcusdt@aggTrade","data":{"e":"aggTrade","E":1697350051134,"a":1874727048,"s":"BTCUSDT","p":"26863.20","q":"0.003","f":4169335773,"l":4169335773,"T":1697350050981,"m":true}}
        # {"stream":"btcusdt@depth","data":{"e":"depthUpdate","E":1697350498111,"T":1697350498109,"s":"BTCUSDT","U":3360499966520,"u":3360499977816,"pu":3360499965865,"b":[["5000.00","225.834"],["20000.00","232.523"],["25518.20","0.041"],["25518.30","0.234"],["26060.00","18.622"],["26443.90","1.892"],["26592.70","0.000"],["26634.80","0.196"],["26636.40","0.104"],["26727.00","1.502"],["26755.00","14.237"],["26770.80","2.133"],["26770.90","0.131"],["26773.10","0.281"],["26773.20","13.965"],["26794.10","0.022"],["26794.20","3.353"],["26795.80","0.075"],["26795.90","1.433"],["26805.80","0.030"],["26810.10","0.417"],["26811.10","7.333"],["26811.40","0.797"],["26812.20","0.004"],["26813.30","0.096"],["26814.50","0.060"],["26817.30","0.026"],["26817.50","2.137"],["26818.40","0.056"],["26818.50","5.360"],["26819.40","0.177"],["26821.80","0.006"],["26829.40","3.694"],["26831.70","1.221"],["26833.10","0.932"],["26835.50","0.312"],["26840.90","0.381"],["26842.70","3.181"],["26842.80","0.055"],["26842.90","0.540"],["26843.00","2.204"],["26843.10","2.578"],["26843.30","5.817"],["26844.10","0.016"],["26844.40","0.524"],["26844.80","1.598"],["26845.20","0.212"],["26845.40","0.736"],["26845.50","5.404"],["26845.80","0.572"],["26845.90","0.194"],["26847.00","1.387"],["26847.30","2.495"],["26847.70","3.681"],["26848.00","6.767"],["26848.10","4.425"],["26848.20","6.628"],["26848.30","0.001"],["26848.40","0.047"],["26848.50","4.642"],["26849.10","2.423"],["26849.30","6.373"],["26849.40","0.044"],["26850.10","0.016"],["26850.30","2.832"],["26850.40","2.521"],["26850.50","2.010"],["26850.70","2.680"],["26850.80","2.481"],["26850.90","0.421"],["26851.00","4.458"],["26852.30","0.909"],["26852.60","0.092"],["26852.90","0.106"],["26853.00","6.401"],["26853.20","8.318"],["26853.40","0.001"],["26853.70","0.155"],["26854.00","9.180"],["26854.40","12.513"],["26854.70","6.405"],["26854.80","7.455"],["26855.20","17.424"],["26855.30","10.477"],["26856.20","3.241"],["26856.30","4.167"],["26858.20","0.338"],["26858.60","2.304"],["26858.80","5.288"],["26859.00","5.564"],["26860.50","0.125"],["26860.90","3.814"],["26861.20","1.823"],["26861.30","21.816"]],"a":[["26861.40","16.561"],["26861.70","0.653"],["26862.10","2.092"],["26862.20","4.261"],["26862.30","0.416"],["26862.40","0.013"],["26862.50","0.527"],["26862.70","0.726"],["26863.40","2.323"],["26864.00","0.182"],["26864.10","3.064"],["26864.50","2.916"],["26865.30","0.213"],["26865.40","1.420"],["26866.00","0.274"],["26866.50","0.604"],["26869.20","19.453"],["26869.30","0.445"],["26869.40","0.102"],["26869.50","2.733"],["26869.60","3.387"],["26869.70","1.500"],["26869.90","1.890"],["26870.00","5.911"],["26870.10","0.639"],["26870.20","0.093"],["26870.50","2.540"],["26870.60","1.904"],["26870.70","0.187"],["26870.90","0.187"],["26871.50","1.647"],["26871.80","1.102"],["26872.40","3.020"],["26873.50","0.026"],["26914.60","0.646"],["26914.70","15.701"],["26916.40","0.026"],["26916.60","0.063"],["26937.80","0.058"],["26937.90","0.059"],["26939.10","0.029"],["26939.20","0.001"],["26945.10","0.048"],["26951.50","0.093"],["26952.00","0.749"],["26952.40","0.199"],["26952.90","0.560"],["26953.00","2.465"],["26953.90","1.519"],["26954.50","0.337"],["26954.70","0.072"],["26954.90","0.003"],["26955.20","0.129"],["26955.40","0.032"],["26955.60","0.157"],["26956.00","3.863"],["26956.10","1.579"],["26956.20","0.670"],["26956.40","0.025"],["26956.50","0.221"],["26957.10","0.090"],["26957.40","0.057"],["26957.50","0.402"],["26957.70","0.035"],["26957.90","0.142"],["26958.00","21.684"],["26958.30","0.040"],["26958.60","0.034"],["26958.80","0.034"],["26959.00","0.709"],["26959.70","0.063"],["26959.80","1.282"],["26959.90","0.108"],["26960.60","0.862"],["26960.70","13.791"],["26961.00","3.271"],["26961.10","0.000"],["26961.20","0.009"],["26961.30","0.083"],["26961.80","1.528"],["26962.20","2.340"],["26963.30","1.154"],["26978.60","0.030"],["26978.90","1.972"],["26981.90","0.090"],["26982.20","1.655"],["26992.30","0.008"],["26998.60","0.001"],["27000.00","256.514"],["27000.20","0.087"],["27004.60","0.099"],["27023.60","0.065"],["27025.30","0.000"],["27130.00","10.577"],["27195.40","0.241"],["27264.10","0.151"],["27331.50","3.658"],["27935.80","1.795"],["28204.30","0.019"]]}}
        # {"stream":"btcusdt@kline_1m","data":{"e":"kline","E":1697350497988,"s":"BTCUSDT","k":{"t":1697350440000, "T":1697350499999, "s":"BTCUSDT", "i":"1m", "f":4169337751, "L":4169338001, "o":"26860", "c":"26861.40", "h":"26861.40", "l":"26860", "v":"10.714", "n":251, "x":false, "q":"287779.05600", "V":"3.732", "Q":"100242.03420", "B":"0"}}}
        
    def __repr__(self) -> str:
        return f"<BinanceWebsocket: ws={self.ws}>"
