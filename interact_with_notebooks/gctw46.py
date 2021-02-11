from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pickle
import pandas as pd
import sys

# Reads configuration from the CSV about which notebooks to run for a particular worker
notebooks_config = pd.read_csv('../' + sys.argv[1])

# Adds configuration to the chromedriver
options = Options()
options.add_argument('headless')    # Configures to start chrome in headless mode
options.add_argument('--start-maximized')   # Configures to start it with maximum window size

# Adds a specific User Agent
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

# List of Notebooks' URLs for this particular task worker
notebooks = ['https://colab.research.google.com/drive/1SGz4wjwljumw-wpS5KY4RQmdwrtVLepo',
             'https://colab.research.google.com/drive/1Y6YYpiUR_eNKjiK3VloQKQWacd8CYwht',
             'https://colab.research.google.com/drive/1jRFnmUUTks60fHQw3Rh9YulFBK7KAQ1v',
             'https://colab.research.google.com/drive/1iwk8m6y18_XPWgkx4OhamyixvC7XAtk_',
             'https://colab.research.google.com/drive/1nsF7_g3vwP5gExd2o1sv-LN0CFEY_-2J',
             'https://colab.research.google.com/drive/1ScLIwJ3G49pDfRcBgFdqGJyu4yn75RBs',
             'https://colab.research.google.com/drive/1vfa1hEEz4vGzUvI7IDJLFiJCcE06xtrG',
             'https://colab.research.google.com/drive/1CYvsVKkzyGOjHhv0qk9WidviUuE1oC3z',
             'https://colab.research.google.com/drive/1cIoSj6jfT9l1Jt3JO9FhsS1kAwFep7p8']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw46.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 345, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 345, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
