import os
import time
import sys
from selenium import webdriver
import requests
from enum import Enum
import regex as re

class Day(Enum):
    WEEKDAY = 1
    WEEKEND = 2

class SatsScrape:
    def __init__(self, webdriver_path: str, day: Day) -> None:
        '''
        Initialising the SatsScrape. Accessing the website.
        input:
            webdriver <str>: path to webdriver.
            day <Day>: An indication whether that day is weekday or weekend.
        '''
        self.URL = "https://satscampuseats.yale-nus.edu.sg/login"
        self.driver = webdriver.Chrome(webdriver_path)
        self.user = os.environ.get('USER')
        self.password = os.environ.get('PASSWORD')
        self.day = day
        self.nutrition = ["calories", "protein", "carbs", "fats"]
        self.breakfast_links = []
        self.brunch_links = []
        self.lunch_links = []
        self.dinner_links = []
    
    def login(self) -> None:
        '''
        Login to the website.
        '''
        self.driver.get(self.URL)
        self.driver.find_element_by_class_name("jss8").click()
        self.driver.find_element_by_id("userNameInput").send_keys(self.user)
        self.driver.find_element_by_id("passwordInput").send_keys(self.password)
        # click login button
        self.driver.find_element_by_id("submitButton").click()
        # click "our food"
        self.driver.find_element_by_class_name("jss97").click()
        time.sleep(2)

    def get_meal_links(self) -> None:
        '''
        Get all the meal links available and append them to the meal links list.
        The meal links depend on the day when class is initialised.
        '''
        if self.day == Day.WEEKDAY:
            for i in range(4):
                # breakfast
                if i < 3:
                    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[' + str(i) + ']/a'
                    element = self.driver.find_element_by_xpath(xpath)
                    self.breakfast_links.append(element.get_attribute('href'))
                # lunch
                xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[3]/div/div[2]/div/div[' + str(i) + ']/a'
                element = self.driver.find_element_by_xpath(xpath)
                self.lunch_links.append(element.get_attribute('href'))
                # dinner
                xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[4]/div/div[2]/div/div[' + str(i) + ']/a'
                element = self.driver.find_element_by_xpath(xpath)
                self.dinner_links.append(element.get_attribute('href'))
        elif self.day == Day.WEEKEND:
            for i in range(4):
                # brunch
                xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[' + str(i) + ']/a'
                element = self.driver.find_element_by_xpath(xpath)
                self.brunch_links.append(element.get_attribute('href'))
                # dinner
                xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[3]/div/div[2]/div/div['+ str(i) +']/a'
                element = self.driver.find_element_by_xpath(xpath)
                self.dinner_links.append(element.get_attribute('href'))
        else:
            print("ERROR: meal links are not found.")
            sys.exit()
    
    def get_stats(self, link: str) -> dict[str: float, str:float, str:float, str:float]:
        '''
        Get all the stats from a specified meal.
        input:
            link <str>: the link to the meal
        output:
            stats <dict>: dictionary of calories, protein, carbs and fats.
        '''
        
        self.driver.get(link)
        time.sleep(1)
        name = self.driver.find_element_by_xpath('//*[@id="signup-modal-slide-description"]/div/div/div[2]/h3').text

        stats = {"name": name}
        for i in range(4):
            stat_full = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/p["+str(i)+"]")
            stat_str = stat_full.text.split(" ")[-1]
            stat_float = float(re.findall(r'\d+', stat_str)[0])
            stats[self.nutrition[i]] = stat_float
        return stats



