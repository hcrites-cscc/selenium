from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def delete_contacts(driver):
    with open("delete_contacts.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_pk1, parent_pk1, contact_pk1 = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/staffinfo/manageStaffInfo?course_id=_204057_1&mode=cpview")

            driver.execute_script("document.getElementsByName('parentFolderId')[0].value='"+parent_pk1+"'")
            driver.execute_script("document.getElementsByName('staffInfoId')[0].value='"+contact_pk1+"'")
            driver.execute_script("document.getElementsByName('course_id')[0].value='"+course_pk1+"'")

            try:
                driver.execute_script("document.getElementById('removeContactForm').submit()")
                
            except TimeoutException:
                #driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+contact_pk1)            
                          
            except:
                print("Failed to delete: "+course_pk1+" "+contact_pk1)

def main():
    driver = login()
    driver.set_page_load_timeout(3)
    delete_contacts(driver)
    logout(driver)

main()
