import requests
from bs4 import BeautifulSoup
import os

WIKI_URL="https://temtem.wiki.gg"
DATA_FOLDER="data"

if not os.path.exists(DATA_FOLDER):
    os.mkdir(DATA_FOLDER)

def get_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")

def save(name, data):
    with open(os.path.join(DATA_FOLDER, name), "w+") as f:
        f.write(data)
