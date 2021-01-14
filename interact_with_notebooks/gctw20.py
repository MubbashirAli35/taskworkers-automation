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
notebooks = ['https://colab.research.google.com/drive/1SfyowjMRZ1sT-GroK4nj5DY0LaZRSvzq?usp=sharing',
             'https://colab.research.google.com/drive/1F3b-8BthOvt9JfebkpBxM6Xt6ErzM1QF?usp=sharing',
             'https://colab.research.google.com/drive/1PuxTpIkaV3Cvc9pavd-MpF_KET2j2wEs?usp=sharing',
             'https://colab.research.google.com/drive/1mMN4XYzmFOMFH49ijd66WOnT4pyA1B2v?usp=sharing',
            'https://colab.research.google.com/drive/1yfv8uhmQZBZK0oFTGqHOq_sJTuKqOxRG',
            'https://colab.research.google.com/drive/1MZwp2upKkaEs4K0iGIf_FYmYAm9SKLvx',
            'https://colab.research.google.com/drive/1-iqqqLsKH4g2SyqrZ847gbicJqltkgCC',
            'https://colab.research.google.com/drive/17f0Ub2ONiKsflz8RdWhFl9FdsjlPWJwZ',
            'https://colab.research.google.com/drive/10KzADzYYXMLvXvS_WPPGZYTsnlppXudx'] 

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw20.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 171, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 171, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    time.sleep(20)
