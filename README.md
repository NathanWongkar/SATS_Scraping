# SATS_Scraping

## Installation

1. [Add Username and Password as environment variables.](https://phoenixnap.com/kb/set-environment-variable-mac) 
2. Install [Selenium](https://selenium-python.readthedocs.io/installation.html) and [webdriver].(https://chromedriver.chromium.org/downloads)
3. Install Webdriver into the project root folder.

## Project Description
1. This project aims to scrape the Yale-NUS dining hall website and send daily meals to a telegram group. We have noticed that going on the dining hall website takes a while as users will have to go through a login process. As the community uses Telegram as the main messaging platform, we have decided to try and make this process of checking today's dining hall menu a much more efficient process by bringing the message to the community. We utilized the Selenium library to interact with the web for the project. Selenium then scrapes all the available foods in today's dining menu and cleans the data. After cleaning said data, it will craft a message of the menu and use Telegram's API to send a message to a set group. The project aims to make it easier for the Yale-NUS community to know what they are eating today in a fast and quick way, avoiding the hassle of needing to go on the SATS website or go down to check.

### Disclaimer
_SATS_Scraping contain links to external websites that are not provided or maintained by us. Please note we do not guarantee the accuracy, relevance, timeliness, or completeness of any information on these external websites._
