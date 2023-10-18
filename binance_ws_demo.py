import sys
from internal.ct import ct_init, seq_set_seq_signal_handler
from internal.log import init_log, logvi
from internal.websocket import seq_asio_run, seq_asio_stop
from internal.binance_ws import BinanceWebsockt


@export
def sigint_handler(s: int):
    logvi(f'sigint_handler: {s}')
    seq_asio_stop()
    logvi("exit")
    sys.exit(0)
    
    
if __name__ == "__main__":
    ct_init()
    
    seq_set_seq_signal_handler(sigint_handler.__raw__())
    
    init_log("INFO")
    
    listen_key = ""
    ws = BinanceWebsockt(testnet=False, listen_key=listen_key)
    
    ws.subscribe(["btcusdt@aggTrade", "btcusdt@depth", "btcusdt@kline_1m"])
    # ws.subscribe(["btcusdt@kline_1m"])
    # ws.subscribe(["btcusdt@kline_1m"])
    
    # ws.subscribe([f"{listen_key}@account", f"{listen_key}@balance"])
    ws.connect()
    
    seq_asio_run()
    