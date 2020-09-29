from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pickle

options = Options()
options.add_argument('headless')
options.add_argument('--start-maximized')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks = ['https://colab.research.google.com/drive/15k53HAIzSNM4e3kdQgRXHssleV2eEmr2',
            'https://colab.research.google.com/drive/1KZCLdBGgAl5FMXYcArV94sQYw2O9MEYT',
            'https://colab.research.google.com/drive/1Q-OcMemqBpp9y2o_XQzy1WdPbcKYaF0T',
            'https://colab.research.google.com/drive/1Z7DfYPYUf1NXe2MiSSzKWKUPIcYd3ziK'] 

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw10.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw10.pkl', 'wb'), protocol=2)

    for notebook in notebooks:
        driver.switch_to.new_window('tab')
        driver.get(notebook)

        if i == 0:
            print('gctw10E.ipynb loaded')
        elif i == 1:
            print('gctw10F.ipynb loaded')
        elif i == 2:
            print('gctw10G.ipynb loaded')
        elif i == 3:
            print('gctw10H.ipynb loaded')
        else:
            print('gctw10I.ipynb loaded')

        runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
        time.sleep(2)
        runtime_menu.click()

        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':20'))

        reset_runtime = driver.find_element(By.ID, ':20')
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

        if i == 0:
            print('gctw10E.ipynb running')
        elif i == 1:
            print('gctw10F.ipynb running')
        elif i == 2:
            print('gctw10G.ipynb running')
        elif i == 3:
            print('gctw10H.ipynb running')
        else:
            print('gctw10I.ipynb running')

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