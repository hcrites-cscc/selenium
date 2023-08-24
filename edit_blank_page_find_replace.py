from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def edit_blank_page_find_replace(driver):
    with open("edit_blank_page_find_replace.txt", mode="r", encoding="utf-8") as edit_list:
        question_line = edit_list.read().splitlines()
        for question in question_line:
            course_pk1, content_pk1, find, replace = question.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/content/blankPage?cmd=view&content_id=_"+content_pk1+"_1&course_id=_"+course_pk1+"_1")
        
            driver.execute_script("var text = document.getElementById('bodytext').value;text = text.replace(/"+find+"/g,`"+replace+"`);document.getElementById('bodytext').value = text;")

            time.sleep(1)

            try:
                driver.find_element(By.NAME, "bottom_Submit").click()
                
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
    edit_blank_page_find_replace(driver)
    logout(driver)

main()
