# To utilize the environment variable of USER and password.
import os

# To provide a timer to make the browser wait.
import time

# To be able to use the browser and access links.
import requests

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

# takes all BRUNCH FOOD links.

brunch_links = []

# Breakfast on weekdays will have exactly 4 meals, it will go through each
# link using the for loop. To take the element it uses the xpath and since
# each meal have similar xpaths and only an increment on the last div, we
# just change that number. It then appends the link into b_fast links.
for i in range(1, 5):
    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[' + str(i) + ']/a'
    element = driver.find_element_by_xpath(xpath)
    # print(element.get_attribute('href'))
    brunch_links.append(element.get_attribute('href'))

# Takes all Dinner food links.

dinner_links = []


# The logic here is similar to breakfast, but lunch will have 4 meals instead
# of 3, hence it will run through 1 until 5. Another thing that differs is the
# xpath for the lunch division. The 3rd to last div is incremented by 1.
for i in range(1, 5):
    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[3]/div/div[2]/div/div['+ str(i) +']/a'
    element = driver.find_element_by_xpath(xpath)
    # print(element.get_attribute('href')) TO check if the link is printed
    dinner_links.append(element.get_attribute('href'))

# This function will click each link and retrieve the nutrient and name for
# each food.


def getting_stats(link):

    # Will access the link that is provided within the parameter.
    driver.get(link)
    # Pause to allow browser to load, if not will not be able to access
    # information.
    time.sleep(1)
    # Uses .text to retrieve the name of the food within the element.
    name = driver.find_element_by_xpath('//*[@id="signup-modal-slide-description"]/div/div/div[2]/h3').text
    print(name)

    # Will loop 4 times to retrieve the calories, protein, carbs and fats.
    # It will then split with the condition of the space value, e.g
    # Carbohydrates 30g becomes [Carbohydrates:, 30g] and it will only take
    # 30g and append it into stats.
    stats = []
    for i in range(1, 5):
        stat_full = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/p["+str(i)+"]")
        stat = stat_full.text.split(" ")[-1]
        stats.append(stat)
    print(stats)

    # This will take the calories as it will be in the form 100Kcal
    # It then will traverse backwords for positions and just take the numbers
    # It then appends it again into stats
    print(stats[0])
    stats[0] = float(stats[0][:-4])
    print(stats[0])

    # This will traverse the remaining nutrients Protein, Carbs and Fat and
    # remove the 'g' from each one
    for i in range(1, 4):
        stats[i] = float(stats[i][:-1])
# This will take the protein and divide it by the calories to get the
# percentage and append it into the stats
    stats.append(stats[2] / stats[0] * 100)
    food = [name] + stats
    print(food)
    return food


# This function will traverse the list of foods for each meal and find the
# highest protein percentage.


def finding_the_best_meal(links):
    # Creates a list to store the different foods and its stats, this will
    # become a 2d list.
    foods = []
    # Creates a list to append the best protein pcts.
    protein_pcts = []

    # This will traverse depending on the length of the links provided
    for i in range(0, len(links)):
        # Calls the getting_stats function to get the stats of each food
        food = getting_stats(links[i])
        # Will append the protein percentage of that food into protein_pcts
        protein_pcts.append(food[-1])
        # Will appened the food itself into the foods list
        foods.append(food)

    # This will find the highest protein percentage and take the index
    best_index = protein_pcts.index(max(protein_pcts))
    # The index previously will then be used to take the stats of the highest
    # protein pct food.
    best_food = foods[best_index]

    print(best_food)
    return best_food


# List to show off the best food for each meal
best_foods = []

# This will call the finding best meal and append it into the best.
# foods function.
best_foods.append(finding_the_best_meal(brunch_links))
best_foods.append(finding_the_best_meal(dinner_links))

# Calculate the sum of calories, carbs, protein and fats.
total_calories = (best_foods[0][1]) + (best_foods[1][1])
total_carb = (best_foods[0][2]) + (best_foods[1][2])
total_protein = (best_foods[0][3]) + (best_foods[1][3])
total_fat = (best_foods[0][4]) + (best_foods[1][4])

# Creating the message to send to Telegram.
message = f"""
*BRUNCH:*
_{best_foods[0][0]}_ with {str(best_foods[0][1])}kcal and {str(best_foods[0][3])}g of protein.
*DINNER:*
_{best_foods[1][0]}_ with {str(best_foods[1][1])}kcal and {str(best_foods[1][3])}g of protein.

*TOTAL STATS*
Total Calories: {total_calories}kcal
Total Carbohydrate: {total_carb}g
Total Protein: {total_protein}g
Total Fat: {total_fat}g
"""

# Replacing the character & with %26 which is & as & is used to declare the
# beginning of an entity reference (a special character).
message = message.replace("&", "%26")

# print(message)

# Appending the message to the link that the telegram bot will send.
message_url = 'https://api.telegram.org/bot5190481628:AAHvjriOdIz_TvR15Q5p39WtAgtF_w7ravU/sendMessage?chat_id=-794849324&parse_mode=Markdown&text=' + message

# Requesting the link which will send the message to the designated group.
requests.get(message_url)
