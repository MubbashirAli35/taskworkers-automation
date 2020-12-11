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
options.add_argument('headless')    # Configures to start chrome in headless mode
options.add_argument('--start-maximized')   # Configures to start it with maximum window size

# Adds a specific User Agent
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

# List of Notebooks' URLs for this particular task worker
notebooks = ['https://colab.research.google.com/drive/1HgoOmQqGdS6uI7tB5SnqhoKthkGYyrvY',
             'https://colab.research.google.com/drive/1bnn9Syx7miXY6_OS_KBoJ8io1BceAZ5B',
             'https://colab.research.google.com/drive/1EgDoDiXQJCNgW2OR3pv0LGAPsk3QTe3z',
             'https://colab.research.google.com/drive/1EtCOFWSkV9rCQCKLodTQAAoO_od8CpER',
             'https://colab.research.google.com/drive/1YmARaITML3Qqyc6vFziQYIbCFJaF9RYj',
             'https://colab.research.google.com/drive/1_8o8NLDbz_cl3V77iDiEEmTc6_1nHdM8',
             'https://colab.research.google.com/drive/1ahxnSLjFJkRZTDtrHzBtTkE06CpId789',
             'https://colab.research.google.com/drive/1FotnajNcXfDKMWbsrtWeLyfjARrd-_2W',
             'https://colab.research.google.com/drive/12l7BwkrKR60JOsNEyrIlcehVT7K3j016']

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('./cookies/cookies_gctw27.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw27.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 234, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 234, 'Notebooks'] + ' Loaded')

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

            WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1w'))
            run_all = driver.find_element(By.ID, ':1w')
            time.sleep(2)
            run_all.click()

            print(notebooks_config.at[i + 234, 'Notebooks'] + ' Running')

            time.sleep(180)
            driver.save_screenshot('./screenshots/gctw27/' + notebooks_config.at[i + 234, 'Notebooks'] + '.png')
            time.sleep(2)
        i += 1

    time.sleep(20)
