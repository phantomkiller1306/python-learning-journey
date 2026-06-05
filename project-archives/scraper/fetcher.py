import logging
import requests
import requests_cache
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

cached_path  = Path('./cached').absolute()

def fetch_content(url_target: str, params: dict = None, delay=False):
    sessions = requests_cache.CachedSession(cached_path)

    try:
        
        response = sessions.get(url_target,params=params or {})
        
        if response.status_code == 200:
            content = response.text
            return content
        
        return None

            
    except requests.exceptions.RequestException:
        logging.info(f'Unable to connect to the server at {url_target}. Please check the URL again')
        return None