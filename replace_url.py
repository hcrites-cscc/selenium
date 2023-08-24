from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def replace_content(driver):
    global content_handlers
    with open("replace_url.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_id, content_id, replace_content = content.split("\t")    

            driver.get(my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_"+content_id+"_1&course_id=_"+course_id+"_1&dispatch=edit&type=externallink")

            is_lti = "N"
            if(driver.find_element(By.ID, "bltiToolProvider").is_selected()):
                is_lti = "Y"
                #is_eval = "N"
                #if(driver.find_element(By.ID, "gradingOptions_enabledYesId").is_selected()):
                    #is_eval = "Y"
                    #points_possible = driver.find_element(By.ID, "gradingOptions_possible").get_attribute('value')
                    #is_visible = "visibleToStudentsNo";
                    #if(driver.find_element(By.ID, "visibleToStudentsYes").is_selected()):
                        #is_visible = "visibleToStudentsYes";

                    #is_due_date = "N"
                    #if(driver.find_element(By.ID, "gradingOptions_dueDate_in_use").is_selected()):
                        #is_due_date = "Y"
                        #due_date = driver.find_element(By.ID, "dp_gradingOptions_dueDate_date").get_attribute('value')
                        #due_time = driver.find_element(By.ID, "tp_gradingOptions_dueDate_time").get_attribute('value')


            driver.find_element(By.ID, "url").clear()
            driver.find_element(By.ID, "url").send_keys(replace_content)

            if(is_lti=="Y"):
                driver.find_element(By.ID, "bltiToolProvider").click()
                #if(is_eval=="Y"):
                    #driver.find_element(By.ID, "gradingOptions_possible").send_keys(points_possible)
                    #driver.find_element(By.ID, is_visible).click()
                    #if(is_due_date=="Y"):
                        #driver.find_element(By.ID, "gradingOptions_dueDate_in_use").click()
                        #driver.find_element(By.ID, "dp_gradingOptions_dueDate_date").send_keys(due_date)
                        #driver.find_element(By.ID, "tp_gradingOptions_dueDate_time").send_keys(due_time)

            driver.execute_script("document.getElementById('launchInNew_true').checked = true;")
            driver.find_element(By.NAME, "bottom_Submit").click()
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_id+" "+content_id)
            except :
                print("Failed to update: "+course_id+" "+content_id)
                driver.implicitly_wait(3)

def main():
    driver = login()
    replace_content(driver)
    logout(driver)

main()
