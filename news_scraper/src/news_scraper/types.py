import typing


TargetURL: typing.TypeAlias = str


class URLExtracted(typing.TypedDict,total=True):
    original_url: str
    scheme: str
    hostname: str
    port: int
    path: str
    fragment: str
    query: str
    domain: str
    subdomain: str 
    suffix: str