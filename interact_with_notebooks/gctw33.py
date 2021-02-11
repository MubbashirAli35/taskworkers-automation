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
notebooks = ['https://colab.research.google.com/drive/1xfKSaqCy8vk7zOCVD2dLE8R7ESO2XFQx',
             'https://colab.research.google.com/drive/1yPHw1islmzRM54AC5GyiHdsIU4wQuhY-',
             'https://colab.research.google.com/drive/1dObnyEZYAmgNg1a4YYO4618v8fWGje6X',
             'https://colab.research.google.com/drive/1S0s7utIGqbImc7thWYuZt7G7vnpNqj85',
             'https://colab.research.google.com/drive/1SnTevTzC-7ntn5iNHcJUQ7pJ8peYjFaa',
             'https://colab.research.google.com/drive/1V19k8GLfF4BtiPKusV9-faSOl5eCxEx4',
             'https://colab.research.google.com/drive/1f8QrZKDQvcA5jMoQp4Y6rYfQCKu4uCJQ',
             'https://colab.research.google.com/drive/1dH8vRkCIQIn3mED1V_JqF9h0SS-l_kV1',
             'https://colab.research.google.com/drive/14X4nPRtaPxlLMCkCVAb9odmG8rNeF38l']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw33.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 288, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 288, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
