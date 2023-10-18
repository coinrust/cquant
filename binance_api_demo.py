from internal.ct import ct_init
from internal.binance_api import BinanceClient


# {"code":-1021,"msg":"Timestamp for this request was 1000ms ahead of the server's time."}
# {"code":-2015,"msg":"Invalid API-key, IP, or permissions for action, request ip: x.x.x.x"}


if __name__ == "__main__":
    ct_init()
    
    # testnet
    access_key = ""
    secret_key = ""
    
    b = BinanceClient(True, access_key, secret_key)
    
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
    