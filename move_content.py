from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def move_content(driver):
    with open("move_content.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_pk1, content_pk1, new_parent_pk1 = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/content/copyItem.jsp?course_id=_"+course_pk1+"_1&content_id=_"+content_pk1+"_1&bIsTabContent=false&bIsMove=true")

            driver.implicitly_wait(3)

            driver.execute_script("document.getElementById('courseLocation').value = 'New Parent';")
            driver.execute_script("document.getElementById('courseLinkType').value = 'COURSE_CONTENTS';")
            driver.execute_script("document.getElementById('courseLinkId').value = '_"+new_parent_pk1+"_1';")

            driver.find_element(By.ID, "bottom_Submit").click()
            
            try:
                print(content_pk1+" "+driver.find_element(By.ID, "goodMsg1").text)
            except:
                print("element not found")
            
def main():
    driver = login()
    move_content(driver)
    logout(driver)

main()
