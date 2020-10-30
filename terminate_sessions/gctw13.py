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

notebooks = ['https://colab.research.google.com/drive/1f7-6IVvB8hT3EW8ApoJ5VeFlj78nW9Yv',
             'https://colab.research.google.com/drive/1OJkmBIFShnRioNVTM6OWET0kTX7akW1L',
             'https://colab.research.google.com/drive/1MVa9FlfaKGumu-l3-Wa5BFv98JhOMh2k',
             'https://colab.research.google.com/drive/1DzDgxBEcMgC3a3TpavT6wWaZG1DKLWBL',
            'https://colab.research.google.com/drive/14suZUlb4Ogpn5-vbYnBsVynysZ0iARmQ',
            'https://colab.research.google.com/drive/142hbd5szjWPjHpl419z1oXwqUKgMeG4U',
            'https://colab.research.google.com/drive/1P16iR7BBEp8lu6xjFK5ft7DiFq-WeIsq',
            'https://colab.research.google.com/drive/1rOBI5iWmFpvZuisnsMPliiY3NRC_00UV',
            'https://colab.research.google.com/drive/10zNpF2vxz4X5ASznKdGCco_LpUt7lrr3']

cookies_path = '../cookies/cookies_gctw13.pkl'

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[4])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 108, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 108, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 108, 'Notebooks'] + ' terminated')

        i += 1
