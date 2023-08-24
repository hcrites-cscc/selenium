from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

def delete_banner(driver):
    with open("delete_banner.txt", mode="r", encoding="utf-8") as banner_list:
        course_line = banner_list.read().splitlines()
        for course in course_line:

            driver.get(my_domain+"/webapps/blackboard/execute/cp/manageCourseDesign?cmd=display&course_id=_"+course+"_1")

            driver.execute_script("document.getElementById('removeBanner').click();")
            driver.find_element(By.ID, "bottom_Submit").click()
            driver.implicitly_wait(5)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course)
            except:
                print("Failure: "+course)

def main():
    driver = login()
    delete_banner(driver)
    logout(driver)

main()
