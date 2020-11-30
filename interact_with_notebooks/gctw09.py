from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pickle
import pandas as pd
import sys

# Reads configuration from the CSV about which notebooks to run for a particular worker
notebooks_config = pd.read_csv('../' + sys.argv[1])

# Adds configuration to the chromedriver
options = Options()
options.add_argument('headless')    # Configures to start chrome in headless mode
options.add_argument('--start-maximized')   # Configures to start it with maximum window size

# Adds a specific User Agent
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')

# List of Notebooks' URLs for this particular task worker
notebooks = ['https://colab.research.google.com/drive/17yehxLGrtoLwEnfoWpR2boM_CGp4-JYH',
            'https://colab.research.google.com/drive/1ooEA_BHJW4kNFbXeTXUpatm3Dr0sswNx',
            'https://colab.research.google.com/drive/1sCLBOXPgFYISdtgB25BF3rE-X64CME_E',
            'https://colab.research.google.com/drive/1XIEztEBWeCItWUvB1ypj2uVrxCbbP3Yp',
            'https://colab.research.google.com/drive/1xVfD6Ha3U8CNrX4p8sPjn2AXeRPLn43N',
            'https://colab.research.google.com/drive/11Hldjz_cC3Ibr85aquDy-N1dI_M2YOaU',
            'https://colab.research.google.com/drive/1hVNAxt56JUD_TTXw0ABAQi7hn01fHWwn',
            'https://colab.research.google.com/drive/1e8jIh9lQj3q6OUCL2QxlNm4ytSHub5AH',
            'https://colab.research.google.com/drive/1O_AXnGzv5PxSlTvzsQEzKhDaUWFt5WTf'] 

i = 0

with Chrome(executable_path='../chromedriver', options=options) as driver:
    driver.get(notebooks[0])    # Gets first notebook

    # Adds Cookies for this particular task worker's gmail account
    for cookie in pickle.load(open('../cookies/cookies_gctw09.pkl', 'rb')):

        # Sets the 'sameSite' cookie to 'Strict' since Google doesn't allow requests from Cross Origin
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

    # The line below reads cookies from the site, since cookie expiration period is long enough,
    # You won't need to uncomment it

    # pickle.dump(driver.get_cookies(), open('./cookies/cookies_gctw09.pkl', 'wb'), protocol=2)

    # Iterates over the Notebooks' list
    for i in range(9):

        # Runs a notebook if its status is Yes in the CSV file
        if notebooks_config.at[i + 72, 'Status'] == 'Yes':
            driver.switch_to.new_window('tab')  # Opens and switches to a new tab
            driver.get(notebooks[i])    # Gets a Notebook

            print(notebooks_config.at[i + 72, 'Notebooks'] + ' Loaded')  # Logs on terminal that the Notebook is loaded

            # Gets the Runtime menu button and clicks it
            runtime_menu = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.ID, 'runtime-menu-button'))
            time.sleep(2)
            runtime_menu.click()

    time.sleep(20)
