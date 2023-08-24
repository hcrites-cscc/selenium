from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def delete_columns(driver):
    with open("delete_specific_grade_center_column.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            course_pk1 = content_array[0]
            column_pk1 = content_array[1]

            driver.get(my_domain+"/webapps/gradebook/do/instructor/enterGradeCenter?course_id=_"+course_pk1+"_1")

            driver.execute_script("document.getElementsByName('itemId')[0].value='"+column_pk1+"'")
            driver.execute_script("document.getElementsByName('deleteColumnForm')[0].submit()")
            
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+column_pk1)
            except:
                print("Failed to delete: "+course_pk1+" "+column_pk1)

def main():
    driver = login()
    delete_columns(driver)
    logout(driver)

main()
