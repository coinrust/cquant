import sys
from internal.ct import ct_init, seq_set_seq_signal_handler
from internal.log import init_log, logvi
from internal.websocket import seq_asio_run, seq_asio_stop
from internal.bybit_ws import BybitWebsockt


@export
def sigint_handler(s: int):
    logvi(f'sigint_handler: {s}')
    seq_asio_stop()
    logvi("exit")
    sys.exit(0)


if __name__ == "__main__":
    ct_init()
    
    seq_set_seq_signal_handler(sigint_handler.__raw__())

    # init_log("DEBUG")
    init_log("INFO")
    
    ws = BybitWebsockt(testnet=False, private=False, access_key="", secret_key="")
    ws.subscribe(["orderbook.1.BTCUSDT", "publicTrade.BTCUSDT"])
    ws.connect()
    
    seq_asio_run()
    