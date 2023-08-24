from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def edit_announcement(driver):
    with open("edit_announcement.txt", mode="r", encoding="utf-8") as edit_list:
        question_line = edit_list.read().splitlines()
        for question in question_line:
            course_pk1, announcement_pk1, fix_contents = question.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/announcement?method=edit&editMode=true&viewChoice=2&searchSelect=_"+course_pk1+"_1&context=course&course_id=_"+course_pk1+"_1&internalHandle=cp_announcements&announcementId=_"+announcement_pk1+"_1")
        
            driver.execute_script("jQuery('#messagetext').val(`"+fix_contents+"`);")
            driver.execute_script("document.getElementById('isPermanent_false').click();")
            driver.execute_script("document.getElementById('pushNotify_true').checked = false;")

            time.sleep(1)

            try:
                driver.find_element(By.NAME, "bottom_Submit").click()
                
            except NoSuchElementException:
                print("Failed to submit: "+course_pk1+" "+announcement_pk1)

            try:
                time.sleep(1)
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+announcement_pk1)
                
            except:
                print("Failed to edit: "+course_pk1+" "+announcement_pk1)


def main():
    driver = login()
    edit_announcement(driver)
    logout(driver)

main()
