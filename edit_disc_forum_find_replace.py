from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def edit_disc_forum_find_replace(driver):
    with open("edit_disc_forum_find_replace.txt", mode="r", encoding="utf-8") as edit_list:
        forum_line = edit_list.read().splitlines()
        for forum in forum_line:
            course_pk, forum_pk, conf_pk, find, replace = forum.split("\t")

            driver.get(my_domain+"/webapps/discussionboard/do/forum?action=modify&course_id=_"+course_pk+"_1&nav=cp_discussion_board&conf_id=_"+conf_pk+"_1&forum_id=_"+forum_pk+"_1")

            driver.execute_script("var text = document.getElementById('descriptiontext').value;text = text.replace(/"+find+"/g,`"+replace+"`);document.getElementById('descriptiontext').value = text;")

            try:
                driver.find_element(By.NAME, "bottom_Submit").click()
                
            except NoSuchElementException:
                print("Failed to submit: "+course_pk+" "+forum_pk)

            try:
                time.sleep(1)
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk+" "+forum_pk)
                
            except:
                print("Failed to edit: "+course_pk+" "+forum_pk)


def main():
    driver = login()
    edit_disc_forum_find_replace(driver)
    logout(driver)

main()
