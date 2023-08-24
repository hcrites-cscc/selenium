from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def replace_send_email(driver):
    with open("replace_send_email.txt", mode="r", encoding="utf-8") as creation_list:
        menu_line = creation_list.read().splitlines()
        for menu in menu_line:
            course_pk1, old_toc_pk1, link_script, link_name, link_avail, link_pos = menu.split("\t")

            if delete_old_menu_item(driver, course_pk1, old_toc_pk1, link_name)==True:
                create_new_menu_item(driver, course_pk1, link_script, link_name, link_avail, link_pos)
            else:
                print("Skipped: "+course_pk1+" "+old_toc_pk1)


def create_new_menu_item(driver, course_pk1, link_script, link_name, link_avail, link_pos):
    
    driver.get(my_domain+"/webapps/blackboard/landingPage.jsp?navItem=cp_evaluation&course_id=_"+course_pk1+"_1")

    try:
        parent_window = driver.window_handles[0]
        driver.find_element(By.ID, "addCmItem").click()
        driver.execute_script("document.getElementById('addCourseLinkButton').click();")

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "picker1"))
        )
        
        driver.find_element(By.NAME, "picker1").click()
        child_window = driver.window_handles[1]
        driver.switch_to.window(child_window)
        driver.execute_script(link_script)
        driver.switch_to.window(parent_window)

        if link_avail=='Y':
            driver.find_element(By.ID, "course_link_availability_ckbox").click()

        driver.execute_script("document.getElementById('addCourseLinkName').value = \""+link_name+"\";")
        driver.find_element(By.ID, "addCourseLinkFormSubmit").click()

        reorder_new_menu_item(driver, course_pk1, link_pos, link_name)
        
    except Exception as e:
        print("Failed to create: "+course_pk1+" "+link_name+" -- "+str(e))

def reorder_new_menu_item(driver, course_pk1, link_pos, link_name):

    driver.get(my_domain+"/webapps/blackboard/landingPage.jsp?navItem=cp_course_customization&course_id=_"+course_pk1+"_1")
    driver.find_element(By.ID, "courseMenuPalette_reorderControlLink").click()

    driver.execute_script("var mySelect = document.getElementById('courseMenuPalette_pageListReorderControlSelect');var lastValue = mySelect.options[mySelect.options.length - 1].value;var lastText = mySelect.options[mySelect.options.length - 1].text;mySelect.removeChild(mySelect.options[mySelect.options.length - 1]);mySelect.options.add(new Option(lastText, lastValue), mySelect.options["+link_pos+"]);changeAriaExpandedValue('courseMenuPalette_reorderControlLink');var reorderItemsPopupMenu = document.getElementById('reorderItemsPopupMenu');var controls = reorderItemsPopupMenu.lastChild;var submitButton = controls.lastChild.click();")
    
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
        driver.find_element(By.ID, "goodMsg1")
        print("Success: "+course_pk1+" "+link_name)
        
    except Exception as e:
        print("Failed to reorder: "+course_pk1+" "+link_name+" -- "+str(e))
        


def delete_old_menu_item(driver, course_pk1, toc_pk1, toc_title):
    driver.get(my_domain+"/webapps/blackboard/landingPage.jsp?navItem=cp_package_utillities&course_id=_"+course_pk1+"_1&filterForCourse=true")
    time.sleep(0.25)

    driver.execute_script("javascript:theCourseMenu.removeToc('_"+toc_pk1+"_1')")
    driver.implicitly_wait(3)

    try:
        driver.find_element(By.ID, "goodMsg1").text
        #print("Success: "+toc_pk1+" "+toc_title)
        return True
        
    except:
        #print("Failed to delete: "+toc_pk1+" "+toc_title)
        return False


def main():
    driver = login()
    replace_send_email(driver)
    logout(driver)

main()
