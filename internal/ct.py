from internal.dlopen import dlext

so_path = "./" + "libctrt." + dlext()

print(so_path)

LIBRARY=so_path

# 初始化函数
from C import LIBRARY.seq_ct_init() -> int
from C import LIBRARY.seq_nanoid() -> str
# seq_hmac_encode(const char* key, const char* text)
from C import LIBRARY.seq_hmac_encode(cobj, cobj) -> str


# 设置回调
from C import LIBRARY.seq_set_seq_signal_handler(cobj) -> bool

from C import LIBRARY.seq_set_seq_alloc(cobj) -> bool
from C import LIBRARY.seq_set_seq_alloc_atomic(cobj) -> bool
from C import LIBRARY.seq_set_seq_free(cobj) -> None


@pure
@C
def seq_alloc(a: int) -> cobj:
    pass


@pure
@C
def seq_alloc_atomic(a: int) -> cobj:
    pass


@nocapture
@C
def seq_free(p: cobj) -> None:
    pass


def safe_c_str(s: str) -> str:
    """
    字符串安全处理,在字符串最后添加 '\0'
    """
    #n = strlen(t)
    t = s.c_str()
    n = s.len + 1
    p = Ptr[byte](n)
    str.memcpy(p, t, n)
    return str(p, n)


def ct_init():
    """
    初始化
    """
    # 设置基础回调函数
    seq_set_seq_alloc(seq_alloc.__raw__())
    seq_set_seq_alloc_atomic(seq_alloc_atomic.__raw__())
    seq_set_seq_free(seq_free.__raw__())

    seq_ct_init()


if __name__ == "__main__":
    ct_init()
    print('OK')

