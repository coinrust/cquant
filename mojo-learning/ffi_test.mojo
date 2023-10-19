import sys.ffi
import builtin.io

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


struct lib_loader:
    var handler: ffi.DLHandle

    fn __init__(inout self: Self, file: StringRef):
        self.handler = ffi.DLHandle(file, ffi.RTLD.LAZY)

    fn get[T: AnyType](inout self, key: StringRef) -> T:
        return self.handler.get_function[T](key)


fn test_so():
    # https://github.com/modularml/mojo/discussions/778
    # https://github.com/rd4com/mojo-learning
    var lib = lib_loader("../libctrt.so")
    let my_func = lib.get[fn () -> c_int]("seq_ct_init")

    # var ptr = Pointer[Int8]().alloc(5)
    let int_result = my_func()

    # print("hello "+String(ptr,5))
    print(int_result)


fn main():
    test_so()
