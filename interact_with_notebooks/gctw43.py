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
notebooks = ['https://colab.research.google.com/drive/10iXTil-0ypViaHu9qObrNlt9oGKGrV0q',
             'https://colab.research.google.com/drive/1ed5T6Dmuk2maaXTYeyiY9DgswKRXFPn9',
             'https://colab.research.google.com/drive/1V1C4dm5OnjaYfUkfSSduhmimOJ4B4DzN',
             'https://colab.research.google.com/drive/1ppN9qUXa_RIZj--H8a5l_OeNe7VUcHxl',
             'https://colab.research.google.com/drive/1RdtfoIM6svwlCU5cuVxaHX_OOAU-zMQM',
             'https://colab.research.google.com/drive/1LXMDoMfZLL1Pmz5RgqyODTCNGwp3NI0M',
             'https://colab.research.google.com/drive/1uhyZELkxsT0gi8bLXgCi0oKC-GyKK25b',
             'https://colab.research.google.com/drive/1Sm07aYhO9jcmSjAQhf5QHMKMbN_FxD4H',
             'https://colab.research.google.com/drive/1k1b-uYkfj9gXNpa-7j3inrG_xBAaW1VV']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw43.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 378, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 378, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
