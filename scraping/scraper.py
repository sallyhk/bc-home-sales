import os
import time
import pandas
from scraping.sales_posting import HomeInfo
from scraping.sales_page import SalesPage
from scraping.functions import ask_for_criteria


def run(filepath="rew_data.csv"):
    # initialize
    try:
        os.remove(filepath)
    except:
        pass

    # gather all input values first
    n = int(input("How many cities to search for? "))
    criteria_list = []
    for city_num in range(n):
        criteria_list.append(ask_for_criteria(city_num+1))

    # loop through each city
    for i in range(len(criteria_list)):
        criteria = criteria_list[i]

        print(f"\nScraping for City #{str(i+1)} {criteria} criteria...")
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
                     "Bed": h.bed,
                     "Bath": h.bath,
                     "Link": h.link}
                l.append(d)

            print(f"{str(pg_num)} out of {str(last_pg_num)} page(s) done!")
            time.sleep(2)
            df = pandas.DataFrame(l)

            # save each page at a time
            if i == 0 and pg_num == 1:
                df.to_csv(filepath, header=True)
            else:
                df.to_csv(filepath, mode='a', header=False)

