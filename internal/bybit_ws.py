import time
from ct import seq_nanoid, seq_hmac_encode, safe_c_str
from log import logvd, logvi
from yyjson import yyjson_mut_doc, yyjson_doc
from websocket import WebSocket, register_websocket


V5WebsocketPublicTopicOrderBook = "orderbook"
V5WebsocketPublicTopicTrade = "publicTrade"
V5WebsocketPublicTopicKline = "kline"
V5WebsocketPublicTopicTicker = "tickers"
V5WebsocketPrivateTopicPong = "pong"
V5WebsocketPrivateTopicOrder = "order"
V5WebsocketPrivateTopicExecution = "execution"
V5WebsocketPrivateTopicPosition = "position"
V5WebsocketPrivateTopicWallet = "wallet"


class BybitWebsockt(WebSocket):
    # _ws: cobj
    access_key: str
    secret_key: str
    topics: list[str]
    
    def __init__(self, testnet: bool, private: bool, access_key: str, secret_key: str, \
        category: str="linear"):
        if private and access_key == "" and secret_key == "":
            #raise ValueError("WSClient init param error")
            print("WebSocket init param error")
        host = "stream-testnet.bybit.com" if testnet else "stream.bybit.com"
        port = "443"
        path = "/v5/private" if private else f"/v5/public/{category}"
        # url = f"wss://{host}{path}"
        self.access_key = access_key
        self.secret_key = secret_key
        self.topics = []
        super().__init__(host=host, port=port, path=path)
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
        if self.access_key == "" or self.secret_key == "":
            return
        
        now = time.time()
        expires = int(now * 1000) + 10000

        req = "GET/realtime" + str(expires)
        
        hex_signature = seq_hmac_encode(self.secret_key.ptr, safe_c_str(req).ptr)

        auth_template = '{"req_id":"10000","op":"auth","args":["api_key",1662350400000,"signature"]}'
        data = auth_template.replace('10000', seq_nanoid())\
            .replace("api_key", self.access_key)\
            .replace("1662350400000", str(expires))\
            .replace("signature", hex_signature)
        
        logvi(f"auth: {data}")
        
        self.send(data)
    
    def _subscribe(self):
        # orderbook.1.BTCUSDT
        # publicTrade.BTCUSDT
        # tickers.BTCUSDT
        # kline.1.BTCUSDT
        
        # topics = ["orderbook.1.BTCUSDT", "publicTrade.BTCUSDT"]
        # topics = ["orderbook.1.BTCUSDT"]
        
        with yyjson_mut_doc() as doc:
            doc.add_str("req_id", seq_nanoid())
            doc.add_str("op", "subscribe")
            doc.arr_with_str("args", self.topics)
            
            data = doc.mut_write()
        
        logvi(f"subscribe: {data}")
        
        self.send(data)
    
    def on_heartbeat(self):
        logvi('on_heartbeat')
        
        with yyjson_mut_doc() as doc:
            doc.add_str("req_id", seq_nanoid())
            doc.add_str("op", "ping")
            
            data = doc.mut_write()
        
        logvi(f"ping: {data}")
        
        self.send(data)
        
    def on_message(self, data: cobj, len: int):
        # {"success":false,"ret_msg":"error:handler not found,topic:getOrderBook.1.BTCUSDT","conn_id":"958a35b7-c1fb-48e3-953f-997702f22f6e","req_id":"2XXN2rHDDOBDbEQH-WsRa","op":"subscribe"}
        # {"success":true,"ret_msg":"pong","conn_id":"958a35b7-c1fb-48e3-953f-997702f22f6e","req_id":"yQTJaPDH0sty3HDrOEiSX","op":"ping"}
        # print('on_message', data, len)
        # 0xffff88111040 153
        s = str(data, len)
        logvi(f"on_message: {s}")
        with yyjson_doc(s) as doc:
            root = doc.root()
        # {"topic":"publicTrade.BTCUSDT","type":"snapshot","ts":1696572949307,"data":[{"T":1696572949305,"s":"BTCUSDT","S":"Buy","v":"0.003","p":"27473.30","L":"ZeroPlusTick","i":"5252c117-9258-5fc7-8b08-23998055be9e","BT":false},{"T":1696572949305,"s":"BTCUSDT","S":"Buy","v":"0.007","p":"27473.30","L":"ZeroPlusTick","i":"58a98654-f87b-58b0-91f2-41bb12ca59b9","BT":false},{"T":1696572949305,"s":"BTCUSDT","S":"Buy","v":"0.005","p":"27473.30","L":"ZeroPlusTick","i":"7d71e0c3-b8d9-52c8-89f2-ad5e5302ac4f","BT":false}]}
        
        # {"topic":"orderbook.1.BTCUSDT","type":"snapshot","ts":1696581023728,"data":{"s":"BTCUSDT","b":[["27646.80","5.317"]],"a":[["27646.90","18.740"]],"u":42452159,"seq":88215706297}}
        # on_message {"topic":"orderbook.1.BTCUSDT","type":"delta","ts":1696581023748,"data":{"s":"BTCUSDT","b":[],"a":[["27646.90","20.396"]],"u":42452160,"seq":88215706351}}
        # on_message {"topic":"orderbook.1.BTCUSDT","type":"delta","ts":1696581023767,"data":{"s":"BTCUSDT","b":[["27646.80","4.564"]],"a":[],"u":42452161,"seq":88215706385}}
        # on_message {"topic":"orderbook.1.BTCUSDT","type":"delta","ts":1696581023798,"data":{"s":"BTCUSDT","b":[["27646.80","4.743"]],"a":[],"u":42452162,"seq":88215706473}}
        # on_message {"topic":"orderbook.1.BTCUSDT","type":"delta","ts":1696581023807,"data":{"s":"BTCUSDT","b":[],"a":[["27646.90","19.615"]],"u":42452163,"seq":88215706515}}
        
        # https://www.codearmo.com/python-tutorial/bybit-websockets-python
        # https://github.com/bybit-exchange/pybit/blob/master/README.md
        
    def __repr__(self) -> str:
        return f"<BybitWebsocket: ws={self._ws}>"
