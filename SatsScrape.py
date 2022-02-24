import os
import time
import sys
from matplotlib.cbook import get_sample_data
from selenium import webdriver
import requests
from enum import Enum
import re
from pathlib import Path


class Day(Enum):
    WEEKDAY = 1
    WEEKEND = 2

class SatsScrape:
    def __init__(self, webdriver_name: str, day: Day) -> None:
        '''
        Initialising the SatsScrape. Accessing the website.
        input:
            webdriver <str>: path to webdriver.
            day <Day>: An indication whether that day is weekday or weekend.
        '''
        print("initialising webdriver...")
        print("-----------------")
        project_root = Path(__file__).parent
        webdriver_path = str(project_root) + "/" + str(webdriver_name)
        self.URL = "https://satscampuseats.yale-nus.edu.sg/login"
        self.driver = webdriver.Chrome(webdriver_path)
        self.user = os.environ.get('USER')
        self.password = os.environ.get('PASSWORD')
        self.day = day
        self.nutrition = ["calories", "protein", "carbs", "fats"]
        # meal links
        if day == Day.WEEKDAY:
            self.breakfast_links = []
            self.breakfast_menu = []
            self.lunch_links = []
            self.lunch_menu = []
        else:
            self.brunch_links = []
            self.brunch_menu = []
        self.dinner_links = []
        self.dinner_menu = []
        print("done")
        print("-----------------")
    
    def login(self) -> None:
        '''
        Login to the website.
        '''
        print("Logging in")
        print("--------------")
        self.driver.get(self.URL)
        self.driver.find_element_by_class_name("jss8").click()
        self.driver.find_element_by_id("userNameInput").send_keys(self.user)
        self.driver.find_element_by_id("passwordInput").send_keys(self.password)
        # click login button
        self.driver.find_element_by_id("submitButton").click()
        print("Logged in")
        print("--------------")

    def get_meal_links(self) -> None:
        '''
        Get all the meal links available and append them to the meal links list.
        The meal links depend on the day when class is initialised.
        '''
        print("Getting meal links")
        print("--------------")
        # click "our food"
        self.driver.find_element_by_class_name("jss97").click()
        time.sleep(2)
        if self.day == Day.WEEKDAY:
            print("weekday:")
            for i in range(1, 5):
                # breakfast
                if i < 4:
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
            for i in range(1, 5):
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
    
    def get_stats(self, link: str) -> "dict[str: str, str: float, str:float, str:float, str:float]":
        '''
        Get all the stats from a specified meal.
        input:
            link <str>: the link to the meal
        output:
            stats <dict>: dictionary of name, calories, protein, carbs, and fats.
        '''
        self.driver.get(link)
        time.sleep(1)
        name = self.driver.find_element_by_xpath('//*[@id="signup-modal-slide-description"]/div/div/div[2]/h3').text
        stats = {"name": name}
        for i in range(1, 5):
            stat_full = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/p["+str(i)+"]")
            stat_str = stat_full.text.split(" ")[-1]
            stat_float = float(re.findall(r'\d+', stat_str)[0])
            stats[self.nutrition[i - 1]] = stat_float
        return stats
    
    def get_all_meals(self):
        '''
        Getting all the meals (name, calories, protein, carbs, and fats) and append them into a list.
        The information is stored in the state.
        '''
        if self.day == Day.WEEKDAY:   
            for i in range(4):
                if i < 3:
                    self.breakfast_menu.append(self.get_stats(self.breakfast_links[i]))
                self.lunch_menu.append(self.get_stats(self.lunch_links[i]))
                self.dinner_menu.append(self.get_stats(self.dinner_links[i]))
        else:
            for i in range(4):
                self.brunch_menu.append(self.get_stats(self.brunch_links[i]))
                self.dinner_menu.append(self.get_stats(self.dinner_links[i]))
    



