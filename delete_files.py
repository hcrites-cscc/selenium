from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def delete_files(driver):
    with open("delete_files.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            directory = content_array[0]
            list_of_files = content_array[1].split("|")

            driver.get(my_domain+"/webapps/cmsmain/webui"+directory+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=1000&startIndex=1000")

            driver.implicitly_wait(3)

            found = False         
	
            if list_of_files[0] == "AllFiles":
                try:
                    driver.find_element(By.ID, "listContainer_selectAll").click()
                    if bool(found) == False:
                        found = True
                    
                except NoSuchElementException:
                    print("'Click All' not found")  
                    
            else:
                for file in list_of_files:
                    try:
                        driver.execute_script("document.querySelector(\"[value='"+directory+file+"']\").checked = true;")
                        #driver.find_element(By.XPATH, "//input[@value='"+directory+file+"']").click()
                        #print(old_directory+file+" found")
                        if bool(found) == False:
                            found = True
                            
                    except:
                        #driver.execute_script("alert('"+old_directory+file+" not found')")
                        print(directory+file+" not found")
            
            if bool(found) == True:
                driver.execute_script("csfunctions.deleteFilesFolders();")

                confirmation = driver.switch_to.alert
                confirmation.accept()
                                
                driver.implicitly_wait(3)

                try:
                    driver.execute_script("document.getElementById('goodMsg1').text;")
                except:
                    print("element not found")

def main():
    driver = login()
    delete_files(driver)
    logout(driver)

main()
