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
notebooks = ['https://colab.research.google.com/drive/1ItfZWr8u2qjwXn6srkee6-Eo0cEYIBep',
             'https://colab.research.google.com/drive/19pHXnkNeHwSUg6je2GmB04ROu4wAObuZ',
             'https://colab.research.google.com/drive/1roVDTuZq_UTnbGmobFqF6Hh-YmsmVSK0',
             'https://colab.research.google.com/drive/1q2sAj5XVR4ggIROAaaRlSb0yVqsBsrNa',
            'https://colab.research.google.com/drive/1sZmKfU1JGUeVCsfgeKEJbCMTT_0urhCX',
            'https://colab.research.google.com/drive/1Vb6fkGMWwJLghoXqTNueDnkEWZGbd_2i',
            'https://colab.research.google.com/drive/1ZY1dQcVZjAtJR7xH6GMX47MxumrjQz0j',
            'https://colab.research.google.com/drive/1polX7Mrg2HgrIbLImZWR0ShpjJri9axk',
            'https://colab.research.google.com/drive/1vcZoohRQoHq9siUOqGnclR1xUAGvo_FM'] 

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('./cookies/cookies_gctw17.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw17.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 144, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 144, 'Notebooks'], 'Loaded')

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

            print(notebooks_config.at[i + 144, 'Notebooks'], 'Running')

            time.sleep(5)
            driver.save_screenshot('./screenshots/gctw17/' + notebooks_config.at[i + 144, 'Notebooks'] + '.png')
            time.sleep(2)
        i += 1

    time.sleep(20)
