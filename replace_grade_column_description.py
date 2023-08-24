from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def replace_description(driver):
    with open("replace_grade_column_description.txt", mode="r", encoding="utf-8") as column_list:
        column_line = column_list.read().splitlines()
        for column in column_line:
            course_id, column_id, replace_description = column.split("\t")    

            driver.get(my_domain+"/webapps/gradebook/do/instructor/addModifyItemDefinition?actionType=modify&course_id=_"+course_id+"_1&id="+column_id)

            driver.find_element(By.ID, "descriptiontext").clear()
            driver.execute_script("document.getElementById('descriptiontext').value = '"+replace_description.replace("'", "\'")+"';")

            driver.find_element(By.NAME, "bottom_Submit").click()
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_id+" "+column_id)
            except :
                print("Failed to update: "+course_id+" "+column_id)
        

def main():
    driver = login()
    replace_description(driver)
    logout(driver)

main()
