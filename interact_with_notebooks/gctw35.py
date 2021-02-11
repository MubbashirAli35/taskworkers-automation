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
notebooks = ['https://colab.research.google.com/drive/1TnT2ItyYZepZ1ZCNArIFE494KfyriiD9',
             'https://colab.research.google.com/drive/1i-mFW36sbt4HPXY-NnppWuh4WRUGkIWP',
             'https://colab.research.google.com/drive/1g5t7e2yezMF6hyTbD74JU_4y_kJWfSt7',
             'https://colab.research.google.com/drive/1miOfiB2XPqN5Lw39P8IjdNG99nAqyZLY',
             'https://colab.research.google.com/drive/1p0mIA8-SVmjulVlL8NuvIrnR85AXzP0w',
             'https://colab.research.google.com/drive/1BQhXShJw1KPMBU5-OWilFKFzhjjAphp4',
             'https://colab.research.google.com/drive/109pLG3KzY6xmuA5HDerFJyXcQ0iH1L3g',
             'https://colab.research.google.com/drive/10_GE-jfTBSVA52FHzR-zeaL-m3ydsa7b',
             'https://colab.research.google.com/drive/1phEqv8G7B7p7h8OUX55hVK3trSx5cfh9']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw35.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 306, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 306, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
