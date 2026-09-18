import requests
import pathlib

def fetch_raw_schedule(url: str):
    domain = url.split("/")[2]
    temp_file = pathlib.Path(f"{domain}.html")

    if temp_file.exists():
        with temp_file.open() as f:
            content = f.read()
        return content

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.ConnectionError:
        return None
        

    if response.status_code != 200:
        print(" FAIL TO GET RAW SCHEDULE ")
        return None

    
    

def main():
    fetch_raw_schedule("https://www.an.tv/schedule")


if __name__ == "__main__":
    main()