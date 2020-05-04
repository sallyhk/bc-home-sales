from scraping.functions import do_geocode
import re


class HomeInfo:
    def __init__(self, posting):
        self.address = posting.find("a")["title"][:-13]
        self.unitless_address = self.address[self.address.find("-")+1:]
        self.postal_code = posting.find("a")["title"][-7:]

        geo = self.location()
        self.latitude = geo.latitude if geo else None
        self.longitude = geo.longitude if geo else None

        self.price_str = posting.find("div", {"class": "displaypanel-title hidden-xs"}).text.replace("\n", "")
        self.price = int(self.price_str.replace("$", "").replace(",", ""))
        info = [i.text for i in posting.find("div", {"class": "displaypanel-section clearfix"}).find_all("li")]
        self.bed = int(re.search("([0-9]+)\sbd", info[0])[1])
        self.bath = int(re.search("([0-9]+)\sba", info[1])[1])
        self.area = int(re.search("([0-9]+)\ssf", info[2])[1])
        self.dollar_sqft = round(self.price / self.area)
        self.link = "rew.ca" + posting.find("div", {"class": "displaypanel-body"}).find("a", href=True)["href"]

    def location(self):
        g = do_geocode(self.unitless_address)
        if g is None:
            g = do_geocode(self.postal_code)
        if g is None:
            g = do_geocode(self.postal_code[:3])
        if g is None:
            return None
        return g