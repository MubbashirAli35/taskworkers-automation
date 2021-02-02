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

notebooks = ['https://colab.research.google.com/drive/1upZZ62oPBlHiVDqXHauEBCn-ztsTEiUy',
             'https://colab.research.google.com/drive/1OxelyinGp09BN-NupbnHg0qGt1V-JvXp',
             'https://colab.research.google.com/drive/1FtqUL3edQkUDrC5WRWDxl-xNZD5uiFSp',
             'https://colab.research.google.com/drive/1m2Ulod816am-vb_C6UV4z9e2vteabWiy',
             'https://colab.research.google.com/drive/1p33fKBGcMt4EvVReVE55dgzE_hAeE4KO',
             'https://colab.research.google.com/drive/185yN5TrwVbeNHWdxCep5OnO1AmK9zXhM',
             'https://colab.research.google.com/drive/1RIalPiOhyYDHqHUf3qD78_XoK1AdX5Vk',
             'https://colab.research.google.com/drive/1RoaxcN4Ymh9wqIBrm0Z-TvLJk908K3Kp',
             'https://colab.research.google.com/drive/1YgLQH_yvZB8Re9Q6CJ41bWK59oWAhU3N']

cookies_path = '../cookies/cookies_gctw29.pkl'

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[4])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 252, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 252, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 252, 'Notebooks'] + ' terminated')

        i += 1

    time.sleep(20)
