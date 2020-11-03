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
notebooks = ['https://colab.research.google.com/drive/1DHev3HMoYrWmciakdgj7GD8k9OqPVVZz',
             'https://colab.research.google.com/drive/1kDCJEVzt_Fi3vwgEYUFKkrQRDXzFgKsS',
             'https://colab.research.google.com/drive/1ll3WvPVLDetvTg37DTY16P3dVq_5gwn_',
             'https://colab.research.google.com/drive/1SiiqbUeqzyWu0P5aqgPY-03CCuwv5v1b',
            'https://colab.research.google.com/drive/1yiHj3QtustmMWYbu_JmdFlvQM_foXO1p',
            'https://colab.research.google.com/drive/1p9VWjAsIOfuuTb1YS4PehO7GfAJ__xAC',
            'https://colab.research.google.com/drive/14VLU6TbnDA-BTrwu_NXPhwtjILnhfXIq',
            'https://colab.research.google.com/drive/1vi84XuJ9twvWZpQ0ESpycRKzMKH07A03',
            'https://colab.research.google.com/drive/1ipYdRv70QUo8vUtrmqOEo-azHrYgdHk5'] 

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    driver.get(notebooks[4])

    for cookie in pickle.load(open('./cookies/cookies_gctw19.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw19.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 162, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 162, 'Notebooks'], 'Loaded')

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

            print(notebooks_config.at[i + 162, 'Notebooks'], 'Running')

        i += 1

    interaction_cycles = 0

    for interaction_cycles in range(6):
        time.sleep(7200)
        tabs = 0

        for window_handle in driver.window_handles:
            driver.switch_to.window(window_handle)

            if tabs != 0:
                WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()

            tabs += 1

        interaction_cycles += 1