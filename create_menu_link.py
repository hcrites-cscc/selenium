from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

#link_info examples
#course_link: publishPickedLocation('278','NAVIGATION_ITEM','/Tools/Send Email/Select Users','false');return false;
#tool_link: blti-placement-tool-zoom-meeting

def create_menu_tem(driver):
    with open("create_menu_link.txt", mode="r", encoding="utf-8") as creation_list:
        menu_line = creation_list.read().splitlines()
        for menu in menu_line:
            link_type, course_pk, link_info, link_name, link_avail, link_pos = menu.split("\t")

            driver.get(my_domain+"/webapps/blackboard/landingPage.jsp?navItem=cp_evaluation&course_id=_"+course_pk+"_1")

            try:
                parent_window = driver.window_handles[0]

                if link_type=="course_link":
                
                    #------------------
                    # add course link
                    #------------------
                    driver.execute_script("document.getElementById('addCourseLinkButton').click();")
                    driver.find_element(By.NAME, "picker1").click()
                    child_window = driver.window_handles[1]
                    driver.switch_to.window(child_window)
                    driver.execute_script(link_info)
                    driver.switch_to.window(parent_window)
                    driver.execute_script("document.getElementById('addCourseLinkName').value = '"+link_name+"';")

                    if link_avail=='Y':
                        driver.find_element(By.ID, "course_link_availability_ckbox").click()

                    driver.find_element(By.ID, "addCourseLinkFormSubmit").click()

                elif link_type=="tool_link":
                    #------------------
                    # add tool link
                    #------------------
                    driver.execute_script("document.getElementById('addToolLinkButton').click();")
                    driver.execute_script("document.getElementById('addToolLinkName').value = '"+link_name+"';")
                    driver.find_element(By.ID, "toolSelect").click()
                    tool_select = Select(driver.find_element(By.ID, "toolSelect"))
                    tool_select.select_by_value(link_info)          

                    if link_avail=='Y':
                        driver.find_element(By.ID, "course_link_availability_ckbox").click()

                    driver.find_element(By.ID, "addToolLinkFormSubmit").click()

                # Reorder Menu
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
                    print("Success: "+course_pk+" "+link_name)
                    
                except Exception as e:
                    print("Failed to convert: "+course_pk+" "+link_name+" -- "+str(e))
                
            except Exception as e:
                print("Failed to display: "+course_pk+" "+link_name+" -- "+str(e))

            


def main():
    driver = login()
    create_menu_tem(driver)
    logout(driver)

main()
