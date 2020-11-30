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

notebooks = ['https://colab.research.google.com/drive/1OepYFlgnNC1Q-QAM_FrXqIxheGM9fIcH',
            'https://colab.research.google.com/drive/1qxZzYVGcT3A_Ufr-KDLs0WC26KcjIWRb',
            'https://colab.research.google.com/drive/1NasDLPnKYJJMKj2wgH7Sw_2vxulzjTn7',
            'https://colab.research.google.com/drive/1v29GBW8ZN77jrTuzVYtFMEmu9igSMXiI',
            'https://colab.research.google.com/drive/1G_-Dq-ue0a6PBAMfV1W3cTlaafXV-JeD',
            'https://colab.research.google.com/drive/19c-8Ind1oofz5TTfACZ-YfrR7PhG-t8Q',
            'https://colab.research.google.com/drive/1KuK6GdBx5ySuUOmiWZnFnlgnfsd6nB1Q',
            'https://colab.research.google.com/drive/1HKvNyiHrWjfh_jYc2qCguH2UBG9Dq2EE',
            'https://colab.research.google.com/drive/1cCBNOCCWrSacNXc4UOhUKjZmv9uipuCs']

cookies_path = '../cookies/cookies_gctw11.pkl'

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[0])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 90, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 90, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 90, 'Notebooks'] + ' terminated')

        i += 1

    time.sleep(20)
