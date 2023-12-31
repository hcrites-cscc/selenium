from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def delete_menu_item(driver):
    with open("delete_menu_item.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_pk1, toc_pk1, toc_title = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/landingPage.jsp?navItem=cp_package_utillities&course_id=_"+course_pk1+"_1&filterForCourse=true")
            time.sleep(1.25)

            driver.execute_script("javascript:theCourseMenu.removeToc('_"+toc_pk1+"_1')")
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+toc_pk1+" "+toc_title)
                
            except:
                print("Failed to delete: "+toc_pk1+" "+toc_title)

def main():
    driver = login()
    delete_menu_item(driver)
    logout(driver)

main()
