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
notebooks = ['https://colab.research.google.com/drive/1pj7dZ8gnhDXHtN__osjXUJporF2EekCM',
             'https://colab.research.google.com/drive/1DpMhMT3yGclXQlTBBRs99QIdGxk62YTo',
             'https://colab.research.google.com/drive/1T8xsLf9tPAR_L3mMVAZKum0yN4tI29Yh',
             'https://colab.research.google.com/drive/1ADLTSfTkzwwc0mEZHDQMe78DE3JoXvhr',
             'https://colab.research.google.com/drive/1pZ-Rajd0RE5NpooVIZzU4-AAlngcb87U',
             'https://colab.research.google.com/drive/10RLCUV8Er91dX0WaTyYjroXNtyhPLd6Z',
             'https://colab.research.google.com/drive/13jMPJn46JjAIvibdogJarhbL8LY9CQ8T',
             'https://colab.research.google.com/drive/1zGPSPIjsC5gmdnToNRGkS8_w38sA6N0n',
             'https://colab.research.google.com/drive/1ueXTDeOjK02EKWuteJUtiydappf3JqpJ']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw38.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 333, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 333, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
