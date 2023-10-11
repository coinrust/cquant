## 基于 Codon 的量化交易系统精要

这是一个使用 Codon,Python 和 C++ 开发的开源量化交易系统。其中包括:

* Bybit API 封装,用于下单 (bybit_api.py)
* Bybit websocket,用于获取市场数据 (bybit_ws.py)
* 固定价格跳表数据结构 (foundation.py)
* 使用 yyjson 的快速 JSON 解析 (yyjson.py)
* C++ 基础架构,用于获得高性能 (libctrt.so - 没有开源)

### 需求

* Python 3.11+
* Codon 运行时
* Bybit 账户和 API 密钥

### 使用

导出 Codon Python 库路径:

```shell
export CODON_PYTHON=/path/to/libpython3.11.so
```

使用 Codon 运行策略:

```shell
codon run -release foundation.py
```

使用 Python 实现您的交易策略。可以利用 Bybit API 封装、websocket 和其他库。

跳表和 yyjson 库提供了高性能的数据结构用于量化交易。时间关键的代码也可以用 C++ 实现以获得最大速度。

### 贡献

欢迎贡献!打开 Issue 或 PR 来改进 API 封装、添加新的策略、或者其他方式增强项目。

### 许可证

该项目使用 MIT 许可证。C++ libctrt.so 没有开源。

### 微信交流群

请联系我加入微信群: chds27
