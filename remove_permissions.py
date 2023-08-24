from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def remove_permissions(driver):
    with open("remove_permissions.txt", mode="r", encoding="utf-8") as permission_list:
        permission_line = permission_list.read().splitlines()
        for permission_entry in permission_line:
            permission_array = permission_entry.split("\t")
            directory = permission_array[0]
            list_of_permissions = permission_array[1].split("|")

            driver.get(my_domain+"/webapps/cmsmain/webui"+directory+"?action=permissions&subaction=print&uniq=-jgbgk2&gobackto=dirListHere-")

            driver.implicitly_wait(3)

            found = False         
	
            if list_of_permissions[0] == "AllPermissions":
                try:
                    driver.find_element(By.ID, "listContainer_selectAll").click()
                    if bool(found) == False:
                        found = True
                    
                except NoSuchElementException:
                    print("'Click All' not found")  
                    
            else:
                for permission in list_of_permissions:
                    try:
                        driver.find_element(By.ID, "listContainer_"+permission+"@RemoveT").click()
                        if bool(found) == False:
                            found = True
                            
                    except:
                        print(directory+permission+" not found")
            
            if bool(found) == True:
                driver.find_element(By.ID, "listContainer_link_removePermissionAction_top").click()

                confirmation = driver.switch_to.alert
                confirmation.accept()
                                
                driver.implicitly_wait(3)

                
                #try:
                #      WebDriverWait(driver, 8).until(EC.alert_is_present(),
                #                     'Timed out waiting for PA creation ' +
                #                     'confirmation popup to appear.')
                #      alert = driver.switch_to.alert
                #      alert.accept()
                #except TimeoutException:
                #      pass


                try:
                    print(driver.find_element(By.ID, "goodMsg1").text)
                except:
                    print("element not found")

def main():
    driver = login()
    remove_permissions(driver)
    logout(driver)

main()
