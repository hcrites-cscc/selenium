from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def edit_tool_availability(driver):
    with open("edit_tool_availability.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            course_pk1 = content_array[0]
            list_of_tools = content_array[1].split("|")

            driver.get(my_domain+"/webapps/blackboard/execute/course/tools/settings?dispatch=viewToolsSettings&course_id=_"+course_pk1+"_1")

            driver.implicitly_wait(3)

            found = False         
	
            for tool in list_of_tools:
                try:
                    #--- Use this to enable tool type
                    #driver.execute_script("checkbox = document.getElementById('available__"+tool+"_1'); if(!checkbox.checked) {checkbox.click();}")

                    #--- Use this to disable tool type
                    #driver.execute_script("checkbox = document.getElementById('available__"+tool+"_1'); if(checkbox.checked) {checkbox.click();}")

                    #--- Use this to enable content type
                    driver.execute_script("checkbox = document.getElementById('_"+tool+"_1'); if(!checkbox.checked) {checkbox.click();}")

                    #--- Use this to disable content type
                    #driver.execute_script("checkbox = document.getElementById('_"+tool+"_1'); if(checkbox.checked) {checkbox.click();}")

                    driver.implicitly_wait(20)
                    
                    if bool(found) == False:
                        found = True
                        
                except:
                    print(course_pk1+tool+" not found")
            
            if bool(found) == True:
                driver.find_element(By.ID, "bottom_Submit").click()
                driver.implicitly_wait(3)

                try:
                    print(driver.find_element(By.ID, "goodMsg1").text)
                except:
                    print("element not found")

def main():
    driver = login()
    edit_tool_availability(driver)
    logout(driver)

main()
