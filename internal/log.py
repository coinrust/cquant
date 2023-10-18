from ct import LIBRARY

# 日志函数
# SEQ_FUNC void seq_init_log(const char *min_severity,
#                            const std::string &filename = "", bool async = true,
#                            bool enable_console = true, size_t max_file_size = 0,
#                            size_t max_files = 0,
#                            bool flush_every_time = false)
from C import LIBRARY.seq_init_log(cobj, cobj, bool, bool, int, int, bool) -> None
# SEQ_FUNC void seq_logvd(const char* s, size_t sLen);
from C import LIBRARY.seq_logvd(cobj, int) -> None
# SEQ_FUNC void seq_logvi(const char* s, size_t sLen);
from C import LIBRARY.seq_logvi(cobj, int) -> None
# SEQ_FUNC void seq_logvw(const char* s, size_t sLen);
from C import LIBRARY.seq_logvw(cobj, int) -> None
# SEQ_FUNC void seq_logve(const char* s, size_t sLen);
from C import LIBRARY.seq_logve(cobj, int) -> None


def init_log(level: str="INFO", filename: str="", async_: bool=True, \
             enable_console: bool=True, max_file_size: int=0, max_files: int=0, flush_every_time: bool=False):
    seq_init_log(level.ptr, filename.ptr, async_, enable_console, max_file_size, max_files, flush_every_time)


def logvd(s: str):
    seq_logvd(s.ptr, s.len)


def logvi(s: str):
    seq_logvi(s.ptr, s.len)


def logvw(s: str):
    seq_logvw(s.ptr, s.len)


def logve(s: str):
    seq_logve(s.ptr, s.len)
