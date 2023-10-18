import time
from ct import LIBRARY, ct_init


@tuple
class Fixed:
    fp: int


# SEQ_FUNC fixed_12_t fixed_12_new()
from C import LIBRARY.fixed_12_new() -> Fixed
# SEQ_FUNC fixed_12_t fixed_12_new_int(int64_t value)
from C import LIBRARY.fixed_12_new_int(int) -> Fixed
# SEQ_FUNC fixed_12_t fixed_12_new_double(double value)
from C import LIBRARY.fixed_12_new_double(float) -> Fixed
# SEQ_FUNC fixed_12_t fixed_12_new_string_n(const char* cstr, size_t len)
from C import LIBRARY.fixed_12_new_string_n(cobj, int) -> Fixed
# SEQ_FUNC fixed_12_t fixed_12_new_string(const char* cstr)
from C import LIBRARY.fixed_12_new_string(cobj) -> Fixed
# SEQ_FUNC seq_str_t fixed_12_string(const fixed_12_t &fixed)
from C import LIBRARY.fixed_12_string(Fixed) -> str
# SEQ_FUNC size_t fixed_12_string_res(const fixed_12_t &fixed, char *result)
from C import LIBRARY.fixed_12_string_res(Fixed, Ptr[byte]) -> int

# SEQ_FUNC skiplist_t *seq_skiplist_new(bool isForward);
from C import LIBRARY.seq_skiplist_new(bool) -> cobj
# SEQ_FUNC void seq_skiplist_delete(skiplist_t *list);
from C import LIBRARY.seq_skiplist_delete() -> None
# SEQ_FUNC bool seq_skiplist_insert(skiplist_t *list, int64_t key, int64_t value);
from C import LIBRARY.seq_skiplist_insert(cobj, int, int) -> bool
# SEQ_FUNC int64_t seq_skiplist_remove(skiplist_t *list, int64_t key);
from C import LIBRARY.seq_skiplist_remove(cobj, int) -> int
# SEQ_FUNC int64_t seq_skiplist_search(skiplist_t *list, int64_t key);
from C import LIBRARY.seq_skiplist_search(cobj, int) -> int
# SEQ_FUNC void seq_skiplist_dump(skiplist_t *list);
from C import LIBRARY.seq_skiplist_dump(cobj) -> None

# from C import LIBRARY.test_main() -> int
from C import LIBRARY.test_skiplistx() -> int


@extend
class Fixed:
    """
    最小值:      0.0
    精度:        0.000000000001
    最大值: 999999.999999999999
    """
    def __new__():
        return Fixed(0)
    
    def __new__(s: str):
        return fixed_12_new_string_n(s.ptr, s.len)
    
    def __new__(f: float):
        # return fixed_12_new_double(f)
        return Fixed(fp=int(f * 1000000000000))
    
    def __bool__(self) -> bool:
        return self.fp != 0
    
    def __eq__(self, other: Fixed) -> bool:
        return self.fp == other.fp
    
    def __ne__(self, other: Fixed) -> bool:
        return self.fp != other.fp
    
    def __gt__(self, other: Fixed) -> bool:
        return self.fp > other.fp
    
    def __ge__(self, other: Fixed) -> bool:
        return self.fp >= other.fp
    
    def __lt__(self, other: Fixed) -> bool:
        return self.fp < other.fp
    
    def __le__(self, other: Fixed) -> bool:
        return self.fp <= other.fp
    
    def __add__(self, other: Fixed) -> Fixed:
        return Fixed(fp=self.fp + other.fp)

    def __sub__(self, other: Fixed) -> Fixed:
        return Fixed(fp=self.fp - other.fp)

    def __mul__(self, other: Fixed) -> Fixed:
        return Fixed((self.fp / 1000000000000) * (other.fp / 1000000000000))
    
    def __div__(self, other: Fixed) -> Fixed:
        return Fixed((self.fp / 1000000000000) / (other.fp / 1000000000000))
    
    def __truediv__(self, other: Fixed):
        return Fixed((self.fp / 1000000000000) / (other.fp / 1000000000000))
    
    def __floordiv__(self, other: Fixed):
        return Fixed((self.fp // 1000000000000) // (other.fp // 1000000000000))
    
    def str(self) -> str:
        n = 16
        p = Ptr[byte](n)
        len = fixed_12_string_res(self, p)
        return str(p, len)
    
    def __repr__(self) -> str:
        return f"<Fixed: fp={self.fp}, str={self.str()}>"


@tuple
class SkipList:
    p: cobj
    
    def __new__(is_orward: bool):
        """
        is_orward: true-正序，从小到到 false 反序，从大到小
        """
        return SkipList(p=seq_skiplist_new(is_orward))
    
    def release(self):
        seq_skiplist_delete(self.p)
    
    @inline
    def insert(self, price: Fixed, qty: Fixed) -> bool:
        """
        update_if_exists
        """
        return seq_skiplist_insert(self.p, price.fp, qty.fp)
    
    @inline
    def search(self, price: Fixed) -> Fixed:
        return Fixed(fp=seq_skiplist_search(self.p, price.fp))
    
    @inline
    def remove(self, price: Fixed) -> Fixed:
        return Fixed(fp=seq_skiplist_remove(self.p, price.fp))
    
    def dump(self):
        seq_skiplist_dump(self.p)
    
    
if __name__ == "__main__":
    ct_init()
    
    f = Fixed(0)
    print(f)
    g = Fixed("3.15")
    print(g)
    print(g.str())
    print(g)
    a = Fixed("5.3")
    b = Fixed("3.5")
    c = a + b
    print(c.str())
    d = a - b
    print(d.str())
    print(a + b + Fixed("91.51515"))
    print(Fixed(3.55151))
    print(a == b)
    print(a != b)
    print(a * b)
    print(a / b)
    print(a // b)
    
    # test_main()
    
    bids = SkipList(True)
    # bids.dump()
    bids.insert(Fixed(2.1), Fixed(4.0))
    bids.insert(Fixed(2.2), Fixed(4.0))
    bids.insert(Fixed(2.5), Fixed(4.0))
    bids.insert(Fixed(2.6), Fixed(10.0))
    bids.insert(Fixed(2.3), Fixed(10.0))
    bids.insert(Fixed(2.4), Fixed(11.0))
    bids.insert(Fixed(2.4), Fixed(12.0))
    bids.remove(Fixed(2.3))
    print('dump:')
    bids.dump()
    print('dump.')
    
    value = bids.search(Fixed(2.5))
    print('value: ', value)

    num_runs = 10000000
    
    key = Fixed(2.3)
    value = Fixed(10.0)

    bids1 = SkipList(True)
    
    start_time = time.time()  # 获取开始时间
    
    for _ in range(num_runs):
        bids1.insert(key, value)
        bids1.remove(key)

    end_time = time.time()  # 获取结束时间
    total_time = (end_time - start_time) * 1e9  # 累加运行时间，并将其转换为纳秒

    # 计算平均耗时
    average_time = total_time / num_runs
    print(f'Average time is {average_time} ns.')
    
    # test_skiplistx()
    