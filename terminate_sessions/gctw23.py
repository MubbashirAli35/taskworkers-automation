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

notebooks = ['https://colab.research.google.com/drive/1CrnDyRgV_YrFSZ5We3CaMRVya0TO47t2',
             'https://colab.research.google.com/drive/1m163n1lWPamlVPeIDHtjppecQVv6gc5H',
             'https://colab.research.google.com/drive/126Iv6j8gTdBJjpYYu8GfaNi61GQGp3Rh',
             'https://colab.research.google.com/drive/15lrCOQ0N-b_t9xsjBQd8LCEdBf8hYVag',
             'https://colab.research.google.com/drive/1zmOTqyHI32SmC1VSm7Nji0M6SScsWAcH',
             'https://colab.research.google.com/drive/14KaeDJlH0p2U-dp1rARgDwn-JSS2-L_W',
             'https://colab.research.google.com/drive/1KLzj1q6JDMm1HL9Y0HhV7KInBfmWmwCi',
             'https://colab.research.google.com/drive/1RV70d9Ny4jvU6_Wuy5MZl_idJ_WfiiQo',
             'https://colab.research.google.com/drive/1e1T7SOfdZS2mVP9LCFzzt4eRJ2DzS41S']

cookies_path = '../cookies/cookies_gctw23.pkl'

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[4])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 198, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 198, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 198, 'Notebooks'] + ' terminated')

        i += 1

    time.sleep(20)
