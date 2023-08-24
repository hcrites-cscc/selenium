from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def convert_to_item(driver):
    with open("convert_to_item.txt", mode="r", encoding="utf-8") as convert_list:
        content_line = convert_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            course_id = content_array[0]
            content_id = content_array[1]

            driver.get(my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_"+content_id+"_1&course_id=_"+course_id+"_1&dispatch=edit")

            try:
                driver.find_element(By.NAME, "bottom_Submit").click()
                driver.implicitly_wait(3)

                try:
                    driver.find_element(By.ID, "goodMsg1").text
                    print("Success: "+course_id+" "+content_id)
                    
                except:
                    print("Failed to convert: "+course_id+" "+content_id)
                
            except:
                print("Failed to display: "+course_id+" "+content_id)

            


def main():
    driver = login()
    convert_to_item(driver)
    logout(driver)

main()
