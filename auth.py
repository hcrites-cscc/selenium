# Set your domain here
my_domain = "https://your_domain.blackboard.com/"

# Set your username
user_id = "yo"
user_password = "yo"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time, base64

def login():  
    # Pulls up the course manager
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")
    chrome_options.add_argument("--user-data-dir=C:\\Users\\hcrites\\AppData\\Local\\Google\\Chrome\\User Data")
    chrome_options.add_argument("--profile-directory=Profile 4")
    chrome_options.add_argument("--remote-allow-origins=*")
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--incognito");

    chrome_options.set_capability("pageLoadStrategy", "normal") #-- full page load
    #chrome_options.set_capability("pageLoadStrategy", "eager") #-- wait for the DOMContentLoaded event
    #chrome_options.set_capability("pageLoadStrategy", "none") #-- return immediately after html content downloaded 

    # Initiate Driver
    service = Service(executable_path=r"c:/python/BrowserDriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options) 

    # Load Login Page
    driver.get(my_domain+"/webapps/login/?action=default_login")
    #print("9")

    if find_element_by_id(driver, "agree_button"):
        driver.find_element(By.ID, "agree_button").click()
    
    if find_element_by_id(driver, "user_id"):
        driver.find_element(By.ID, "user_id").send_keys(user_id)
        driver.find_element(By.NAME, "password").send_keys(user_password)
        driver.find_element(By.ID, "entry-login").click()

    print("=================\nLog In\n=================")

    return driver

def logout(driver):
    # Logout
    driver.get(my_domain+"/webapps/login/?action=logout")

    # Wait
    time.sleep(2)

    # Close windows
    windows = driver.window_handles
    for w in windows:
        driver.switch_to.window(w)
        driver.close()
    
    # Quit Browser
    driver.quit()

    print("=================\nLog Out\n=================")

def find_element_by_id(driver, element_id):
    try:
        driver.find_element(By.ID, element_id)
    except NoSuchElementException:
        return False
    return True
