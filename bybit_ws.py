import time
from ct import ct_init, seq_nanoid, seq_hmac_encode, fix_c_str, caller, shutdown_requested, LIBRARY
from yyjson import yyjson_mut_doc
from ws import seq_wsclient_new, seq_set_on_connect, seq_set_on_heartbeat, \
    seq_set_on_message, seq_wsclient_free, seq_wsclient_close, seq_wsclient_connect, \
    seq_wsclient_reset, seq_wsclient_send


# typedef void (*OnConnectCallback)(WSClient* ws);
# typedef void (*OnHeartbeatCallback)(WSClient* ws);
# typedef void (*OnMessageCallback)(WSClient* ws, const char * data, size_t len);


V5WebsocketPublicTopicOrderBook = "orderbook"
V5WebsocketPublicTopicTrade = "publicTrade"
V5WebsocketPublicTopicKline = "kline"
V5WebsocketPublicTopicTicker = "tickers"
V5WebsocketPrivateTopicPong = "pong"
V5WebsocketPrivateTopicOrder = "order"
V5WebsocketPrivateTopicExecution = "execution"
V5WebsocketPrivateTopicPosition = "position"
V5WebsocketPrivateTopicWallet = "wallet"


@tuple
class WSClient:
    ws: cobj
    access_key: str
    secret_key: str

# 客户端字典
# key: int(ws ptr)
wsclient_dict = dict[int, WSClient]()


@extend
class WSClient:
    def __new__(url: str, access_key: str, secret_key: str):
        # self.access_key = access_key
        # self.secret_key = secret_key
        ws = seq_wsclient_new(url.ptr)
        return WSClient(access_key=access_key, secret_key=secret_key, ws=ws)
    
    def __new__(testnet: bool, private: bool, access_key: str, secret_key: str, \
        category: str="linear"):
        if private and access_key == "" and secret_key == "":
            #raise ValueError("WSClient init param error")
            print("WSClient init param error")
        host = "stream-testnet.bybit.com" if testnet else "stream.bybit.com"
        path = "/v5/private" if private else f"/v5/public/{category}"
        url = f"wss://{host}{path}"
        ws = seq_wsclient_new(url.ptr)
        return WSClient(access_key=access_key, secret_key=secret_key, ws=ws)
    
    def release(self):
        seq_wsclient_free(self.ws)
    
    def connect(self):
        seq_wsclient_connect(self.ws)
    
    def close(self):
        seq_wsclient_close(self.ws)
        
    def send(self, text: str):
        seq_wsclient_send(self.ws, text.ptr, text.len)
        
    def on_connect(self):
        print('on_connect')
        
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
        
        hex_signature = seq_hmac_encode(self.secret_key.ptr, fix_c_str(req).ptr)

        auth_template = '{"req_id":"10000","op":"auth","args":["api_key",1662350400000,"signature"]}'
        data = auth_template.replace('10000', seq_nanoid())\
            .replace("api_key", self.access_key)\
            .replace("1662350400000", str(expires))\
            .replace("signature", hex_signature)
        
        print("auth: ", data)
        
        self.send(data)
    
    def _subscribe(self):
        # orderbook.1.BTCUSDT
        # publicTrade.BTCUSDT
        # tickers.BTCUSDT
        # kline.1.BTCUSDT
        
        # topics = ["orderbook.1.BTCUSDT", "publicTrade.BTCUSDT"]
        topics = ["orderbook.1.BTCUSDT"]
        
        with yyjson_mut_doc() as doc:
            doc.add_str("req_id", seq_nanoid())
            doc.add_str("op", "subscribe")
            doc.arr_with_str("args", topics)
            
            data = doc.mut_write()
        
        print("subscribe: ", data)
        
        self.send(data)
    
    def on_heartbeat(self):
        print('on_heartbeat')
        
        with yyjson_mut_doc() as doc:
            doc.add_str("req_id", seq_nanoid())
            doc.add_str("op", "ping")
            
            data = doc.mut_write()
        
        print("ping: ", data)
        
        self.send(data)
        
    def on_message(self, data: cobj, len: int):
        # {"success":false,"ret_msg":"error:handler not found,topic:getOrderBook.1.BTCUSDT","conn_id":"958a35b7-c1fb-48e3-953f-997702f22f6e","req_id":"2XXN2rHDDOBDbEQH-WsRa","op":"subscribe"}
        # {"success":true,"ret_msg":"pong","conn_id":"958a35b7-c1fb-48e3-953f-997702f22f6e","req_id":"yQTJaPDH0sty3HDrOEiSX","op":"ping"}
        # print('on_message', data, len)
        # 0xffff88111040 153
        s = str(data, len)
        print('on_message', s)
        # {"topic":"publicTrade.BTCUSDT","type":"snapshot","ts":1696572949307,"data":[{"T":1696572949305,"s":"BTCUSDT","S":"Buy","v":"0.003","p":"27473.30","L":"ZeroPlusTick","i":"5252c117-9258-5fc7-8b08-23998055be9e","BT":false},{"T":1696572949305,"s":"BTCUSDT","S":"Buy","v":"0.007","p":"27473.30","L":"ZeroPlusTick","i":"58a98654-f87b-58b0-91f2-41bb12ca59b9","BT":false},{"T":1696572949305,"s":"BTCUSDT","S":"Buy","v":"0.005","p":"27473.30","L":"ZeroPlusTick","i":"7d71e0c3-b8d9-52c8-89f2-ad5e5302ac4f","BT":false}]}
        
        # {"topic":"orderbook.1.BTCUSDT","type":"snapshot","ts":1696581023728,"data":{"s":"BTCUSDT","b":[["27646.80","5.317"]],"a":[["27646.90","18.740"]],"u":42452159,"seq":88215706297}}
        # on_message {"topic":"orderbook.1.BTCUSDT","type":"delta","ts":1696581023748,"data":{"s":"BTCUSDT","b":[],"a":[["27646.90","20.396"]],"u":42452160,"seq":88215706351}}
        # on_message {"topic":"orderbook.1.BTCUSDT","type":"delta","ts":1696581023767,"data":{"s":"BTCUSDT","b":[["27646.80","4.564"]],"a":[],"u":42452161,"seq":88215706385}}
        # on_message {"topic":"orderbook.1.BTCUSDT","type":"delta","ts":1696581023798,"data":{"s":"BTCUSDT","b":[["27646.80","4.743"]],"a":[],"u":42452162,"seq":88215706473}}
        # on_message {"topic":"orderbook.1.BTCUSDT","type":"delta","ts":1696581023807,"data":{"s":"BTCUSDT","b":[],"a":[["27646.90","19.615"]],"u":42452163,"seq":88215706515}}
        
        # https://www.codearmo.com/python-tutorial/bybit-websockets-python
        # https://github.com/bybit-exchange/pybit/blob/master/README.md
        
    def __repr__(self) -> str:
        return f"<WSClient: ws={self.ws}>"


@export
def wsclient_connect_callback(ws: cobj):
    print(f'wsclient_connect_callback', ws)
    #if ws in wsclient_dict:
    # global wsclient_dict
    try:
        wsclient_dict[int(ws)].on_connect()
    except:
        print('wsclient_connect_callback error')
    # print(wsclient_dict)


@export
def wsclient_heartbeat_callback(ws: cobj):
    print(f'wsclient_heartbeat_callback', ws)
    try:
        wsclient_dict[int(ws)].on_heartbeat()
    except:
        print('wsclient_heartbeat_callback error')


@export
def wsclient_message_callback(ws: cobj, data: cobj, len: int):
    # print(f'wsclient_message_callback', ws)
    # print('cobj: ', cobj, ' len: ', len)
    try:
        wsclient_dict[int(ws)].on_message(data, len)
    except:
        print('wsclient_message_callback error')


def register_ws(ws: WSClient):
    """
    注册WS
    """
    seq_set_on_connect(ws.ws, wsclient_connect_callback.__raw__())
    seq_set_on_heartbeat(ws.ws, wsclient_heartbeat_callback.__raw__())
    seq_set_on_message(ws.ws, wsclient_message_callback.__raw__())
    
    # print(int(ws.ws), ws.ws)
    wsclient_dict[int(ws.ws)] = ws


if __name__ == "__main__":
    ct_init()
    
    # url = "wss://socketsbay.com/wss/v2/1/demo/"
    # url = "wss://stream.bybit.com/v5/public/linear"
    # ws = WSClient(url, "", "")
    
    ws = WSClient(testnet=False, private=False, access_key="", secret_key="")
    register_ws(ws)
    ws.connect()
    
    while not shutdown_requested():
        time.sleep(0.1)
    