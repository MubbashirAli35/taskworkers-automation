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
notebooks = ['https://colab.research.google.com/drive/1OepYFlgnNC1Q-QAM_FrXqIxheGM9fIcH',
            'https://colab.research.google.com/drive/1qxZzYVGcT3A_Ufr-KDLs0WC26KcjIWRb',
            'https://colab.research.google.com/drive/1NasDLPnKYJJMKj2wgH7Sw_2vxulzjTn7',
            'https://colab.research.google.com/drive/1v29GBW8ZN77jrTuzVYtFMEmu9igSMXiI',
            'https://colab.research.google.com/drive/1G_-Dq-ue0a6PBAMfV1W3cTlaafXV-JeD',
            'https://colab.research.google.com/drive/19c-8Ind1oofz5TTfACZ-YfrR7PhG-t8Q',
            'https://colab.research.google.com/drive/1KuK6GdBx5ySuUOmiWZnFnlgnfsd6nB1Q',
            'https://colab.research.google.com/drive/1HKvNyiHrWjfh_jYc2qCguH2UBG9Dq2EE',
            'https://colab.research.google.com/drive/1cCBNOCCWrSacNXc4UOhUKjZmv9uipuCs'] 

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[0])    # Gets first notebook

    # Adds Cookies for this particular task worker's gmail account
    for cookie in pickle.load(open('../cookies/cookies_gctw11.pkl', 'rb')):

        # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # The line below reads cookies from the site, since cookie expiration period is long enough,
    # You won't need to uncomment it

    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw11.pkl', 'wb'), protocol=2)

    # Iterates over the Notebooks' list
    for i in range(9):

        # Runs a notebook if its status is Yes in the CSV file
        if notebooks_config.at[i + 90, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')  # Opens and switches to a new tab
            driver.get(notebooks[i])    # Gets a Notebook

            print(notebooks_config.at[i + 90, 'Notebooks'] + ' Loaded')  # Logs on terminal that the Notebook is loaded

            # Gets the Runtime menu button and clicks it
            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    # time.sleep(20)
