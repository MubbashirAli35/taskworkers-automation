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

notebooks = ['https://colab.research.google.com/drive/1ZtH7ZYgx07zt4Uq6XuElr0n-Qg0vkSNb',
            'https://colab.research.google.com/drive/1MIH8lt56mMLJv_XzcPGqutpQS9-H5QXA',
            'https://colab.research.google.com/drive/1DbByWMHFkXuCAQTzQjiEvut3sya08BLv',
            'https://colab.research.google.com/drive/1zy-gRPeq9HG0hVs6h4S5Xp8gQaUQaXrQ',
            'https://colab.research.google.com/drive/1Z6sF2SVlSYIzS37oIBM_6eZBP1n39cne'] 

i = 0

with Chrome() as driver:

    driver.get(notebooks[0])

    for cookie in pickle.load(open('./cookies/cookies_gctw06.pkl', 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # WebDriverWait(driver, 20).until(lambda d: d.find_element(By.TAG_NAME, 'input'))

    # #time.sleep(2)
    # email_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    # time.sleep(2)
    # email_box.send_keys('gctaskworker6@gmail.com')
    # print('Email for gctw06 entered')
    # driver.save_screenshot('image.png')   
    # email_box_next = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='VfPpkd-Jh9lGc']")))
    # driver.execute_script('arguments[0].click();', email_box_next)
    # print('Next on Email page clicked')

    # time.sleep(2)
    # driver.save_screenshot('image.png')
    # pass_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    # pass_box.send_keys('gc$$32145')
    # print('Password entered')

    # # driver.save_screenshot('image.png')
    # pass_next = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='VfPpkd-Jh9lGc']")))
    # driver.execute_script('arguments[0].click();', pass_next)
    # print('Next on Password clicked')

    # time.sleep(20)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw06.pkl', 'wb'), protocol=2)

    for notebook in notebooks:
        driver.switch_to.new_window('tab')
        driver.get(notebook)

        # WebDriverWait(driver, 20).until(lambda d: d.find_element(By.CLASS_NAME, 'inputarea'))

        time.sleep(20)
        # driver.save_screenshot('image.png')
        runtime_menu = driver.find_element(By.ID, 'runtime-menu-button')
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
            print('gctw06E running')
        elif i == 1:
            print('gctw06F running')
        elif i == 2:
            print('gctw06G running')
        elif i == 3:
            print('gctw06H running')
        else:
            print('gctw06I running')

        i += 1

time.sleep(43200)