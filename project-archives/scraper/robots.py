import scraper.fetcher as fetcher
import utils.url
from urllib import robotparser,parse


def robots_scraping(url_target,user_agent="*",delay=False):
    default_delay = 5

    # Memparsing url target_url dan menentukan url robots
    parse_url   = utils.url.parse_url(url_target)
    base_url    = parse_url['base_url']
    robots_url  = parse.urljoin(base_url,'robots.txt')


    robots        = robotparser.RobotFileParser(robots_url)
    robot_content = fetcher.fetch_content(robots_url)

    if robot_content:
        robots.parse(robot_content.splitlines())
    else:
        robots.read()


    can_fetch   = robots.can_fetch(useragent=user_agent,url=url_target)
    delay_time  = robots.crawl_delay(useragent=user_agent)

    if delay:
        return (delay_time+1) if delay_time else default_delay

    return can_fetch
