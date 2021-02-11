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
notebooks = ['https://colab.research.google.com/drive/1pl_Vu3NffFS8-TRnqWMXIyTef24mIPYC',
             'https://colab.research.google.com/drive/1P5cMqFtssivbDfEJBaDjMYwuVi_wbIVe',
             'https://colab.research.google.com/drive/1imPXtL0xM5ETStXVkVbl6MZyHW5PPZR4',
             'https://colab.research.google.com/drive/1wnL-4pJXT1v9hgqbi72dEEdZ5E6q-7E0',
             'https://colab.research.google.com/drive/1A1JFP_GtDtkx9kCbM-KJFUgeNRUZUzR2',
             'https://colab.research.google.com/drive/1iMAaBsm9R5LZxolpvXi5cjxDLUT4REHP',
             'https://colab.research.google.com/drive/1KLiA7B_ZWwJJ642VADwRne-pWSb2WkZH',
             'https://colab.research.google.com/drive/111Oq1wq21JaC0pvpZWoAtFqPJmpxb2S4',
             'https://colab.research.google.com/drive/111vev3_dZj84mH70ZyW3hIEYJGBwif7v']
i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('../cookies/cookies_gctw44.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw20.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 387, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 387, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
