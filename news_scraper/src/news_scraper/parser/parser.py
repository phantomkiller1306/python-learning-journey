import urllib.parse
import urllib.robotparser
import tldextract
from news_scraper.types import TargetURL,URLExtracted

def url_parser(URL: TargetURL) -> URLExtracted:
    "Extract URL to dictionary key"
    url_original = URL
    urlsplit     = urllib.parse.urlparse(url=URL)
    domain_extract = tldextract.extract(url=URL)
    
    scheme      = urlsplit.scheme
    hostname    = urlsplit.hostname
    port        = urlsplit.port
    path        = urlsplit.path
    fragment    = urlsplit.fragment
    query       = urlsplit.query
    domain      = domain_extract.domain
    subdomain   = domain_extract.subdomain
    suffix      = domain_extract.suffix
    

    return {
        "url_original": url_original,
        "scheme": scheme,
        "hostname": hostname,
        "port": port,
        "path": path,
        "fragment": fragment,
        "query": query,
        "domain": domain,
        "subdomain": subdomain,
        "suffix": suffix
    }



def robot_parser(URL: TargetURL, user_agent: str = "*", default_delay: int=3) -> dict[str,(bool|int)]:
    """
    This function parses the robot.txt file from the target URL and return a dictionary
    """
    url_extracted = url_parser(URL)
    robots = f"{url_extracted['scheme']}://{url_extracted['hostname']}/robots.txt"
    
    robot = urllib.robotparser.RobotFileParser(url=robots)
    robot.read()
    
    can_fetch = robot.can_fetch(url=URL,useragent=user_agent)

    return can_fetch



if __name__ == "__main__":
    robot_parser(b"ff")
    pass