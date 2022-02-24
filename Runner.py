import time
from SatsScrape import SatsScrape, Day  
from pprint import pprint

if __name__ == "__main__":
    # we need to check if it is weekday or weekend
    sats_scrape = SatsScrape("chromedriver", Day.WEEKDAY)
    sats_scrape.login()
    sats_scrape.get_meal_links()
    sats_scrape.get_all_meals()
    pprint(sats_scrape.breakfast_menu)