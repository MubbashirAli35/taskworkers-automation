from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pickle
import pandas as pd
import sys

notebooks_config = pd.read_csv(sys.argv[1])

options = Options()
options.add_argument('headless')
options.add_argument('--start-maximized')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks = ['https://colab.research.google.com/drive/18qx2GuKEfXALirrHhKR7BbkBYf5rOP7R',
            'https://colab.research.google.com/drive/1uQu8nG7ETgavRQQTElazlCG58-2wt0tb',
            'https://colab.research.google.com/drive/1DgoVrHkCrsX5EvKs5SkRo0mrFqscNUkt',
            'https://colab.research.google.com/drive/1Nr7cI4dSZP4xvg9BQ1lRlKajqMH6fbvb',
            'https://colab.research.google.com/drive/1ZtH7ZYgx07zt4Uq6XuElr0n-Qg0vkSNb',
            'https://colab.research.google.com/drive/1MIH8lt56mMLJv_XzcPGqutpQS9-H5QXA',
            'https://colab.research.google.com/drive/1DbByWMHFkXuCAQTzQjiEvut3sya08BLv',
            'https://colab.research.google.com/drive/1zy-gRPeq9HG0hVs6h4S5Xp8gQaUQaXrQ',
            'https://colab.research.google.com/drive/1Z6sF2SVlSYIzS37oIBM_6eZBP1n39cne'] 

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw06.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw06.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 45, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 45, 'Notebooks'], 'Loaded')

            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

            WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':20'))

            reset_runtime = driver.find_element_by_xpath("//*[contains(text(), 'Factory reset runtime')]")
            time.sleep(2)
            reset_runtime.click()

            WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok'))
            reset_confirmation = driver.find_element(By.ID, 'ok')
            time.sleep(2)
            reset_confirmation.click()

            runtime_menu = driver.find_element(By.ID, 'runtime-menu-button')
            time.sleep(2)
            runtime_menu.click()

            WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1r'))
            run_all = driver.find_element(By.ID, ':1r')
            time.sleep(2)
            run_all.click()

            print(notebooks_config.at[i + 45, 'Notebooks'], 'Running')

        i += 1

    interaction_cycles = 0
    
    for interaction_cycles in range(6):
        time.sleep(7200)
        tabs = 0

        for window_handle in driver.window_handles:
            driver.switch_to.window(window_handle)
            
            if tabs != 0:
                WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()

            tabs += 1

        interaction_cycles += 1