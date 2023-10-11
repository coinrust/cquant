import time
import sys
import os
from internal.dlopen import dlext
from python import os as py_os
from python import platform as py_platform

# from python import json
# from python import time as time2

# LIBRARY="/home/yl/cpp/cpt/build/linux/x86_64/release/libctrt.so"
# LIBRARY="/home/ubuntu/cpp/cpt/build/linux/arm64-v8a/release/libctrt.so"

so_file = "libctrt." + dlext()
so_path = ""
if py_os.path.exists("./" + so_file):
    so_path = "./" + so_file
else:
    architecture = py_platform.machine()
    root_path = py_os.path.dirname(py_os.getcwd())
    so_path = root_path + "/build/linux/" + architecture + "/release/" + so_file

print(so_path)

LIBRARY=so_path

# 初始化函数
from C import LIBRARY.seq_ct_init() -> int
from C import LIBRARY.seq_nanoid() -> str
# seq_hmac_encode(const char* key, const char* text)
from C import LIBRARY.seq_hmac_encode(cobj, cobj) -> str


# 设置回调
from C import LIBRARY.seq_set_seq_signal_handler(cobj) -> bool
from C import LIBRARY.seq_set_seq_alloc_atomic(cobj) -> bool


@pure
@C
def seq_alloc_atomic(a: int) -> cobj:
    pass


def fix_c_str(s: str) -> str:
    #n = strlen(t)
    t = s.c_str()
    n = s.len + 1
    p = Ptr[byte](n)
    str.memcpy(p, t, n)
    return str(p, n)


def caller(args, func):
    return func(args)


# @pure
# @C
# def seq_ct_init() -> int:
#     pass

# 设置全局标记
_shutdown_requested = False


@export
def sigint_handler(s: int):
    print(f'sigint_handler: {s}')
    global _shutdown_requested
    _shutdown_requested = True
    # sys.exit(0)

    
def shutdown_requested():
    global _shutdown_requested
    return _shutdown_requested


# 初始化
def ct_init():
    # 初始化回调
    seq_set_seq_signal_handler(sigint_handler.__raw__())
    seq_set_seq_alloc_atomic(seq_alloc_atomic.__raw__())

    seq_ct_init()
    
    
if __name__ == "__main__":
    ct_init()
    print('OK')
