from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import pickle
import pandas as pd

notebooks_data = pd.read_csv('../config_mixed.csv')

options = Options()
options.add_argument('headless')
options.add_argument('--start-maximized')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks = ['https://colab.research.google.com/drive/17yehxLGrtoLwEnfoWpR2boM_CGp4-JYH',
            'https://colab.research.google.com/drive/1ooEA_BHJW4kNFbXeTXUpatm3Dr0sswNx',
            'https://colab.research.google.com/drive/1sCLBOXPgFYISdtgB25BF3rE-X64CME_E',
            'https://colab.research.google.com/drive/1XIEztEBWeCItWUvB1ypj2uVrxCbbP3Yp',
            'https://colab.research.google.com/drive/1xVfD6Ha3U8CNrX4p8sPjn2AXeRPLn43N',
            'https://colab.research.google.com/drive/11Hldjz_cC3Ibr85aquDy-N1dI_M2YOaU',
            'https://colab.research.google.com/drive/1hVNAxt56JUD_TTXw0ABAQi7hn01fHWwn',
            'https://colab.research.google.com/drive/1e8jIh9lQj3q6OUCL2QxlNm4ytSHub5AH',
            'https://colab.research.google.com/drive/1O_AXnGzv5PxSlTvzsQEzKhDaUWFt5WTf']

cookies_path = '../cookies/cookies_gctw09.pkl'

i = 0

with Chrome() as driver:
    driver.get(notebooks[0])

    for cookie in pickle.load(open(cookies_path, 'rb')):
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    for notebook in notebooks:

        if notebooks_data.at[i + 72, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')

            driver.get(notebooks[i])

            time.sleep(20)
            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

            interrupt_execution = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1x'))

            try:
                interrupt_execution.click()
            except WebDriverException:
                print(notebooks_data.at[i + 72, 'Notebooks'] + 'already not in execution')

            try:
                reset_runtime = driver.find_element_by_xpath("//*[contains(text(), 'Factory reset runtime')]")
                time.sleep(2)
                reset_runtime.click()

                WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok'))
                reset_confirmation = driver.find_element(By.ID, 'ok')
                time.sleep(2)
                reset_confirmation.click()
            except WebDriverException:
                time.sleep(2)
                runtime_menu.click()
                time.sleep(2)
                reset_runtime = driver.find_element_by_xpath("//*[contains(text(), 'Factory reset runtime')]")
                time.sleep(2)
                reset_runtime.click()

                WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok'))
                reset_confirmation = driver.find_element(By.ID, 'ok')
                time.sleep(2)
                reset_confirmation.click()

            print(notebooks_data.at[i + 72, 'Notebooks'] + ' terminated')

        i += 1
