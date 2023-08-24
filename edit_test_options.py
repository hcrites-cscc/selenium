from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def edit_test_options(driver):
    with open("edit_test_options.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_pk1, content_pk1 = content.split("\t")
            
            driver.get(my_domain+"/webapps/assessment/do/content/assessment?action=MODIFY&course_id=_"+course_pk1+"_1&content_id=_"+content_pk1+"_1&assessmentType=Test&method=modifyOptions")          

            driver.implicitly_wait(3)

            #driver.execute_script("document.getElementById('noRadio').click();") #Set "Open test in a new window" to No
            driver.execute_script("document.getElementById('yesRadio').click();") #Set "Open test in a new window" to Yes
            driver.execute_script("document.getElementById('bottom_Submit').click();")

            driver.implicitly_wait(3)
            
            try:
                print(content_pk1+" "+driver.find_element(By.ID, "goodMsg1").text)
            except:
                print("element not found")

def main():
    driver = login()
    edit_test_options(driver)
    logout(driver)

main()
