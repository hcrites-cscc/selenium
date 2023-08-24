from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def reorder_menu_item(driver):
    with open("reorder_menu_item.txt", mode="r", encoding="utf-8") as creation_list:
        menu_line = creation_list.read().splitlines()
        for menu in menu_line:
            course_pk1, toc_pk1, current_pos, new_pos = menu.split("\t")

            driver.get(my_domain+"/webapps/blackboard/landingPage.jsp?navItem=cp_evaluation&course_id=_"+course_pk1+"_1")
            driver.find_element(By.ID, "courseMenuPalette_reorderControlLink").click()

            driver.execute_script("var mySelect = document.getElementById('courseMenuPalette_pageListReorderControlSelect');var myValue = mySelect.options["+current_pos+"].value;var myText = mySelect.options["+current_pos+"].text;mySelect.removeChild(mySelect.options["+current_pos+"]);mySelect.options.add(new Option(myText, myValue), mySelect.options["+new_pos+"]);changeAriaExpandedValue('courseMenuPalette_reorderControlLink');var reorderItemsPopupMenu = document.getElementById('reorderItemsPopupMenu');var controls = reorderItemsPopupMenu.lastChild;var submitButton = controls.lastChild.click();")
            
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                               'Timed out waiting for PA creation ' +
                               'confirmation popup to appear.')
                alert = driver.switch_to.alert
                alert.accept()

            except TimeoutException:
                pass

            driver.implicitly_wait(3)

            print("Success: "+course_pk1+" "+toc_pk1)
                
            

def main():
    driver = login()
    reorder_menu_item(driver)
    logout(driver)

main()
