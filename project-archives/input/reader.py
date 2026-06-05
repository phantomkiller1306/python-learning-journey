import logging
import utils.url
from models.types import *

logging.basicConfig(level=logging.INFO,format="[%(levelname)s]: %(message)s")

def read_input(pathname: filenameOrPath, type: URLInputType) -> dict | None:
    pathname = str(pathname)
    path = Path(pathname)

    if not path.exists():
        logging.info(f'path {pathname} tidak ditemukan, silahkan periksa kembali')
        return None

    match type:
        case 'text':
            with open(pathname,mode='r',encoding='UTF-8') as file:
                content: list[str] = [line.strip() for line in file.readlines()]

            try:
                url_list    = content[1:]
                hostname    = utils.url.parse_url(content[0])['hostname']
            except IndexError:
                if not len(content) > 1:
                    logging.info(f'File dalam {pathname} minimal harus memiliki 2 baris, baris 1 untuk domain, dan 2 seterusnya berupa url')
                else:
                    logging.info(f'Domain pada baris pertama dalam {pathname} tidak ditemukan, silahkan sertakan domain pada baris pertama file itu')
                
                return None
            
        case 'json':
            print('test')
            pass
            # try:
            #     with open(pathname,mode='r',encoding='UTF-8') as file:
            #         content = json.load(fp=file)
            # except json.JSONDecodeError as e:
            #     logging.info(f'Format File {pathname} tidak valid {e}')
            return None
            
            
        case '_':
            print('test')
            logging.info("read_input argumen tipe yang diberikan tidak valid, hanya menerima 'json' dan 'text'")
            return None

    return {
        'hostname': hostname,
        'url_list': url_list
    }    
