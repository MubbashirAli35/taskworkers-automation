from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle
import json
import re

notebooks_links = open('./notebooks_links.json')
notebooks_links_dict = json.load(notebooks_links)


def run_notebook(notebook_name):
    options = Options()
    options.add_argument('headless')  # Configures to start chrome in headless mode
    options.add_argument('--start-maximized')  # Configures to start it with maximum window size
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        + ' (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

    with Chrome(executable_path='./chromedriver', options=options) as driver:
        if re.match('[0-9]', notebook_name[5:6]) is None:
            notebook_link = notebooks_links_dict['links'][str(notebook_name[0:6]).lower()]
            worker_cookies_path = notebooks_links_dict['cookies_paths'][str(notebook_name[0:5]).lower()]
        else:
            notebook_link = notebooks_links_dict['links'][str(notebook_name[0:7]).lower()]
            worker_cookies_path = notebooks_links_dict['cookies_paths'][str(notebook_name[0:6]).lower()]

        driver.get(notebook_link)

        for cookie in pickle.load(open(worker_cookies_path, 'rb')):

            # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
            if 'sameSite' in cookie:
                if cookie['sameSite'] == 'None':
                    cookie['sameSite'] = 'Strict'
            driver.add_cookie(cookie)

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        driver.get(notebook_link)  # Gets a Notebook

        print(notebook_name + ' Loaded')

        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':20'))
        WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.XPATH, "//*[contains(text(), 'Factory reset runtime')]")).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok')).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1v')).click()

        print(notebook_name + ' Running')  # Logs on terminal that the Notebook is running
        time.sleep(30)


def ping_notebook(notebook_name):
    options = Options()
    options.add_argument('headless')  # Configures to start chrome in headless mode
    options.add_argument('--start-maximized')  # Configures to start it with maximum window size
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        + ' (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

    with Chrome(executable_path='./chromedriver', options=options) as driver:
        if re.match('[0-9]', notebook_name[5:6]) is None:
            notebook_link = notebooks_links_dict['links'][str(notebook_name[0:6]).lower()]
            worker_cookies_path = notebooks_links_dict['cookies_paths'][str(notebook_name[0:5]).lower()]
        else:
            notebook_link = notebooks_links_dict['links'][str(notebook_name[0:7]).lower()]
            worker_cookies_path = notebooks_links_dict['cookies_paths'][str(notebook_name[0:6]).lower()]

        driver.get(notebook_link)

        for cookie in pickle.load(open(worker_cookies_path, 'rb')):

            # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
            if 'sameSite' in cookie:
                if cookie['sameSite'] == 'None':
                    cookie['sameSite'] = 'Strict'
            driver.add_cookie(cookie)

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        driver.get(notebook_link)  # Gets a Notebook

        time.sleep(10)
        print(notebook_name + ' Loaded')


notebooks_links.close()