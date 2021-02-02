from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pickle
import pandas as pd
import sys

config_path = '../' + sys.argv[1]

notebooks_data = pd.read_csv(config_path)

options = Options()
options.add_argument('headless')
options.add_argument('--start-maximized')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks = ['https://colab.research.google.com/drive/1TnT2ItyYZepZ1ZCNArIFE494KfyriiD9',
             'https://colab.research.google.com/drive/1i-mFW36sbt4HPXY-NnppWuh4WRUGkIWP',
             'https://colab.research.google.com/drive/1g5t7e2yezMF6hyTbD74JU_4y_kJWfSt7',
             'https://colab.research.google.com/drive/1miOfiB2XPqN5Lw39P8IjdNG99nAqyZLY',
             'https://colab.research.google.com/drive/1p0mIA8-SVmjulVlL8NuvIrnR85AXzP0w',
             'https://colab.research.google.com/drive/1BQhXShJw1KPMBU5-OWilFKFzhjjAphp4',
             'https://colab.research.google.com/drive/109pLG3KzY6xmuA5HDerFJyXcQ0iH1L3g',
             'https://colab.research.google.com/drive/10_GE-jfTBSVA52FHzR-zeaL-m3ydsa7b',
             'https://colab.research.google.com/drive/1phEqv8G7B7p7h8OUX55hVK3trSx5cfh9']

cookies_path = '../cookies/cookies_gctw25.pkl'

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[4])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 306, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 306, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 306, 'Notebooks'] + ' terminated')

        i += 1

    time.sleep(20)
