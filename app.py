from scraping import scraper
from webmapping import webmapper

scraper.run("scraping/rew_data.csv")
webmapper.run("scraping/rew_data.csv")