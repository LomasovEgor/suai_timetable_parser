import bs4
import requests
from abc import ABC


class Parser(ABC):
    """Makes a request and creates a soup object"""

    def __init__(self, url):
        self.url: str = url
        self.request: requests.Request | None = None
        self.soup: bs4.BeautifulSoup | None = None
        self.result: dict | list | None = None

    def run(self):
        pass

    def save(self):
        pass
