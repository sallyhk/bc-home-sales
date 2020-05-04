import os
import time
import pandas
from scraping.sales_posting import HomeInfo
from scraping.sales_page import SalesPage
from scraping.functions import ask_for_criteria


def run(filepath="rew_data.csv"):
    # input parameters
    criteria = ask_for_criteria()

    # initialize
    try:
        os.remove(filepath)
    except:
        pass

    last_pg_num = SalesPage(1, criteria).find_last_pg()

    # loop through each page
    for pg_num in range(1, last_pg_num+1):
        page = SalesPage(pg_num, criteria).page

        # for each posting, fetch information of interest
        l = []
        for posting in page:
            h = HomeInfo(posting)
            d = {"Address": h.address,
                 "Latitude": h.latitude,
                 "Longitude": h.longitude,
                 "Price": h.price_str,
                 "$/sq": h.dollar_sqft,
                 "Area": h.area,
                 "Link": h.link}
            l.append(d)

        print(f"{str(pg_num)} out of {str(last_pg_num)} page(s) done!")
        time.sleep(2)
        df = pandas.DataFrame(l)

        # save each page at a time
        if pg_num == 1:
            df.to_csv(filepath)
        else:
            df.to_csv(filepath, mode='a', header=False)

