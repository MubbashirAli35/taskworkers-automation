from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pickle
import pandas as pd
import sys

notebooks_config = pd.read_csv(sys.argv[1])

options = Options()
options.add_argument('headless')
options.add_argument('--start-maximized')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks = ['https://colab.research.google.com/drive/1Ai5GLCw4adNX3gEbDOnw21F0Id-yYqRw',
            'https://colab.research.google.com/drive/1Q_Kvcdl0S5yqyTSjyjm5-tLeQUXg2vnw',
            'https://colab.research.google.com/drive/1NH4lXceVGq2MNbsLQPh_jyWi_XzNL5wK',
            'https://colab.research.google.com/drive/1phFAZeaQ3OHjtzjqCvWR3_n-4a8Su-Bs',
            'https://colab.research.google.com/drive/1ri9aXj2huB_GaPtgp5xote_aBDZbIKi6',
            'https://colab.research.google.com/drive/1m-bnyK_sFIV7bGEjqidtvV-w1zzrS3r4',
            'https://colab.research.google.com/drive/1SBnmng_eMe2PgFUHnlnpLCpJpjU8QiZH',
            'https://colab.research.google.com/drive/1ZncEiiMyilNVgILBMR8O-VegX7Q13G4M',
            'https://colab.research.google.com/drive/1D3n1A-lXKvBTQ7xPMdajlwz8byPYu8vN'] 

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    # driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Ac5921dac60514d45%2C10%3A1600365462%2C16%3Ac2ff366d22bf25ef%2C43ad100192963a0ab68a62cd6581a5f8f77214d8a5ac4276eba49418bd0ccf5d%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22bc4e24a526c546b1a401552595c8f591%22%7D&response_type=code&flowName=GeneralOAuthFlow')
    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw07.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)
    
    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw07.pkl', 'wb'), protocol=2)

    for i in range(9):
        if notebooks_config.at[i + 54, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')
            driver.get(notebooks[i])

            print(notebooks_config.at[i + 54, 'Notebooks'], 'Loaded')

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

            print(notebooks_config.at[i + 54, 'Notebooks'], 'Running')

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