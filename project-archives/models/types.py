import typing
from pathlib import Path


NewsSource       = typing.Literal['Kompas','Detikcom']
URLInputType     = typing.Literal['text','json','URL string']
URLInputData     : typing.TypeAlias = list[str] | dict
PathnOrURL       : typing.TypeAlias = str | Path
filenameOrPath   : typing.TypeAlias = Path | str | list[str]
# PaginationRange  : typing.TypeAlias = range


class PaginationConfig(typing.TypedDict,total=False):
    current_page : int
    max_page     : int
    query_name   : str | None

class ExtractedURL(typing.TypedDict,total=True):
    origin_url: str
    base_url: str
    scheme: str
    netloc: str
    hostname: str 
    query_string: str
    port: int
    params: dict 
    domain: str 
    subdomain: str
    suffix: str
