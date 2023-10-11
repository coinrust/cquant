from ct import LIBRARY


# // 创建 WSClient 实例
# SEQ_FUNC WSClient* seq_wsclient_new(const char* url);
from C import LIBRARY.seq_wsclient_new(cobj) -> cobj
# // 设置连接回调函数
# SEQ_FUNC void seq_set_on_connect(WSClient* p, OnConnectCallback callback);
from C import LIBRARY.seq_set_on_connect(cobj, cobj) -> None
# // 设置心跳回调函数
# SEQ_FUNC void seq_set_on_heartbeat(WSClient* p, OnHeartbeatCallback callback);
from C import LIBRARY.seq_set_on_heartbeat(cobj, cobj) -> None
# // 设置消息回调函数
# SEQ_FUNC void seq_set_on_message(WSClient* p, OnMessageCallback callback);
from C import LIBRARY.seq_set_on_message(cobj, cobj) -> None
# // 释放 WSClient 实例
# SEQ_FUNC void seq_wsclient_free(WSClient* p);
from C import LIBRARY.seq_wsclient_free(cobj) -> None
# // 关闭 WS
# SEQ_FUNC void seq_wsclient_close(WSClient* p);
from C import LIBRARY.seq_wsclient_close(cobj) -> None
# // 连接
# SEQ_FUNC void seq_wsclient_connect(WSClient* p);
from C import LIBRARY.seq_wsclient_connect(cobj) -> None
# // 重置
# SEQ_FUNC void seq_wsclient_reset(WSClient* p);
from C import LIBRARY.seq_wsclient_reset(cobj) -> None
# // 发送消息
# SEQ_FUNC void seq_wsclient_send(WSClient* p, const char* text, size_t len);
from C import LIBRARY.seq_wsclient_send(cobj, cobj, int) -> None
