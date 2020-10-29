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

notebooks = ['https://colab.research.google.com/drive/1Ai5GLCw4adNX3gEbDOnw21F0Id-yYqRw',
            'https://colab.research.google.com/drive/1Q_Kvcdl0S5yqyTSjyjm5-tLeQUXg2vnw',
            'https://colab.research.google.com/drive/1NH4lXceVGq2MNbsLQPh_jyWi_XzNL5wK',
            'https://colab.research.google.com/drive/1phFAZeaQ3OHjtzjqCvWR3_n-4a8Su-Bs',
            'https://colab.research.google.com/drive/1ri9aXj2huB_GaPtgp5xote_aBDZbIKi6',
            'https://colab.research.google.com/drive/1m-bnyK_sFIV7bGEjqidtvV-w1zzrS3r4',
            'https://colab.research.google.com/drive/1SBnmng_eMe2PgFUHnlnpLCpJpjU8QiZH',
            'https://colab.research.google.com/drive/1ZncEiiMyilNVgILBMR8O-VegX7Q13G4M',
            'https://colab.research.google.com/drive/1D3n1A-lXKvBTQ7xPMdajlwz8byPYu8vN']

cookies_path = '../cookies/cookies_gctw07.pkl'

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[0])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 54, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 54, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 54, 'Notebooks'] + ' terminated')

        i += 1
