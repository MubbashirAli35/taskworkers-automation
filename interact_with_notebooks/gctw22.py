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
notebooks = ['https://colab.research.google.com/drive/1mfbK5ZhT6RQqwVqqMaoDj_bjaHD4JI6f',
             'https://colab.research.google.com/drive/1MC8hhae3JfIg0FEx-gtJeiQNekolJ3jc',
             'https://colab.research.google.com/drive/1_S2ss-ff-3cBgvDBhZcBIu6nNfQ3717e',
             'https://colab.research.google.com/drive/1bIgqO9noGDjgKVpBM0jx-nfo8dk3BDyL',
             'https://colab.research.google.com/drive/1JUKzLhVkBlnUkwHXdJMsQg5Wb421IyOM',
             'https://colab.research.google.com/drive/1ADpMTemBYES5gzCko4ztiZsvSdL5ikGq',
             'https://colab.research.google.com/drive/1tJE2hrtx05d-1pHdTrgd7_qVohTDCaiX',
             'https://colab.research.google.com/drive/1gEDQJvtKRjx-jdI-izYZi-HPv9mpvCa7',
             'https://colab.research.google.com/drive/1ZwmI0xiHtL92LVzVqeRc62vRojO0TlpM']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw22.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 189, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 189, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    time.sleep(20)
