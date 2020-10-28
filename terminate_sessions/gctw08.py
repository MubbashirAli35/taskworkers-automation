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

notebooks = ['https://colab.research.google.com/drive/1xzdYrRZDYo8s-xdK3F1nXz-Xu0f3fw5_',
            'https://colab.research.google.com/drive/1U58l5rPqSHDH629HU0nNwZgETCZHileC',
            'https://colab.research.google.com/drive/1U3Ol-LNu4mitnpmbZT_N0WTvwcKPnzVp',
            'https://colab.research.google.com/drive/1NRyJ1YQNpaO-D7TF7-okJk6icennOvoX',
            'https://colab.research.google.com/drive/1rvZuH53A4HUtqkz61EDXoyaG2Qcz9Wax',
            'https://colab.research.google.com/drive/1gArOv4Kkjxzpi9mCa-iPjuKv7_CfNED-',
            'https://colab.research.google.com/drive/1nbif7SgZ68a1Lwt6kxDsGhZVLZ6aafWk',
            'https://colab.research.google.com/drive/1CBTNiCBqSWJlZKifJGS4GrNTStBay8gc',
            'https://colab.research.google.com/drive/1ThJYQnkn8TVcC4gYG9hlHX_eZ504MaKR']

cookies_path = '../cookies/cookies_gctw08.pkl'

i = 0

with Chrome() as driver:
    driver.get(notebooks[0])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 63, 'Status'] == 'Yes':
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
                print(notebooks_data.at[i + 63, 'Notebooks'] + 'already not in execution')

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

            print(notebooks_data.at[i + 63, 'Notebooks'] + ' terminated')

        i += 1
