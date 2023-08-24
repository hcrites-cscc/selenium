from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def reorder_content_item(driver):
    with open("reorder_content.txt", mode="r", encoding="utf-8") as creation_list:
        content_list = creation_list.read().splitlines()
        for content in content_list:
            course_pk1, parent_pk1, content_pk1, new_pos = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/content/listContentEditable.jsp?content_id=_"+parent_pk1+"_1&course_id=_"+course_pk1+"_1")

            nav_menu = driver.find_element(By.ID, "navsecondary").find_element(By.TAG_NAME, "li").find_element(By.TAG_NAME, "a").click()

            driver.execute_script("var mySelect = document.getElementById('pageListReorderControlSelect');var myOption = mySelect.querySelector('option[value=\"_"+content_pk1+"_1\"]');var myText = myOption.text;var myValue = '_"+content_pk1+"_1'; mySelect.removeChild(myOption);mySelect.options.add(new Option(myText, myValue), mySelect.options["+new_pos+"]);")

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

            print("Success: "+course_pk1+" "+content_pk1)
                
            

def main():
    driver = login()
    reorder_content_item(driver)
    logout(driver)

main()
