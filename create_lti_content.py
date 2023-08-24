from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def create_lti_content(driver):
    with open("create_lti_content.txt", mode="r", encoding="utf-8") as edit_list:
        edit_list = edit_list.read().splitlines()
        for content in edit_list:
            lti_pk1, course_pk1, parent_pk1, content_title, content_body, content_available, content_tracking, eval_ind, points_possible, visible_ind, due_date_ind, due_date, due_time = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/blti/contentHandlerPlacement?cmd=create&blti_placement_id=_"+lti_pk1+"_1&content_id=_"+parent_pk1+"_1&course_id=_"+course_pk1+"_1")

            driver.execute_script("document.getElementById('title').value=`"+content_title+"`;")
            driver.execute_script("document.getElementById('descriptiontext').value=`"+content_body+"`;")

            if eval_ind == 'Y':
                driver.execute_script("document.getElementById('gradingOptions_enabledYesId').click();")
                driver.execute_script("document.getElementById('gradingOptions_possible').value = '"+points_possible+"';")

                if visible_ind == 'N':
                    driver.execute_script("document.getElementById('visibleToStudentsNo').value = '"+points_possible+"';")

                if due_date_ind == 'Y':
                    driver.execute_script("document.getElementById('gradingOptions_dueDate_in_use').click();")
                    driver.execute_script("document.getElementById('dp_gradingOptions_dueDate_date').value = '"+due_date+"';")
                    driver.execute_script("document.getElementById('tp_gradingOptions_dueDate_time').value = '"+due_time+"';")
                

            if content_available == 'N':
                driver.execute_script("document.getElementById('available_false').click();")

            if content_tracking == 'Y':
                driver.execute_script("document.getElementById('track_true').click();")

            driver.find_element(By.NAME, "bottom_Submit").click()

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+content_title)
                
            except:
                print("Failed to edit: "+course_pk1+" "+content_title)


def main():
    driver = login()
    create_lti_content(driver)
    logout(driver)

main()
