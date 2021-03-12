from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle
import pandas as pd
import sys

# Reads configuration from the CSV about which notebooks to run for a particular worker
# notebooks_config = pd.read_csv(sys.argv[1])

# Adds configuration to the chromedriver
options = Options()
# options.add_argument('--user-data-dir=C:/Users/mubba/AppData/Local/Google/Chrome/User Data')
# options.add_argument('--profile-directory=Profile 1')
options.add_argument('headless')    # Configures to start chrome in headless mode
options.add_argument('--start-maximized')   # Configures to start it with maximum window size

# Adds a specific User Agent
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

notebooks_dict = {
    'gctw10a': 'https://colab.research.google.com/drive/10m-9N1dcjcBtE6eW8dgZRXUpvzuRrzlX',
    'gctw10b': 'https://colab.research.google.com/drive/1vfDQq-10C5J6zM_alRM3j7LQmpNcmlgx',
    'gctw10c': 'https://colab.research.google.com/drive/1JRZpIkw322EJl4IELt4TH3UI3Rs-cRfj',
    'gctw10d': 'https://colab.research.google.com/drive/1CMvY6QtGJ5E_MY2BpBA0pGhtDKi9RpUY',
    'gctw10e': 'https://colab.research.google.com/drive/15k53HAIzSNM4e3kdQgRXHssleV2eEmr2',
    'gctw10f': 'https://colab.research.google.com/drive/1KZCLdBGgAl5FMXYcArV94sQYw2O9MEYT',
    'gctw10g': 'https://colab.research.google.com/drive/1Q-OcMemqBpp9y2o_XQzy1WdPbcKYaF0T',
    'gctw10h': 'https://colab.research.google.com/drive/1Z7DfYPYUf1NXe2MiSSzKWKUPIcYd3ziK',
    'gctw10i': 'https://colab.research.google.com/drive/1Z4vuB0a79uF9Wijjvgirwu0_pmiW7DVg'
}

notebook_link = 'https://colab.research.google.com/drive/10m-9N1dcjcBtE6eW8dgZRXUpvzuRrzlX'

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:
    # driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Aaa5bbfcd04987df9%2C10%3A1609186223%2C16%3Ae0f9e400ff758b8a%2Cc93369a30a25c98422fa6bbedbcd77dca39193057a5efe32ea8b0bb0c24a2d50%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2200c68903dfa345e59f106379ca35fdb8%22%7D&response_type=code&flowName=GeneralOAuthFlow')

    driver.get(notebook_link)    # Gets first notebook

    # Adds Cookies for this particular task worker's gmail account
    for cookie in pickle.load(open('./cookies/cookies_gctw10.pkl', 'rb')):

        # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # The line below reads cookies from the site, since cookie expiration period is long enough,
    # You won't need to uncomment it
    # time.sleep(5)
    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw01.pkl', 'wb'), protocol=2)

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.get(notebook_link)  # Gets a Notebook

    print(sys.argv[1] + ' Loaded')  # Logs on terminal that the Notebook is loaded

    if sys.argv[2].lower() == 'interact':
        time.sleep(10)

        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
    elif sys.argv[2].lower() == 'terminate':
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
        WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.XPATH, "//*[contains(text(), 'Factory reset runtime')]")
        ).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok')).click()
    else:
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':20'))
        WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.XPATH, "//*[contains(text(), 'Factory reset runtime')]")).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok')).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
        WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1w')).click()

        print(sys.argv[1] + ' Running')  # Logs on terminal that the Notebook is running
        time.sleep(10)
