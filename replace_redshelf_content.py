from auth import *
import time, re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def replace_redshelf_content(driver):
    with open("replace_redshelf_content.txt", mode="r", encoding="utf-8") as creation_list:
        content_line = creation_list.read().splitlines()
        for content in content_line:
            course_pk1, parent_pk1, old_content_pk1, content_name, content_tracking, content_avail, content_pos, content_body = content.split("\t")

            if delete_old_content_item(driver, course_pk1, parent_pk1, old_content_pk1, content_name)==True:
                create_new_content_item(driver, course_pk1, parent_pk1, content_name, content_tracking, content_avail, content_body, content_pos)
            else:
                print("Skipped: "+course_pk1+" "+old_content_pk1)


def create_new_content_item(driver, course_pk1, parent_pk1, content_name, content_tracking, content_avail, content_body, content_pos):
    
    driver.get(my_domain+"/webapps/blackboard/execute/blti/contentHandlerPlacement?cmd=create&blti_placement_id=_181_1&content_id=_"+parent_pk1+"_1&course_id=_"+course_pk1+"_1")

    if content_avail=="Y":
        availability = "true"
    else:
        availability = "false"

    if content_tracking=="N":
        tracking = "false"
    else:
        tracking = "true"
        
    driver.execute_script("document.getElementById('title').value = `"+content_name+"`;")
    driver.execute_script("document.getElementById('descriptiontext').value = `"+content_body+"`;")
    driver.execute_script("document.getElementById('available_"+availability+"').click();")
    driver.execute_script("document.getElementById('track_"+tracking+"').click();")
    
    driver.find_element(By.ID, "bottom_Submit").click()

    try:
        driver.find_element(By.ID, "goodMsg1")
        #print("Success: "+course_pk1+" "+content_name)
        reorder_new_content_item(driver, course_pk1, content_pos, content_name)
        
    except Exception as e:
        print("Failed to create: "+course_pk1+" "+content_name+" -- "+str(e))
        

def reorder_new_content_item(driver, course_pk1, content_pos, content_name):

    nav_menu = driver.find_element(By.ID, "navsecondary").find_element(By.TAGE_NAME, "li").find_element(By.TAGE_NAME, "a").click()

    driver.execute_script("var mySelect = document.getElementById('pageListReorderControlSelect');var lastValue = mySelect.options[mySelect.options.length - 1].value;var lastText = mySelect.options[mySelect.options.length - 1].text;mySelect.removeChild(mySelect.options[mySelect.options.length - 1]);mySelect.options.add(new Option(lastText, lastValue), mySelect.options["+content_pos+"]);")

    submit_button = driver.find_element(By.XPATH, "//body//div[@class=\"keyboardAccess\"]//div[@class=\"controls\"]//button[@class=\"button-3\"]").click()
    
    
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                       'Timed out waiting for PA creation ' +
                       'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.accept()

    except TimeoutException:
        pass

    driver.implicitly_wait(3)

    print("Success: "+course_pk1+" "+content_name)
        


def delete_old_content_item(driver, course_pk1, parent_pk1, old_content_pk1, content_name):

    driver.get(my_domain+"/webapps/blackboard/content/listContentEditable.jsp?content_id=_"+parent_pk1+"_1&course_id=_"+course_pk1+"_1")
    sleep(0.25)

    try:
        drop_down = driver.find_element(By.XPATH, "//div[@id='_"+old_content_pk1+"_1']/span/a")
        
    except NoSuchElementException:
        print("Not found: "+course_pk1+" "+content_id)
    
    except ElementNotInteractableException:
        try:
            sleep(1)
            drop_down = driver.find_element(By.XPATH, "//div[@id='_"+old_content_pk1+"_1']/span/a")
        except ElementNotInteractableException:
            print("Course not interact: "+course_pk1+" "+content_id)

    delete_id = drop_down.get_attribute("id").replace("cmlink_","")
    try:
        drop_down.click()
    except ElementNotInteractableException:
        sleep(1)
        try:
            drop_down.click()
        except ElementNotInteractableException:
            print("Course not interact: "+course_pk1+" "+old_content_pk1)

    except ElementClickInterceptedException:
        print("ElementClickInterceptedException: "+course_pk1+" "+old_content_pk1)
       

    try:
        driver.find_element(By.ID, "remove_"+delete_id).click()
    except NoSuchElementException:
        drop_down.click()
        try:
            driver.find_element(By.ID, "remove_"+delete_id).click()
        except NoSuchElementException:    
            print("Drop-down Failed: "+course_pk1+" "+old_content_pk1)

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
        #print("Success: "+course_pk1+" "+old_content_pk1)
        return True
    except :
        #print("Failed to update: "+course_pk1+" "+old_content_pk1)
        return False


def main():
    driver = login()
    replace_redshelf_content(driver)
    logout(driver)

main()
