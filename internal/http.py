VERB_UNKNOWN = 0
VERB_DELETE = 1
VERB_GET = 2
VERB_HEAD = 3
VERB_POST = 4
VERB_PUT = 5


@tuple
class HttpResponse:
    status: int
    body: str
    
    def __new__(status: int, body: str):
        return HttpResponse(status, body)


@inline
def create_query(query_values: dict[str, str]) -> str:
    query_string = "&".join(f"{k}={v}" for k, v in query_values.items())
    return query_string
