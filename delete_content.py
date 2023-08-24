from auth import *
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

def delete_content(driver):
    with open("delete_content.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_id, parent_id, content_id = content.split("\t")    

            driver.get(my_domain+"/webapps/blackboard/content/listContentEditable.jsp?content_id=_"+parent_id+"_1&course_id=_"+course_id+"_1")
            sleep(0.25)

            try:
                drop_down = driver.find_element(By.XPATH, "//div[@id='_"+content_id+"_1']/span/a")
            except NoSuchElementException:
                print("Not found: "+course_id+" "+content_id)
                continue
            except ElementNotInteractableException:
                try:
                    sleep(1)
                    drop_down = driver.find_element(By.XPATH, "//div[@id='_"+content_id+"_1']/span/a")
                except ElementNotInteractableException:
                    print("Course not interact: "+course_id+" "+content_id)
                    continue

            delete_id = drop_down.get_attribute("id").replace("cmlink_","")
            try:
                drop_down.click()
            except ElementNotInteractableException:
                sleep(1)
                try:
                    drop_down.click()
                except ElementNotInteractableException:
                    print("Course not interact: "+course_id+" "+content_id)
                    continue
            except ElementClickInterceptedException:
                print("ElementClickInterceptedException: "+course_id+" "+content_id)
                continue
                

            try:
                driver.find_element(By.ID, "remove_"+delete_id).click()
            except NoSuchElementException:
                drop_down.click()
                try:
                    driver.find_element(By.ID, "remove_"+delete_id).click()
                except NoSuchElementException:    
                    print("Drop-down Failed: "+course_id+" "+content_id)
                    continue

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                               'Timed out waiting for PA creation ' +
                               'confirmation popup to appear.')
                alert = driver.switch_to.alert
                alert.accept()

            except TimeoutException:
                pass
            
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_id+" "+content_id)
            except :
                print("Failed to update: "+course_id+" "+content_id)
                driver.implicitly_wait(3)


def main():
    driver = login()
    delete_content(driver)
    logout(driver)

main()
