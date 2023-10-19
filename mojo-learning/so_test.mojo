from os import getenv
from sys.intrinsics import external_call
import c

# https://github.com/crisadamo/mojo-libc/blob/main/Libc.mojo

# Types aliases
alias c_void = UInt8 
alias c_char = UInt8
alias c_schar = Int8
alias c_uchar = UInt8
alias c_short = Int16
alias c_ushort = UInt16
alias c_int = Int32
alias c_uint = UInt32 
alias c_long = Int64
alias c_ulong = UInt64
alias c_float = Float32
alias c_double = Float64

# Note: `Int` is known to be machine's width 
alias c_size_t = Int
alias c_ssize_t = Int

alias ptrdiff_t = Int64
alias intptr_t = Int64
alias uintptr_t = UInt64

fn to_char_ptr(s: String) -> Pointer[c_char]:
    """only ASCII-based strings"""
    let ptr = Pointer[c_char]().alloc(len(s))
    for i in range(len(s)):
        ptr.store(i, ord(s[i]))
    return ptr


fn c_charptr_to_string(s: Pointer[c_char]) -> String:
    return String(s.bitcast[Int8](), strlen(s))

fn strlen(s: Pointer[c_char]) -> c_size_t:
    """libc POSIX `strlen` function
    Reference: https://man7.org/linux/man-pages/man3/strlen.3p.html
    Fn signature: size_t strlen(const char *s)

    Args:
    Returns:
    """
    return external_call["strlen", c_size_t, Pointer[c_char]](s)

# print(getenv("PATH"))
# print(getenv(StringRef("PATH")))

fn getpid() -> c.int:
    return external_call["getpid", c.int]()

fn seq_ct_init() -> c_int:
    return external_call["ctrt.seq_ct_init", c_int]()

import sys.ffi
import builtin.io

struct lib_loader:
    var handler:ffi.DLHandle

    fn __init__(inout self: Self, file: StringRef):
        self.handler = ffi.DLHandle(file,ffi.RTLD.LAZY)

    fn get[T:AnyType](inout self,key:StringRef) -> T:
        return self.handler.get_function[T](key)

fn test_so():
    # https://github.com/modularml/mojo/discussions/778
    # https://github.com/rd4com/mojo-learning
    var lib = lib_loader("./libctrt.so")
    var my_func = lib.get[fn()->c_int]("seq_ct_init")

    # var ptr = Pointer[Int8]().alloc(5)
    var int_result = my_func()

    # print("hello "+String(ptr,5))
    print(int_result)


fn main():
    print(getenv("PATH"))
    print("1")
    print(100)
    let pid = getpid()
    print(pid)
    # let s = to_char_ptr("/home/yl/py/cquant/libctrt.so")
    # let handle = dlopen(s, 0)
    # print("100")
    # let c_ret = dlclose(handle)
    # print("101")
    # print(c_ret)
    # let x = seq_ct_init()
    # print(x)
    test_so()


# # or like this
# # from SIMD import SI8
# from intrinsics import external_call

# var path1 = external_call["getenv", StringRef](StringRef("PATH"))
# print(path1.data)

# var path2 = external_call["getenv", StringRef]("PATH")
# print(path2.data)

# let abs_10 = external_call["abs", SI8, Int](-10)
# print(abs_10)