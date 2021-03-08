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
# options.add_argument('--user-data-dir=C:/Users/mubba/AppData/Local/Google/Chrome/User Data')
# options.add_argument('--profile-directory=Profile 1')
options.add_argument('headless')    # Configures to start chrome in headless mode
options.add_argument('--start-maximized')   # Configures to start it with maximum window size

# Adds a specific User Agent
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks_dict = {
    'gctw01a': 'https://colab.research.google.com/drive/1CvwSNCrZNP-zNM6i4SnEAfZTcBbO79lR',
    'gctw01b': 'https://colab.research.google.com/drive/1_Y-JFW36AY2gMdDbwz_Os3LI1DianUaC',
    'gctw01c': 'https://colab.research.google.com/drive/1TM_qtPMmbzDsUvbUh266Gm1biip9I6SH',
    'gctw01d': 'https://colab.research.google.com/drive/12Z_2YQoGFHJ_1p4duhGdoxmk6mCGYpQq',
    'gctw01e': 'https://colab.research.google.com/drive/1uzBFUgUpzkZ_jm3ddq4by0EiIu-WLzmr',
    'gctw01f': 'https://colab.research.google.com/drive/1-aLcgnKZuW2Gv_iqw8pirhuoG0jXVbdg',
    'gctw01g': 'https://colab.research.google.com/drive/1z6K7S_ZXpLesdUJTChexmLtY00V7rO8c',
    'gctw01h': 'https://colab.research.google.com/drive/1R4-1Vp8GouYjky2OBNHZFyLnsIvp-W9V',
    'gctw01i': 'https://colab.research.google.com/drive/1gxnMi-ge50zl_F1PIih_lzh003ziYzi0'
}

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

with Chrome(executable_path='./chromedriver', options=options) as driver:
    # driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Aaa5bbfcd04987df9%2C10%3A1609186223%2C16%3Ae0f9e400ff758b8a%2Cc93369a30a25c98422fa6bbedbcd77dca39193057a5efe32ea8b0bb0c24a2d50%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2200c68903dfa345e59f106379ca35fdb8%22%7D&response_type=code&flowName=GeneralOAuthFlow')

    driver.get(notebooks[0])    # Gets first notebook

    # Adds Cookies for this particular task worker's gmail account
    for cookie in pickle.load(open('./cookies/cookies_gctw01.pkl', 'rb')):

        # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # The line below reads cookies from the site, since cookie expiration period is long enough,
    # You won't need to uncomment it
    # time.sleep(5)
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

            WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1w'))

            # Clicks on Run all cells
            run_all = driver.find_element(By.ID, ':1w')
            time.sleep(2)
            run_all.click()

            print(notebooks_config.at[i, 'Notebooks'] + ' Running')     # Logs on terminal that the Notebook is running

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
    #
    #     interaction_cycles += 1
