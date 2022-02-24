from SatsScrape import SatsScrape, Day  

if __name__ == "main":
    # we need to check if it is weekday or weekend
    sats_scrape = SatsScrape("chromedriver", Day.WEEKDAY)
