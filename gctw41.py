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
# options.add_argument('--user-data-dir=C:/Users/mubba/AppData/Local/Google/Chrome/User Data')
# options.add_argument('--profile-directory=Profile 45')
options.add_argument('headless')    # Configures to start chrome in headless mode
options.add_argument('--start-maximized')   # Configures to start it with maximum window size

# Adds a specific User Agent
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks_dict = {
    'gctw41a': 'https://colab.research.google.com/drive/1hzZJNLmKKnCJ0c1al3E5Yd9TXctVehQS',
    'gctw41b': 'https://colab.research.google.com/drive/1Bo-6RuQZnEUxUbdzA7i_rt96dgbAivUI',
    'gctw41c': 'https://colab.research.google.com/drive/1tVfdtBVZRdgylG47WQ9rzqBXnn0OB-gU',
    'gctw41d': 'https://colab.research.google.com/drive/1K4i-WqOdLpIgd2GIilcEsUdpjm3O01Yr',
    'gctw41e': 'https://colab.research.google.com/drive/1QlCq2YCZtYJ_44-AiCSVERT9qX4zvsPb',
    'gctw41f': 'https://colab.research.google.com/drive/17nNOJQb7i3aaIIktB_8YFONl4f8vKWJ3',
    'gctw41g': 'https://colab.research.google.com/drive/1ZgjxknJAoBTixPFXUARAcvKsAxhYCSqj',
    'gctw41h': 'https://colab.research.google.com/drive/12rZnPmRpZxrhiZr06wwYhPWZy5bkuIi1',
    'gctw41i': 'https://colab.research.google.com/drive/15wrLaNlFQvOuiytxpdY7ql4CbgZPQ7pU'
}

# List of Notebooks' URLs for this particular task worker
notebooks = ['https://colab.research.google.com/drive/1hzZJNLmKKnCJ0c1al3E5Yd9TXctVehQS',
             'https://colab.research.google.com/drive/1Bo-6RuQZnEUxUbdzA7i_rt96dgbAivUI',
             'https://colab.research.google.com/drive/1tVfdtBVZRdgylG47WQ9rzqBXnn0OB-gU',
             'https://colab.research.google.com/drive/1K4i-WqOdLpIgd2GIilcEsUdpjm3O01Yr',
             'https://colab.research.google.com/drive/1QlCq2YCZtYJ_44-AiCSVERT9qX4zvsPb',
             'https://colab.research.google.com/drive/17nNOJQb7i3aaIIktB_8YFONl4f8vKWJ3',
             'https://colab.research.google.com/drive/1ZgjxknJAoBTixPFXUARAcvKsAxhYCSqj',
             'https://colab.research.google.com/drive/12rZnPmRpZxrhiZr06wwYhPWZy5bkuIi1',
             'https://colab.research.google.com/drive/15wrLaNlFQvOuiytxpdY7ql4CbgZPQ7pU']

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:
    # driver.get('https://accounts.google.com/o/oauth2/auth?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile+email&redirect_uri=https%3a%2f%2fstackauth.com%2fauth%2foauth2%2fgoogle&state=%7b%22sid%22%3a1%2c%22st%22%3a%2259%3a3%3abbc%2c16%3ad59a408c62ea918c%2c10%3a1612268008%2c16%3a28c2775f72a01b57%2c583d15e6d908c8c93e0b889ad6ccde0fd8b4ff8e85e39adea0dab6d971012af9%22%2c%22cdl%22%3anull%2c%22cid%22%3a%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2c%22k%22%3a%22Google%22%2c%22ses%22%3a%2202019a361f354830a83f24a0f6ac63d7%22%7d&response_type=code')
    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw41.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(5)
    #
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw41.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 360, 'Status'] == 'Yes':
        # if True:
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 360, 'Notebooks'] + ' Loaded')

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

            print(notebooks_config.at[i + 360, 'Notebooks'] + ' Running')

        i += 1

    time.sleep(20)
