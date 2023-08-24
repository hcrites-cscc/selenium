from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def convert_url_to_lti(driver):
    global content_handlers
    with open("convert_url_to_lti.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_id, content_id = content.split("\t")    

            driver.get(my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_"+content_id+"_1&course_id=_"+course_id+"_1&dispatch=edit&type=externallink")

            driver.find_element(By.ID, "bltiToolProvider").click()

            driver.execute_script("document.getElementById('launchInNew_true').checked = true;")
            

            driver.find_element(By.NAME, "bottom_Submit").click()
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
            except :
                print("Failed to update: "+course_id+" "+content_id)
                driver.implicitly_wait(3)

def main():
    driver = login()
    convert_url_to_lti(driver)
    logout(driver)

main()
