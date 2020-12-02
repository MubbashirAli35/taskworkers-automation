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
notebooks = ['https://colab.research.google.com/drive/1gjOOF1jHY4X-PiXusVtUu2WT8kT4qCQj',
             'https://colab.research.google.com/drive/1ernsywlGxzCR712VA44-y2eoHqNnxeyV',
             'https://colab.research.google.com/drive/1tXPN8UDwa7PQ2gi-FrtmDpNHo0z3xJFK',
             'https://colab.research.google.com/drive/11HPQ13B87YVppw1RQyyfeXiy3OSHcchl',
            'https://colab.research.google.com/drive/1xvCbH3_JQY4qrIug6lTxAc3k-r3BdpH3',
            'https://colab.research.google.com/drive/1Yi2XlI3Bps18Z-w7frnkiIRpft6zBL5g',
            'https://colab.research.google.com/drive/1Rzd6kOfMEzAkyDF7e0TCPE7xsS9XmRwN',
            'https://colab.research.google.com/drive/1TuWWobKyHwr01Mgc9S5s0sKkTEt-39HG',
            'https://colab.research.google.com/drive/1McFdDf40LkRnvE1CUO0bsVqyhEviLVVm'] 

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:
    driver.get(notebooks[0])    # Gets first notebook

    # Adds Cookies for this particular task worker's gmail account
    for cookie in pickle.load(open('./cookies/cookies_gctw16.pkl', 'rb')):

        # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # The line below reads cookies from the site, since cookie expiration period is long enough,
    # You won't need to uncomment it

    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw16.pkl', 'wb'), protocol=2)

    # Iterates over the Notebooks' list
    for i in range(9):

        # Runs a notebook if its status is Yes in the CSV file
        if notebooks_config.at[i + 135, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')  # Opens and switches to a new tab
            driver.get(notebooks[i])    # Gets a Notebook

            print(notebooks_config.at[i + 135, 'Notebooks'] + ' Loaded')  # Logs on terminal that the Notebook is loaded

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

            print(notebooks_config.at[i + 135, 'Notebooks'] + ' Running')     # Logs on terminal that the Notebook is running

            time.sleep(5)
            driver.save_screenshot('./screenshots/gctw16/' + notebooks_config.at[i + 135, 'Notebooks'] + '.png')
            time.sleep(2)
        i += 1

    time.sleep(20)
