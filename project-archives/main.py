from utils import url
import input.reader as reader
from models.types import PathnOrURL,URLInputType,PaginationConfig


def manual_scraping(pathname: PathnOrURL, type: URLInputType,pagination: PaginationConfig = None):
    """
    Melakukan scraping berdasarkan pathname atau url jika pagination offset-based atau cursor-based

    """

    match type:
        case 'text':
            URL_data    = reader.read_input(pathname,type='text')
            if URL_data:
                main_domain = URL_data['hostname']
                url_list    = URL_data['url_list']
                
                # Memastikan tiap url berada pada domain/situs yang sama, untuk memudahkan pencarian elemen - elemen html
                result = url.validator_input(URL_Data=url_list,hostname=main_domain)
                print(result)
            pass
        case 'json':
            print('test')
            pass
            print('test')
        case 'string':
            print('test')
            pass
            print('test')
        case _:
            print('test')
            pass

path = 'website/example-news.txt'

manual_scraping(path,type='text')
