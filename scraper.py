import requests
import yaml
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path = "config")

API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
EXCLUSIONS = ["ost", "actualite", "persos", "paroles", "episode"]

class RequestException(Exception):

    def __init__(self, response):
        message = f'''
        Status code : {response.status_code}
        Reponse text : {response.text}
        '''
        super().__init__(message)

def get_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise RequestException(response)
    return response

def get_songs(filename):
    return yaml.load(open(filename), Loader = yaml.SafeLoader)

def google_search(query):
    return get_request(f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}").json()

def fits_exclusions(string, exclusions):
    for term in exclusions:
        if term in string:
            return False
    return True

def get_url(google_response):
    for item in google_response["items"]:
        print(item["link"])
        if not fits_exclusions(item["link"], EXCLUSIONS):
            continue
        if any(map(item["link"].__contains__, ["anime", "manga"])):
            return item["link"]

def make_soup(url):
    response = get_request(url)
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding="utf-8")
    div = soup.find("div", {'class': "description", 'id': None})
    data = ""
    if div:
        for tag in div:
            data += tag.text
    return data
    
def dump_yaml(filename, data):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, allow_unicode = True)

def main():
    animes = dict()
    songs = get_songs("website/database/data.yml")
    for song in songs:
        if song["anime"] not in animes.keys():
            animes[song["anime"]] = None
            url = get_url(google_search(song["anime"]))
            if url:
                print(url)
                description = make_soup(url)
                animes[song["anime"]] = description
            
    dump_yaml("desc.yml", animes)
        
if __name__ == "__main__":
    main()            
