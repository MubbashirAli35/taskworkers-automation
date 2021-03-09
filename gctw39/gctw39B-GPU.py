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
    'gctw39a': 'https://colab.research.google.com/drive/1HLgNVOvzfQLfjKT4fTzqwb0iNieEdOXT',
    'gctw39b': 'https://colab.research.google.com/drive/1B-WHrGwObVz-mgbi06Ym_PRA_rsjCdKf',
    'gctw39c': 'https://colab.research.google.com/drive/1wGAqfi4Je0bMbtK9HpQA7qvkOlD5h6Bb',
    'gctw39d': 'https://colab.research.google.com/drive/1vEAY2lygueHAT4Xvw9iQ61VLVum-PAOM',
    'gctw39e': 'https://colab.research.google.com/drive/11wY0HIDqbVa-khnAEqgd-y7PzcAUzjQY',
    'gctw39f': 'https://colab.research.google.com/drive/1vcCLloeXa86-_ADDpHeCAOjECU56-omH',
    'gctw39g': 'https://colab.research.google.com/drive/1D_iUn80-Ent5UvmnlXfENf5UHXZv7tUf',
    'gctw39h': 'https://colab.research.google.com/drive/1j4z_rAB4ibdAuqRYpt9jstDpVdnL1SX3',
    'gctw39i': 'https://colab.research.google.com/drive/1EhRkXpeuR-A3-K2r83f0QpWF5zvbrpX7'
}

notebook_link = 'https://colab.research.google.com/drive/1B-WHrGwObVz-mgbi06Ym_PRA_rsjCdKf'

i = 0

with Chrome(executable_path='./chromedriver', options=options) as driver:
    # driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Aaa5bbfcd04987df9%2C10%3A1609186223%2C16%3Ae0f9e400ff758b8a%2Cc93369a30a25c98422fa6bbedbcd77dca39193057a5efe32ea8b0bb0c24a2d50%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2200c68903dfa345e59f106379ca35fdb8%22%7D&response_type=code&flowName=GeneralOAuthFlow')

    driver.get(notebook_link)    # Gets first notebook

    # Adds Cookies for this particular task worker's gmail account
    for cookie in pickle.load(open('./cookies/cookies_gctw39.pkl', 'rb')):

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

    WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
    WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':20'))
    WebDriverWait(driver, 20).until(lambda d: d.find_element(By.XPATH, "//*[contains(text(), 'Factory reset runtime')]")).click()
    WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'ok')).click()
    WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button')).click()
    WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, ':1w')).click()

    print(sys.argv[1] + ' Running')  # Logs on terminal that the Notebook is running