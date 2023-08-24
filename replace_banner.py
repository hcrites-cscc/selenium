from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import NoSuchElementException

def replace_banner_institution(driver):
    with open("replace_banner.txt", mode="r", encoding="utf-8") as banner_list:
        course_line = banner_list.read().splitlines()
        for course in course_line:
            course_pk1, file_path = course.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/cp/manageCourseDesign?cmd=display&course_id=_"+course_pk1+"_1")

            try:
                driver.find_element(By.ID, "newBanner_chooseLocalFile").send_keys(file_path)
                driver.implicitly_wait(5)
                driver.find_element(By.ID, "bottom_Submit").click()
                
                wait = WebDriverWait(driver, 1000)
                wait.until(EC.title_contains("Customization"))

                try:
                    success = driver.find_element(By.ID, "goodMsg1").text
                    print(success+" - "+course_pk1+" "+file_path)
                except:
                    print("Fail: element not found - "+course_pk1+" "+file_path)
                
            except InvalidArgumentException:
                print("Fail: new file path not found - "+course_pk1+" "+file_path)

            except NoSuchElementException:
                print("Fail: page didn't load - "+course_pk1+" "+file_path)

def main():
    driver = login()
    replace_banner_institution(driver)
    logout(driver)

main()
