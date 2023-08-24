from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def edit_announcement_find_replace(driver):
    with open("edit_announcement_find_replace.txt", mode="r", encoding="utf-8") as edit_list:
        announcement_line = edit_list.read().splitlines()
        for announcement in announcement_line:
            course_pk, announcement_pk, find, replace = announcement.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/announcement?method=edit&editMode=true&viewChoice=2&searchSelect=_"+course_pk+"_1&context=course&course_id=_"+course_pk+"_1&internalHandle=cp_announcements&announcementId=_"+announcement_pk+"_1")

            driver.execute_script("var text = document.getElementById('messagetext').value;text = text.replace(/"+find+"/g,`"+replace+"`);document.getElementById('messagetext').value = text;")
            driver.execute_script("document.getElementById('isPermanent_false').click();")
            driver.execute_script("document.getElementById('pushNotify_true').checked = false;")            

            try:
                driver.find_element(By.NAME, "bottom_Submit").click()
                
            except NoSuchElementException:
                print("Failed to submit: "+course_pk+" "+announcement_pk)

            try:
                time.sleep(1)
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk+" "+announcement_pk)
                
            except:
                print("Failed to edit: "+course_pk+" "+announcement_pk)


def main():
    driver = login()
    edit_announcement_find_replace(driver)
    logout(driver)

main()
