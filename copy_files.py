from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def copy_files(driver):
    with open("copy_files.txt", mode="r", encoding="utf8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            new_directory = content_array[0]
            old_directory = content_array[1]
            list_of_files = content_array[2].split("|")

            driver.get(my_domain+"/webapps/cmsmain/webui"+old_directory+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=1000&startIndex=1000")

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
                        driver.execute_script("document.querySelector(\"[value='"+old_directory+file+"']\").checked = true;")
                        #driver.find_element(By.XPATH, '//input[@value="'+old_directory+file+'"]').click()
                        #print(old_directory+file+" found")
                        if bool(found) == False:
                            found = True
                            
                    except:
                        #driver.execute_script("alert('"+old_directory+file+" not found')")
                        print(old_directory+file+" not found")
            
            if bool(found) == True:
                driver.execute_script("csfunctions.copyFiles('Recycle Bin')")
                driver.implicitly_wait(3)
                #driver.find_element(By.ID, "targetPath_CSFile").send_keys(new_directory)
                #driver.find_element(By.ID, "bottom_Submit").click()
                driver.execute_script("document.getElementById('targetPath_CSFile').value = '"+new_directory+"';document.getElementById('bottom_Submit').click()")
                driver.implicitly_wait(3)

                try:
                    #print(driver.find_element(By.ID, "goodMsg1").text)
                    print(driver.execute_script("document.getElementById('goodMsg1').innerText;"))
                except:
                    print("element not found")

def main():
    driver = login()
    copy_files(driver)
    logout(driver)

main()
