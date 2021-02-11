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
notebooks = ['https://colab.research.google.com/drive/122rbuFnSDVJhfnwnCrafh6fb81XrlPtp',
             'https://colab.research.google.com/drive/1_ocU9Cd9wN-tIpOy04D9pw--9JYP3F2a',
             'https://colab.research.google.com/drive/1BcJfnYYiG4HCzBgpl2FmwAFWnUQab-GJ',
             'https://colab.research.google.com/drive/193J4PfkytMTQ2oU9TIuRVA8wm-KcIbi8',
             'https://colab.research.google.com/drive/1ONWZWhxJRAOLn31y4pPtu-fm3dBXhmJ8',
             'https://colab.research.google.com/drive/1mqX-YF1bKoDNVgFvj4QYWPzW_FBOHPvL',
             'https://colab.research.google.com/drive/1D8VQJud5CvO4DkXtkz83XnyzKVVoNOur',
             'https://colab.research.google.com/drive/1PF1BPbYXikePSoa1JfueqXl_YZATVKOK',
             'https://colab.research.google.com/drive/1WLk2KlWVRuGgDRR9EwpJIlURn6xaJXU1']

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
        if notebooks_config.at[i + 261, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 261, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
