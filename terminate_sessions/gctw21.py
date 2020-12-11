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

notebooks = ['https://colab.research.google.com/drive/1MXbb0k8B4_bhqFOYD3BQCSsUOasWOT3S',
             'https://colab.research.google.com/drive/1_h14irfmbjNuxv5EHjZ1Z85trWglsmLf',
             'https://colab.research.google.com/drive/1AribTqKwwx66uedT4UST61KA6vLd1KWh',
             'https://colab.research.google.com/drive/1_m1O8ipd4oIPLyRKHth22mlVqHy97CTr',
             'https://colab.research.google.com/drive/14uxeiSmwpKyFIkRERU9Ok4Xd9fqcfgUN',
             'https://colab.research.google.com/drive/12qFoAH4CBMCTISHCur2wUm7BNoOmJ4WR',
             'https://colab.research.google.com/drive/1IFgfzzgg-tNyIJWqWRLj0u48NbBWdSNN',
             'https://colab.research.google.com/drive/1LcQ6LGCKmLoe9KrQMLlnG1_EAsPBUD3U',
             'https://colab.research.google.com/drive/1whHgbFVNCS8ErKKRwGAIzv0NqZm9xL2q']

cookies_path = '../cookies/cookies_gctw21.pkl'

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[4])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 180, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 180, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 180, 'Notebooks'] + ' terminated')

        i += 1

    time.sleep(20)
