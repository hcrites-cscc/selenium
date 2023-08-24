from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def move_files_except(driver):
    with open("move_files_except.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            new_directory = content_array[0]
            old_directory = content_array[1]
            list_of_files = list(dict.fromkeys(content_array[2].split("|")))

            driver.get(my_domain+"/webapps/cmsmain/webui"+old_directory+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=1000&startIndex=0")

            driver.implicitly_wait(3)

            found = False         
	
            row_count = len(driver.find_elements(By.XPATH, "//table[@id='listContainer_datatable']/tbody/tr"))

            if row_count > 0:
            
                try:
                    driver.find_element(By.ID, "listContainer_selectAll").click()
                    if bool(found) == False:
                        found = True
                    
                except NoSuchElementException:
                    print("No files found:", old_directory)  

            else:
                print("'Click All' not found")
                    
            
            for file in list_of_files:
                try:
                    driver.find_element(By.XPATH, "//input[@value=\""+old_directory+file+"\"]").click()
                    #print(old_directory+file+" found")
                    if bool(found) == False:
                        found = True
                        
                except:
                    #driver.execute_script("alert('"+old_directory+file+" not found')")
                    print(old_directory+file+" not found")
            
            if bool(found) == True:
                driver.execute_script("csfunctions.moveFiles('Recycle Bin')")
                popup = False
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
                    alert = driver.switch_to.alert
                    popup = True
                    alert.accept()
    
                except TimeoutException:
                    pass

                if bool(popup) == False:
                    driver.implicitly_wait(3)
                    driver.find_element(By.ID, "targetPath_CSFile").send_keys(new_directory)
                    driver.find_element(By.ID, "bottom_Submit").click()
                    driver.implicitly_wait(3)

                    try:
                        driver.find_element(By.ID, "goodMsg1").text
                    except:
                        print("Failed to move: "+old_directory+list_of_files[0])

def main():
    driver = login()
    move_files_except(driver)
    logout(driver)

main()
