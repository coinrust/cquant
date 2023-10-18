import sys
from ct import ct_init, LIBRARY


from C import LIBRARY.seq_str_str_map_new() -> cobj
from C import LIBRARY.seq_str_str_map_free(cobj) -> None
from C import LIBRARY.seq_str_str_map_set(cobj, str, str) -> bool
from C import LIBRARY.seq_str_str_map_get(cobj, str) -> str
from C import LIBRARY.seq_str_str_map_size(cobj) -> int


@tuple
class StrStrMap:
    p: cobj

    def __new__() -> StrStrMap:
        """
        创建实例
        """
        return StrStrMap(p=seq_str_str_map_new())
    
    def release(self):
        """
        释放实例
        """
        seq_str_str_map_free(self.p)
           
    def __setitem__(self, key: str, value: str):
        """
        设置 obj[key] = value
        """
        seq_str_str_map_set(self.p, key, value)
        
    def __getitem__(self, key: str):
        """
        获取 obj[key]
        """
        return seq_str_str_map_get(self.p, key)
    
    def __len__(self):
        return seq_str_str_map_size(self.p)


if __name__ == "__main__":
    ct_init()
    
    sm = StrStrMap()
    sm["a"] = "100"
    sm["b"] = "160"
    c = sm["b"]
    print(c)
    print(len(c))
    sm.release()
        
    sm1 = StrStrMap()
    sm1["a"] = "1"
    print(sm1["a"])
    sm1.release()
    sys.exit(0)
