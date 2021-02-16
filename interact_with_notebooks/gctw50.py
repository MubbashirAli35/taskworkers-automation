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
notebooks = ['https://colab.research.google.com/drive/1U12KXsfGnlqHqP4lyRLCawYBEmIOqTd9',
             'https://colab.research.google.com/drive/13t-YiE79qub-23a4eoZsX7weA5AVQfuh',
             'https://colab.research.google.com/drive/1TG05lkJVVejF_-ctb_R2LVAx-Sg7KkCU',
             'https://colab.research.google.com/drive/1GDVzZvS-GCtDD1e9oLxY-MZVnQ3Mp3dz',
             'https://colab.research.google.com/drive/14LRzlVlLAS7sSy6hQSFkg8SHdU9D7EeX',
             'https://colab.research.google.com/drive/1UNZgd5ScERO9p3N2nZEWCzZ8ynMRsv01',
             'https://colab.research.google.com/drive/1J9vYqfxeKrisKnP6KeX2n8RJqXmC3COC',
             'https://colab.research.google.com/drive/1CiRQolCPMLMnwspDiDNRDl1uoCrHiZZK',
             'https://colab.research.google.com/drive/1RxSmoCSRdvXfBYL2lHG7BjvEMLkxElv1']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw30.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 441, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 441, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)