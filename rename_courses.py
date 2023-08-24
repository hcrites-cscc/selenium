from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def rename_folders(driver):
    with open("rename_courses.txt", mode="r", encoding="utf-8") as rename_list:
        content_line = rename_list.read().splitlines()
        for content in content_line:
            course_pk1, new_name = content.split("\t")
            
            driver.get(my_domain+"/webapps/blackboard/execute/editCourseManager?sourceType=COURSES&context=MODIFY&course_id=_"+course_pk1+"_1")

            driver.implicitly_wait(3)

            found = False

            try:
                driver.find_element(By.ID, "courseName").clear()
                driver.find_element(By.ID, "courseName").send_keys(new_name)
                
                driver.find_element(By.NAME, "bottom_Submit").click()

                driver.implicitly_wait(3)

                try:
                    driver.find_element(By.ID, "goodMsg1").text
                    print("Success: "+new_name)
                    
                except :
                    print("Failed to update: "+new_name)
                    driver.implicitly_wait(3)
                    
            except:
                #driver.execute_script("alert('"+old_directory+file+" not found')")
                print(course_pk1+" not found")                



 

def main():
    driver = login()
    rename_folders(driver)
    logout(driver)

main()
