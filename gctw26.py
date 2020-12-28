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
notebooks = ['https://colab.research.google.com/drive/1LjOTJNCyWh-FS0tq8hYch3iT1W3_bOLn',
             'https://colab.research.google.com/drive/1nGgTWVj1883MZgrvkGVsigMzIVlGsRSQ',
             'https://colab.research.google.com/drive/1TfssgyHGO8fRyS6L7XXFzJp3vcn4Dakl',
             'https://colab.research.google.com/drive/12ahIzZ_zrxpS_ria8wDnosnRjJvxuuct',
             'https://colab.research.google.com/drive/1WBOq5KzqDYFSMSEJhpZ91LK0AnLi9qtq',
             'https://colab.research.google.com/drive/1p5qeJF1U-LcR5LTOQLN-l-6wllqJYKDd',
             'https://colab.research.google.com/drive/1k205oemSR299Sw8yXt3a9iiDm3m9PhJY',
             'https://colab.research.google.com/drive/1nz9YkZpPW57vPddPIrzN4Vt1ufPSXCox',
             'https://colab.research.google.com/drive/1NqR3Vq1M9MVTafqNguadRpVMHw27uvlu']

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:
    # driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Aaa5bbfcd04987df9%2C10%3A1609186223%2C16%3Ae0f9e400ff758b8a%2Cc93369a30a25c98422fa6bbedbcd77dca39193057a5efe32ea8b0bb0c24a2d50%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2200c68903dfa345e59f106379ca35fdb8%22%7D&response_type=code&flowName=GeneralOAuthFlow')

    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw26.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)

    for i in range(9):
        if notebooks_config.at[i + 225, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])
            # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw26.pkl', 'wb'), protocol=2)

            print(notebooks_config.at[i + 225, 'Notebooks'] + ' Loaded')

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

            print(notebooks_config.at[i + 225, 'Notebooks'] + ' Running')

            time.sleep(180)
            driver.save_screenshot('./screenshots/gctw26/' + notebooks_config.at[i + 225, 'Notebooks'] + '.png')
            time.sleep(2)
        i += 1

    time.sleep(20)
