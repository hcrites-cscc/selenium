from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def copy_files(driver):
    with open("move_files.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            new_directory = content_array[0]
            old_directory = content_array[1]
            list_of_files = list(dict.fromkeys(content_array[2].split("|")))

            driver.get(my_domain+"/webapps/cmsmain/webui"+old_directory+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=1000&startIndex=29000")

            driver.implicitly_wait(3)

            found = False         
	
            if list_of_files[0] == "AllFiles":
                row_count = len(driver.find_elements_by_xpath("//table[@id='listContainer_datatable']/tbody/tr"))

                if row_count > 0:
                
                    try:
                        driver.find_element(By.ID, "listContainer_selectAll").click()
                        if bool(found) == False:
                            found = True
                        
                    except NoSuchElementException:
                        print("No files found:", old_directory)  

                else:
                    print("'Click All' not found")
                    
            else:
                for file in list_of_files:
                    try:
                        driver.execute_script("document.querySelector(\"[value='"+old_directory+file+"']\").checked = true;")
                        #print(old_directory+file+" found")
                        if bool(found) == False:
                            found = True
                            
                    except:
                        #driver.execute_script("alert('"+old_directory+file+" not found')")
                        print(old_directory+file+" not found")
            
            if bool(found) == True:
                driver.execute_script("csfunctions.moveFiles('Recycle Bin')")
                driver.implicitly_wait(3)
                driver.execute_script("document.getElementById('targetPath_CSFile').value = '"+new_directory+"';document.getElementById('bottom_Submit').click()")
                driver.implicitly_wait(3)

                try:
                    print(driver.execute_script("document.getElementById('goodMsg1').innerText;"))
                except:
                    print("Failed to move: "+old_directory+list_of_files[0])

def main():
    driver = login()
    copy_files(driver)
    logout(driver)

main()
