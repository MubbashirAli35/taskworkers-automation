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

notebooks = ['https://colab.research.google.com/drive/1-94zP9MTGFSsviJyx0_eeVIyZ0NFj403',
             'https://colab.research.google.com/drive/1vxoBdcpFeBcwwsxXQF5mWYffQVVIJV5S',
             'https://colab.research.google.com/drive/1d6Y8gsDCovPO-pRoJ0kpm2UD5XQFLe32',
             'https://colab.research.google.com/drive/1eLpq7hPhP6WqPN2RJy_dOB5vGYuY_Iv5',
             'https://colab.research.google.com/drive/1YTeCbmXsOg2qI9AR-5zAELip_sS-DPpH',
             'https://colab.research.google.com/drive/1LwXF_9z_We0mPSAGusWkAFLXXzcnpHB5',
             'https://colab.research.google.com/drive/1tSUe-JrHVB6UwqfqHmhbEul8sIUnkrPW',
             'https://colab.research.google.com/drive/1sPOWFLdcAUOKilkj9s3_QXzONos3UVSF',
             'https://colab.research.google.com/drive/1SyHEWXtCuGwKXLdneuafJ5FaAs3LPmh1']

cookies_path = '../cookies/cookies_gctw24.pkl'

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[4])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 207, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 207, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 207, 'Notebooks'] + ' terminated')

        i += 1

    time.sleep(20)
