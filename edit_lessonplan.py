from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def edit_lessonplan(driver):
    with open("edit_lessonplan.txt", mode="r", encoding="utf-8") as edit_list:
        question_line = edit_list.read().splitlines()
        for question in question_line:
            course_pk1, content_pk1, fix_contents = question.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/manageLessonPlan?dispatch=modify&content_id=_"+content_pk1+"_1&course_id=_"+course_pk1+"_1")
        
            driver.execute_script("jQuery('#htmlData_text').val(`"+fix_contents+"`);")

            time.sleep(1)

            try:
                driver.find_element(By.NAME, "bottom_Save and Exit").click()
                
            except NoSuchElementException:
                print("Failed to submit: "+course_pk1+" "+content_pk1)

            try:
                time.sleep(1)
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+content_pk1)
                
            except:
                print("Failed to edit: "+course_pk1+" "+content_pk1)


def main():
    driver = login()
    edit_lessonplan(driver)
    logout(driver)

main()
