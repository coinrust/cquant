## essentials-of-codon-quant

This is an open source quantitative trading system built with Codon, Python and C++ for performance. It includes:

* Bybit API wrapper for placing trades (bybit_api.py)
* Bybit websocket for streaming market data (bybit_ws.py)
* Fixed price skip list data structure (foundation.py)
* Fast JSON parsing using yyjson (yyjson.py)
* C++ foundation for performance (libctrt.so - not open sourced)

### Requirements

* Python 3.11+
* Codon runtime
* Bybit account and API keys

### Usage

Export the Codon Python library path:

```shell
export CODON_PYTHON=/path/to/libpython3.11.so
```

Run strategies with Codon:

```shell
codon run -release binance_ws_demo.py
```

Implement your trading strategies in Python. They can take advantage of the Bybit API wrapper, websocket, and other libraries.

The skip list and yyjson libraries provide high performance data structures for quant trading. Time critical code can be implemented in C++ as well for maximal speed.

### Contributing

Contributions are welcome! Open an issue or PR to improve the API wrappers, add new strategies, or otherwise enhance the project.

### License

This project is licensed under the MIT license. The C++ libctrt.so is not open sourced.

### WeChat Group

Add WeChat ID chds27 to join the quant trading discussion group.
