from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pickle
import pandas as pd
import sys
options = Options()
options.add_argument('headless')
options.add_argument('--start-maximized')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks = ['https://colab.research.google.com/drive/1-l47qIPM-qg2thcYmcKPbGvE5gt29pL_']

i = 0

with Chrome() as driver:
    # driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3A82fc73f3bc47e7ae%2C10%3A1602009822%2C16%3Afb578ecbe2ddb02b%2C123533b054a12c418686487d3dcf129ba24c76d4e8affc5d4afa4eb5efa96273%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22cdb698f92c9f40aeb86ce8599842d58b%22%7D&response_type=code&flowName=GeneralOAuthFlow')
    # time.sleep(20)
    driver.get(notebooks[0])
    # time.sleep(5)

    for cookie in pickle.load(open('./cookies/cookies_gctw01.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw01.pkl', 'wb'), protocol=2)

    driver.switch_to.new_window('tab')
    driver.get(notebooks[0])

    runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
    time.sleep(2)
    runtime_menu.click()

    interrupt_execution = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, ':1x')))
    time.sleep(2)

    try:
        interrupt_execution.click()
    except WebDriverException:
        print(notebooks[0], 'already not in execution')

    try:
        reset_runtime = driver.find_element_by_xpath("//*[contains(text(), 'Factory reset runtime')]")
        time.sleep(2)
        reset_runtime.click()

        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok'))
        reset_confirmation = driver.find_element(By.ID, 'ok')
        time.sleep(2)
        reset_confirmation.click()
    except WebDriverException:
        runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
        time.sleep(2)
        runtime_menu.click()

        reset_runtime = driver.find_element_by_xpath("//*[contains(text(), 'Factory reset runtime')]")
        time.sleep(2)
        reset_runtime.click()

        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok'))
        reset_confirmation = driver.find_element(By.ID, 'ok')
        time.sleep(2)
        reset_confirmation.click()

    time.sleep(600)
