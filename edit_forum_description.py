from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def edit_forum_description(driver):
    with open("edit_forum_description.txt", mode="r", encoding="utf-8") as edit_list:
        forum_line = edit_list.read().splitlines()
        for forum in forum_line:
            course_pk1, forum_pk1, conf_pk1, fix_contents = forum.split("\t")

            driver.get(my_domain+"/webapps/discussionboard/do/forum?action=modify&course_id=_"+course_pk1+"_1&nav=cp_discussion_board&conf_id=_"+conf_pk1+"_1&forum_id=_"+forum_pk1+"_1")

            driver.execute_script("document.getElementById('descriptiontext').value=`"+fix_contents+"`;")
            driver.find_element(By.NAME, "bottom_Submit").click()

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+forum_pk1)
                
            except:
                print("Failed to edit: "+course_pk1+" "+forum_pk1)


def main():
    driver = login()
    edit_forum_description(driver)
    logout(driver)

main()
