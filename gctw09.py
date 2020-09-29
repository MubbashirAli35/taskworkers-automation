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

notebooks = ['https://colab.research.google.com/drive/1xVfD6Ha3U8CNrX4p8sPjn2AXeRPLn43N',
            'https://colab.research.google.com/drive/11Hldjz_cC3Ibr85aquDy-N1dI_M2YOaU',
            'https://colab.research.google.com/drive/1hVNAxt56JUD_TTXw0ABAQi7hn01fHWwn',
            'https://colab.research.google.com/drive/1e8jIh9lQj3q6OUCL2QxlNm4ytSHub5AH',
            'https://colab.research.google.com/drive/1O_AXnGzv5PxSlTvzsQEzKhDaUWFt5WTf'] 

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:

    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw09.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw09.pkl', 'wb'), protocol=2)

    for notebook in notebooks:
        driver.switch_to.new_window('tab')
        driver.get(notebook)

        if i == 0:
            print('gctw09E.ipynb loaded')
        elif i == 1:
            print('gctw09F.ipynb loaded')
        elif i == 2:
            print('gctw09G.ipynb loaded')
        elif i == 3:
            print('gctw09H.ipynb loaded')
        else:
            print('gctw09I.ipynb loaded')

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
            print('gctw09E.ipynb running')
        elif i == 1:
            print('gctw09F.ipynb running')
        elif i == 2:
            print('gctw09G.ipynb running')
        elif i == 3:
            print('gctw09H.ipynb running')
        else:
            print('gctw09I.ipynb running')

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