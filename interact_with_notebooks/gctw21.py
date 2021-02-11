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
notebooks = ['https://colab.research.google.com/drive/1MXbb0k8B4_bhqFOYD3BQCSsUOasWOT3S',
             'https://colab.research.google.com/drive/1_h14irfmbjNuxv5EHjZ1Z85trWglsmLf',
             'https://colab.research.google.com/drive/1AribTqKwwx66uedT4UST61KA6vLd1KWh',
             'https://colab.research.google.com/drive/1_m1O8ipd4oIPLyRKHth22mlVqHy97CTr',
             'https://colab.research.google.com/drive/14uxeiSmwpKyFIkRERU9Ok4Xd9fqcfgUN',
             'https://colab.research.google.com/drive/12qFoAH4CBMCTISHCur2wUm7BNoOmJ4WR',
             'https://colab.research.google.com/drive/1IFgfzzgg-tNyIJWqWRLj0u48NbBWdSNN',
             'https://colab.research.google.com/drive/1LcQ6LGCKmLoe9KrQMLlnG1_EAsPBUD3U',
             'https://colab.research.google.com/drive/1whHgbFVNCS8ErKKRwGAIzv0NqZm9xL2q']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw21.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 180, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 180, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
