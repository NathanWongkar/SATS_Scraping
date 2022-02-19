# To utilize the environment variable of USER and password.
import os

# To provide a timer to make the browser wait.
import time

# Allow interaction with browser.
from selenium import webdriver

# Provide directory of webdriver.
PATH = "/Users/nathanwong/Desktop/chromedriver"

# Variable to access webdriver to allow for interaction with browser.
driver = webdriver.Chrome(PATH)

# Link for the dining hall website.
URL = "https://satscampuseats.yale-nus.edu.sg/login"

# Accessing the website.
driver.get(URL)
print(driver.title)

# Assigning the user and password from environment variables.
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')

# Presses the login button to redirect into NUS login page.
NUS_LOGIN = driver.find_element_by_class_name("jss8")
NUS_LOGIN.click()

# Finds the user and password input HTML.
user_input = driver.find_element_by_id("userNameInput")
pass_input = driver.find_element_by_id("passwordInput")

# Inputs the username and password.
user_input.send_keys(user)
pass_input.send_keys(password)

# Clicks the login button and clicks "our food".
submit_login = driver.find_element_by_id("submitButton")
submit_login.click()
our_food = driver.find_element_by_class_name("jss97")
our_food.click()

# Timer to allow website to load.
time.sleep(2)



def getting_stats(link):

    # Will access the link that is provided within the parameter.
    driver.get(link)
    # Pause to allow browser to load, if not will not be able to access
    # information.
    time.sleep(1)

    # Uses .text to retrieve the name of the food within the element
    name = driver.find_element_by_xpath('//*[@id="signup-modal-slide-description"]/div/div/div[2]/h3').text

    # Will loop 4 times to retrieve the calories, protein, carbs and fats.
    # It will then split with the condition of the space value, e.g
    # Carbohydrates: 30g becomes [Carbohydrates:, 30g] and it will only take
    # 30g and append it into stats.
    stats = []
    for i in range(1, 5):
        stat_full = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/p[" + str(i) + "]")
        stat = stat_full.text.split(" ")[-1]
        stats.append(stat)

    # This will take the calories as it will be in the form 100kcal
    # It then will traverse backwords for positions and just take the numbers
    # It then appends it again into stats.
    stats[0] = float(stats[0][:-4])

    # This will traverse the remaining nutrients Protein, Carbs and Fat and
    # remove the 'g' from each one.
    for i in range(1, 4):
        stats[i] = float(stats[i][:-1])

    # This will take the protein and divide it by the calories to get the
    # percentage and append it into the stats.
    stats.append(stats[2] / stats[0] * 100)

    # This will then create a new list called food and appened the name of
    # the food in the very front.
    food = [name] + stats
    print(food)

    return food


def finding_the_best_meal(links):
    # Creates a list to store the different foods and its stats, this will
    # become a 2d list.
    foods = []
    # Creates a list to append the best protein pcts.
    protein_pcts = []

    # This will traverse depending on the length of the links provided.
    for i in range(0, len(links)):
        # Calls the getting_stats function to get the stats of each food.
        food = getting_stats(links[i])
        # Will append the protein percentage of that food into protein_pcts.
        protein_pcts.append(food[-1])
        # Will appened the food itself into the foods list.
        foods.append(food)

    # This will find the highest protein percentage and take the index.
    best_index = protein_pcts.index(max(protein_pcts))
    # The index previously will then be used to take the stats of the highest
    # protein pct food.
    best_food = foods[best_index]

    print(best_food)
    return best_food
