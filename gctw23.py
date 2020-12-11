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
notebooks = ['https://colab.research.google.com/drive/1CrnDyRgV_YrFSZ5We3CaMRVya0TO47t2',
             'https://colab.research.google.com/drive/1m163n1lWPamlVPeIDHtjppecQVv6gc5H',
             'https://colab.research.google.com/drive/126Iv6j8gTdBJjpYYu8GfaNi61GQGp3Rh',
             'https://colab.research.google.com/drive/15lrCOQ0N-b_t9xsjBQd8LCEdBf8hYVag',
             'https://colab.research.google.com/drive/1zmOTqyHI32SmC1VSm7Nji0M6SScsWAcH',
             'https://colab.research.google.com/drive/14KaeDJlH0p2U-dp1rARgDwn-JSS2-L_W',
             'https://colab.research.google.com/drive/1KLzj1q6JDMm1HL9Y0HhV7KInBfmWmwCi',
             'https://colab.research.google.com/drive/1RV70d9Ny4jvU6_Wuy5MZl_idJ_WfiiQo',
             'https://colab.research.google.com/drive/1e1T7SOfdZS2mVP9LCFzzt4eRJ2DzS41S']

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('./cookies/cookies_gctw23.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw23.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 198, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 198, 'Notebooks'] + ' Loaded')

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

            print(notebooks_config.at[i + 198, 'Notebooks'] + ' Running')

            time.sleep(180)
            driver.save_screenshot('./screenshots/gctw23/' + notebooks_config.at[i + 198, 'Notebooks'] + '.png')
            time.sleep(2)
        i += 1

    time.sleep(20)
