from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pickle
import pandas as pd
import sys

# Reads configuration from the CSV about which notebooks to run for a particular worker
notebooks_config = pd.read_csv(sys.argv[1])

# Adds configuration to the chromedriver
options = Options()
options.add_argument('headless')    # Configures to start chrome in headless mode
options.add_argument('--start-maximized')   # Configures to start it with maximum window size

# Adds a specific User Agent
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

# List of Notebooks' URLs for this particular task worker
notebooks = ['https://colab.research.google.com/drive/1rPG1tnGhjmywg12xKvRp5gpLxiEEfp3k',
             'https://colab.research.google.com/drive/1XUAf1bjfILN5mIRx1pkCb6JJCL7IliiM',
             'https://colab.research.google.com/drive/10HlXmXQ-QqTTyvSbDDfUc_jT1414orun',
             'https://colab.research.google.com/drive/1L-mZdIYp68rO5DVy-pEXzkUMQeuRFe34',
             'https://colab.research.google.com/drive/1MI5B-BLPoMn0WIs7T50pILBy4RQWIs-N',
             'https://colab.research.google.com/drive/1EUpphEExKYje759b-u0Sp7q4PsM__aT6',
             'https://colab.research.google.com/drive/1CdziYeFf0LU2JCCm-CKgPofUcbvv6CQZ',
             'https://colab.research.google.com/drive/1zCjJWW-wX8FhHDxYM-QrL9glhZf6tIis',
             'https://colab.research.google.com/drive/1dHAVjA53KVHL0Mn6670OUfCAE9VAWTjv']

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:
    driver.get(notebooks[0])    # Gets first notebook

    # Adds Cookies for this particular task worker's gmail account
    for cookie in pickle.load(open('./cookies/cookies_gctw04.pkl', 'rb')):

        # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # The line below reads cookies from the site, since cookie expiration period is long enough,
    # You won't need to uncomment it

    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw04.pkl', 'wb'), protocol=2)

    # Iterates over the Notebooks' list
    for i in range(9):

        # Runs a notebook if its status is Yes in the CSV file
        if notebooks_config.at[i + 27, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')  # Opens and switches to a new tab
            driver.get(notebooks[i])    # Gets a Notebook

            print(notebooks_config.at[i + 27, 'Notebooks'] + ' Loaded')  # Logs on terminal that the Notebook is loaded

            # Gets the Runtime menu button and clicks it
            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

            # Waits until list is opened
            WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':20'))

            # Factory resets the Notebook
            reset_runtime = driver.find_element(By.XPATH, "//*[contains(text(), 'Factory reset runtime')]")
            time.sleep(2)
            reset_runtime.click()

            WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok'))

            # Confirms to Reset the Notebook
            reset_confirmation = driver.find_element(By.ID, 'ok')
            time.sleep(2)
            reset_confirmation.click()

            # Clicks again on the Runtime Menu tab
            runtime_menu = driver.find_element(By.ID, 'runtime-menu-button')
            time.sleep(2)
            runtime_menu.click()

            WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1r'))

            # Clicks on Run all cells
            run_all = driver.find_element(By.ID, ':1r')
            time.sleep(2)
            run_all.click()

            print(notebooks_config.at[i + 27, 'Notebooks'] + ' Running')     # Logs on terminal that the Notebook is running

            time.sleep(10)
            driver.save_screenshot('./screenshots/gctw04/' + notebooks_config.at[i + 27, 'Notebooks'] + '.png')
            time.sleep(2)
        i += 1

    time.sleep(20)
    # interaction_cycles = 0
    #
    # # This loop just interacts with the Notebooks so they are not disconnected being considered idle
    # for interaction_cycles in range(6):
    #     time.sleep(7200)    # Throws an interaction on every running notebook after every 2 hours
    #     tabs = 0
    #
    #     # Iterates over all the opened tabs and interacts with them
    #     for window_handle in driver.window_handles:
    #         driver.switch_to.window(window_handle)
    #
    #         # Doesn't interact if it is the tab with Sign In form
    #         if tabs != 0:
    #             WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
    #
    #         tabs += 1
