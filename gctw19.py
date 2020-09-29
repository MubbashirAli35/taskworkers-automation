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

notebooks = ['https://colab.research.google.com/drive/1yiHj3QtustmMWYbu_JmdFlvQM_foXO1p',
            'https://colab.research.google.com/drive/1p9VWjAsIOfuuTb1YS4PehO7GfAJ__xAC',
            'https://colab.research.google.com/drive/14VLU6TbnDA-BTrwu_NXPhwtjILnhfXIq',
            'https://colab.research.google.com/drive/1vi84XuJ9twvWZpQ0ESpycRKzMKH07A03',
            'https://colab.research.google.com/drive/1ipYdRv70QUo8vUtrmqOEo-azHrYgdHk5'] 

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw19.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw19.pkl', 'wb'), protocol=2)

    for notebook in notebooks:
        driver.switch_to.new_window('tab')
        driver.get(notebook)

        if i == 0:
            print('gctw19E.ipynb loaded')
        elif i == 1:
            print('gctw19F.ipynb loaded')
        elif i == 2:
            print('gctw19G.ipynb loaded')
        elif i == 3:
            print('gctw19H.ipynb loaded')
        else:
            print('gctw19I.ipynb loaded')

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
            print('gctw19E.ipynb running')
        elif i == 1:
            print('gctw19F.ipynb running')
        elif i == 2:
            print('gctw19G.ipynb running')
        elif i == 3:
            print('gctw19H.ipynb running')
        else:
            print('gctw19I.ipynb running')

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