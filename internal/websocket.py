from ct import LIBRARY

# 启动asio
# SEQ_FUNC void seq_asio_run()
from C import LIBRARY.seq_asio_run() -> None
# 停止asio
# SEQ_FUNC void seq_asio_stop();
from C import LIBRARY.seq_asio_stop() -> None

# SEQ_FUNC WebSocket2 *seq_websocket_new(const char *host, const char *port, const char *path, int tls_version);
from C import LIBRARY.seq_websocket_new(cobj, cobj, cobj, int) -> cobj
# SEQ_FUNC void seq_websocket_delete(WebSocket2 *p);
from C import LIBRARY.seq_websocket_delete(cobj) -> None
# SEQ_FUNC void seq_websocket_connect(WebSocket2 *p);
from C import LIBRARY.seq_websocket_connect(cobj) -> None
# SEQ_FUNC void seq_websocket_send(WebSocket2 *p, const char *text, size_t len);
from C import LIBRARY.seq_websocket_send(cobj, cobj, int) -> None
# SEQ_FUNC void seq_websocket_set_on_connect(WebSocket2 *p,
#                                            OnConnectCallback2 callback);
from C import LIBRARY.seq_websocket_set_on_connect(cobj, cobj) -> None
# SEQ_FUNC void seq_websocket_set_on_heartbeat(WebSocket2 *p,
#                                              OnHeartbeatCallback2 callback);
from C import LIBRARY.seq_websocket_set_on_heartbeat(cobj, cobj) -> None
# SEQ_FUNC void seq_websocket_set_on_message(WebSocket2 *p,
#                                            OnMessageCallback2 callback);
from C import LIBRARY.seq_websocket_set_on_message(cobj, cobj) -> None


TLS1_1_VERSION = 0x0302
TLS1_2_VERSION = 0x0303
TLS1_3_VERSION = 0x0304


class WebSocket:
    _ws: cobj
    
    def __init__(self, host: str, port: str, path: str, tls_version: int=TLS1_3_VERSION):
        self._ws = seq_websocket_new(host.ptr, port.ptr, path.ptr, tls_version)
    
    def c_ptr(self) -> cobj:
        return self._ws
    
    def on_connect(self):
        pass
    
    def on_heartbeat(self):
        pass
    
    def on_message(self, data: cobj, len: int):
        s = str(data, len)
        print('WebSocket::on_message', s)
    
    def release(self):
        seq_websocket_delete(self._ws)
    
    def connect(self):
        seq_websocket_connect(self._ws)
    
    def close(self):
        # seq_websocket_close(self.ws)
        pass
        
    def send(self, text: str):
        seq_websocket_send(self._ws, text.ptr, text.len)
    
    def __repr__(self) -> str:
        return f"<WebSocket: ws={self._ws}>"


ws_event_dict = dict[int, WebSocket]()


@export
def websocket_connect_callback(ws: cobj):
    # print(f'websocket_connect_callback', ws)
    try:
        ws_event_dict[int(ws)].on_connect()
    except:
        print('websocket_connect_callback error')


@export
def websocket_heartbeat_callback(ws: cobj):
    # print(f'websocket_heartbeat_callback', ws)
    try:
        ws_event_dict[int(ws)].on_heartbeat()
    except:
        print('websocket_heartbeat_callback error')


@export
def websocket_message_callback(ws: cobj, data: cobj, len: int):
    # print(f'websocket_message_callback', ws)
    # print('cobj: ', cobj, ' len: ', len)
    try:
        ws_event_dict[int(ws)].on_message(data, len)
    except:
        print('websocket_message_callback error')


def register_websocket(ws: WebSocket):
    """
    注册WS
    """
    seq_websocket_set_on_connect(ws._ws, websocket_connect_callback.__raw__())
    seq_websocket_set_on_heartbeat(ws._ws, websocket_heartbeat_callback.__raw__())
    seq_websocket_set_on_message(ws._ws, websocket_message_callback.__raw__())
    
    ws_event_dict[int(ws._ws)] = ws
