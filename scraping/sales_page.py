import requests
from bs4 import BeautifulSoup
from scraping.functions import url_builder


class SalesPage:
    def __init__(self, pg, criteria):
        self.url = url_builder(pg, *criteria)
        self.soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
        self.page = self.soup.find_all("article", {"class": "displaypanel"})

    def find_last_pg(self):
        return int(self.soup.find_all("li", {"class": "paginator-page"})[-1].text)
