import urllib.parse
import tldextract
from models.types import ExtractedURL,URLInputData




def parse_url(url: str) -> ExtractedURL:
    
    """
    Menguraikan url menjadi 8 bagian dan mengembalikan sebuah dictionary, dengan bagian bagiannya:
    - origin_url
    - base_url
    - scheme
    - netloc
    - hostname
    - query_string
    - port
    - params
    """
    parser    = urllib.parse.urlparse(url=url)
    extracted = tldextract.extract(url=url)
    
    scheme      = parser.scheme
    netloc      = parser.netloc
    hostname    = parser.hostname
    base_url    = f"{scheme}://{hostname}"
    query_str   = parser.query
    port        = parser.port
    params      = urllib.parse.parse_qs(query_str)
    
    subdomain   = extracted.subdomain
    domain      = extracted.domain
    suffix      = extracted.suffix

    return {
        'origin_url': url,
        'base_url': base_url,
        'scheme': scheme,
        'netloc': netloc,
        'hostname': hostname,
        'query_string': query_str,
        'port': port,
        'params': params,
        'domain': domain,
        'subdomain': subdomain,
        'suffix': suffix
    }


def validator_input(URL_Data: URLInputData,hostname: str):
    data_type = type(URL_Data).__name__
    
    def check(url):
        comparison = parse_url(url)['hostname'] == hostname
        return comparison

    match data_type:
        case 'list':
            valid_url = [url for url in URL_Data if check(url)]
            return valid_url

        case 'dict':
            pass
        case 'str':
            pass
    pass