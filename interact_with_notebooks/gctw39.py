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
notebooks = ['https://colab.research.google.com/drive/1HLgNVOvzfQLfjKT4fTzqwb0iNieEdOXT',
             'https://colab.research.google.com/drive/1B-WHrGwObVz-mgbi06Ym_PRA_rsjCdKf',
             'https://colab.research.google.com/drive/1wGAqfi4Je0bMbtK9HpQA7qvkOlD5h6Bb',
             'https://colab.research.google.com/drive/1vEAY2lygueHAT4Xvw9iQ61VLVum-PAOM',
             'https://colab.research.google.com/drive/11wY0HIDqbVa-khnAEqgd-y7PzcAUzjQY',
             'https://colab.research.google.com/drive/1vcCLloeXa86-_ADDpHeCAOjECU56-omH',
             'https://colab.research.google.com/drive/1D_iUn80-Ent5UvmnlXfENf5UHXZv7tUf',
             'https://colab.research.google.com/drive/1j4z_rAB4ibdAuqRYpt9jstDpVdnL1SX3',
             'https://colab.research.google.com/drive/1EhRkXpeuR-A3-K2r83f0QpWF5zvbrpX7']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw39.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 342, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 342, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    time.sleep(20)
