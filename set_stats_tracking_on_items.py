from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def set_stats_tracking_on_items(driver):
    with open("set_stats_tracking_on_items.txt", mode="r", encoding="utf-8") as set_list:
        content_line = set_list.read().splitlines()
        for content in content_line:
            course_id, content_id = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_"+content_id+"_1&course_id=_"+course_id+"_1&dispatch=edit")

            try:
                driver.execute_script("document.getElementById('isTrack_true').click();")                
                driver.find_element(By.NAME, "bottom_Submit").click()
                driver.implicitly_wait(3)

                try:
                    driver.find_element(By.ID, "goodMsg1").text
                    print("Success: "+course_id+" "+content_id)
                    
                except:
                    print("Failed to set: "+course_id+" "+content_id)
                
            except:
                print("Failed to display: "+course_id+" "+content_id)

            


def main():
    driver = login()
    set_stats_tracking_on_items(driver)
    logout(driver)

main()
