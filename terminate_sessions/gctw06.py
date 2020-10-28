from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pickle
import pandas as pd

notebooks_data = pd.read_csv('../config_mixed.csv')

options = Options()
options.add_argument('headless')
options.add_argument('--start-maximized')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks = ['https://colab.research.google.com/drive/18qx2GuKEfXALirrHhKR7BbkBYf5rOP7R',
            'https://colab.research.google.com/drive/1uQu8nG7ETgavRQQTElazlCG58-2wt0tb',
            'https://colab.research.google.com/drive/1DgoVrHkCrsX5EvKs5SkRo0mrFqscNUkt',
            'https://colab.research.google.com/drive/1Nr7cI4dSZP4xvg9BQ1lRlKajqMH6fbvb',
            'https://colab.research.google.com/drive/1ZtH7ZYgx07zt4Uq6XuElr0n-Qg0vkSNb',
            'https://colab.research.google.com/drive/1MIH8lt56mMLJv_XzcPGqutpQS9-H5QXA',
            'https://colab.research.google.com/drive/1DbByWMHFkXuCAQTzQjiEvut3sya08BLv',
            'https://colab.research.google.com/drive/1zy-gRPeq9HG0hVs6h4S5Xp8gQaUQaXrQ',
            'https://colab.research.google.com/drive/1Z6sF2SVlSYIzS37oIBM_6eZBP1n39cne']

cookies_path = '../cookies/cookies_gctw06.pkl'

i = 0

with Chrome() as driver:
    driver.get(notebooks[0])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 45, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')

            driver.get(notebooks[i])

            time.sleep(20)
            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

            interrupt_execution = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1x'))

            try:
                interrupt_execution.click()
            except WebDriverException:
                print(notebooks_data.at[i + 45, 'Notebooks'] + 'already not in execution')

            try:
                reset_runtime = driver.find_element_by_xpath("//*[contains(text(), 'Factory reset runtime')]")
                time.sleep(2)
                reset_runtime.click()

                WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok'))
                reset_confirmation = driver.find_element(By.ID, 'ok')
                time.sleep(2)
                reset_confirmation.click()
            except WebDriverException:
                time.sleep(2)
                runtime_menu.click()
                time.sleep(2)
                reset_runtime = driver.find_element_by_xpath("//*[contains(text(), 'Factory reset runtime')]")
                time.sleep(2)
                reset_runtime.click()

                WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok'))
                reset_confirmation = driver.find_element(By.ID, 'ok')
                time.sleep(2)
                reset_confirmation.click()

            print(notebooks_data.at[i + 45, 'Notebooks'] + ' terminated')

        i += 1
