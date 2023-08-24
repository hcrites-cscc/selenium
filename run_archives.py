from auth import *
from selenium import webdriver
from selenium.webdriver.common.by import By

def run_archives(driver):
    with open("run_archives.txt", mode="r", encoding="utf-8") as copy_list:
        course_line = copy_list.read().splitlines()
        for course in course_line:
            
            driver.get(my_domain+"/webapps/blackboard/execute/contentExchange?navItem=cp_archive_course&course_id=_"+course+"_1&contextNavItem=control_panel")
            driver.implicitly_wait(3)

            driver.find_element(By.ID, "includeLog").click()

            driver.find_element(By.ID, "bottom_Submit").click()
            driver.implicitly_wait(5)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course)
            except:
                print("Failure: "+course)

def main():
    driver = login()
    run_archives(driver)
    logout(driver)

main()
