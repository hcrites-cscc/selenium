from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def copy_courses(driver):
    with open("copy_courses.txt", mode="r", encoding="utf-8") as copy_list:
        copy_line = copy_list.read().splitlines()
        for copy in copy_line:
            source, destination = copy.split("\t")
            
            driver.get(my_domain+"/webapps/blackboard/execute/copy_content?navItem=copy_course_content_exists&target=yes&type=course")

            source_field = driver.find_element(By.ID, "sourceCourseId")
            source_field.click()
            source_field.clear()
            source_field.send_keys(source)
            
            driver.implicitly_wait(1)
            
            destination_field = driver.find_element(By.ID, "destinationCourseId")
            destination_field.click()
            destination_field.clear()
            destination_field.send_keys(destination)
            
            driver.find_element(By.ID, "bottom_Submit").click()
            driver.implicitly_wait(3)
            
            driver.execute_script("selectAll(false, true);return false;")

            body = driver.find_element(By.CSS_SELECTOR, 'body')
            body.click()
            body.send_keys(Keys.CONTROL+Keys.END)

            driver.find_element(By.ID, "copyLinkToCourseFilesAndCopiesOfContent").click()
            #driver.find_element(By.ID, "bottom_Submit").click()
            driver.execute_script("document.getElementById('bottom_Submit').click();")
            driver.implicitly_wait(5)

            try:
                print(driver.find_element(By.ID, "goodMsg1").text)
            except:
                print("Failed: "+source+" into "+destination)

def main():
    driver = login()
    copy_courses(driver)
    logout(driver)

main()
