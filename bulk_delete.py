from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def bulk_delete(driver):
    with open("bulk_delete.txt", mode="r", encoding="utf-8") as copy_list:
        course_line = copy_list.read().splitlines()
        for course in course_line:
            
            driver.get(my_domain+"/webapps/blackboard/execute/recycler?course_id=_"+course+"_1&action=select&context=COURSE")
            driver.implicitly_wait(3)

            driver.execute_script("var allInputs = document.getElementsByTagName('input');for (var i = 0, max = allInputs.length; i < max; i++){if (allInputs[i].type === 'checkbox') {allInputs[i].checked = true;}if(allInputs[i].value=='statistics'||allInputs[i].value=='users'||allInputs[i].value=='STATISTICS'||allInputs[i].value=='USERS') {allInputs[i].checked = false;}}")
            driver.implicitly_wait(3)
            
            driver.find_element(By.ID, "confirmation").send_keys("Delete")

            driver.find_element(By.ID, "bottom_Submit").click()
            driver.implicitly_wait(5)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course)
            except:
                print("Failure: "+course)

def main():
    driver = login()
    bulk_delete(driver)
    logout(driver)

main()
