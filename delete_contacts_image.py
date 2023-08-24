from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def delete_contacts_image(driver):
    with open("delete_contacts_image.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_pk1, parent_pk1, contact_pk1 = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/staffinfo/manageContacts?parentFolderId=_"+parent_pk1+"_1&cmd=edit&staffInfoId=_"+contact_pk1+"_1&course_id=_"+course_pk1+"_1")
            time.sleep(1)
            driver.execute_script("document.getElementById('isRemoveImage').click();")
            driver.execute_script("if(document.getElementById('personalLink').value=='http://'){document.getElementById('personalLink').value='';}");
            driver.find_element(By.ID, "bottom_Submit").click()

            driver.implicitly_wait(5)           

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+contact_pk1)
            except:
                print("Failure: "+course_pk1+" "+contact_pk1)

def main():
    driver = login()
    delete_contacts_image(driver)
    logout(driver)

main()
