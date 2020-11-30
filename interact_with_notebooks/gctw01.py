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
notebooks = ['https://colab.research.google.com/drive/1CvwSNCrZNP-zNM6i4SnEAfZTcBbO79lR',
             'https://colab.research.google.com/drive/1_Y-JFW36AY2gMdDbwz_Os3LI1DianUaC',
             'https://colab.research.google.com/drive/1TM_qtPMmbzDsUvbUh266Gm1biip9I6SH',
             'https://colab.research.google.com/drive/12Z_2YQoGFHJ_1p4duhGdoxmk6mCGYpQq',
             'https://colab.research.google.com/drive/1uzBFUgUpzkZ_jm3ddq4by0EiIu-WLzmr',
             'https://colab.research.google.com/drive/1-aLcgnKZuW2Gv_iqw8pirhuoG0jXVbdg',
             'https://colab.research.google.com/drive/1z6K7S_ZXpLesdUJTChexmLtY00V7rO8c',
             'https://colab.research.google.com/drive/1R4-1Vp8GouYjky2OBNHZFyLnsIvp-W9V',
             'https://colab.research.google.com/drive/1gxnMi-ge50zl_F1PIih_lzh003ziYzi0']

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[0])    # Gets first notebook

    # Adds Cookies for this particular task worker's gmail account
    for cookie in pickle.load(open('../cookies/cookies_gctw01.pkl', 'rb')):

        # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # The line below reads cookies from the site, since cookie expiration period is long enough,
    # You won't need to uncomment it

    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw01.pkl', 'wb'), protocol=2)

    # Iterates over the Notebooks' list
    for i in range(9):

        # Runs a notebook if its status is Yes in the CSV file
        if notebooks_config.at[i, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')  # Opens and switches to a new tab
            driver.get(notebooks[i])    # Gets a Notebook

            print(notebooks_config.at[i, 'Notebooks'] + ' Loaded')  # Logs on terminal that the Notebook is loaded

            # Gets the Runtime menu button and clicks it
            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    time.sleep(20)
