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

notebooks = ['https://colab.research.google.com/drive/16cdVhp5ICCnplLEjD_x7DV6ba1O0r9hl',
            'https://colab.research.google.com/drive/10xAQ4mxzhKQU2RjiOHKbjIyO1l70etYL',
            'https://colab.research.google.com/drive/1O1yoFxw3yt3ryaVSfrkVxk41zbR1Ronj',
            'https://colab.research.google.com/drive/1a7IGcxJr5_oNPJHsl5i0JR1Zt0EIuz62',
            'https://colab.research.google.com/drive/196GmCnXwaH4MV1uBaMkVQj4JLE3ISHP1s'] 

i = 0

with Chrome() as driver:

    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw14.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw14.pkl', 'wb'), protocol=2)

    for notebook in notebooks:
        driver.switch_to.new_window('tab')
        driver.get(notebook)

        if i == 0:
            print('gctw14E.ipynb loaded')
        elif i == 1:
            print('gctw14F.ipynb loaded')
        elif i == 2:
            print('gctw14G.ipynb loaded')
        elif i == 3:
            print('gctw14H.ipynb loaded')
        else:
            print('gctw14I.ipynb loaded')

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
            print('gctw14E.ipynb running')
        elif i == 1:
            print('gctw14F.ipynb running')
        elif i == 2:
            print('gctw14G.ipynb running')
        elif i == 3:
            print('gctw14H.ipynb running')
        else:
            print('gctw14I.ipynb running')

        i += 1

time.sleep(43200)