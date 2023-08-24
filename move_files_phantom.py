from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def copy_files(driver):
    with open("move_files_phantom.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            new_directory = content_array[0]
            old_directory = content_array[1]
            file_name = content_array[2]

            driver.get(my_domain+"/webapps/cmsmain/webui/institution/zz (Do Not Use) To Be Archived/")

            driver.implicitly_wait(3)

            found = False

            try:
                driver.find_element(By.XPATH, "//input[@value=\"/institution/zz (Do Not Use) To Be Archived/placeholder\"]").click()
                #print(old_directory+file+" found")
                if bool(found) == False:
                    found = True
            except:
                #driver.execute_script("alert('"+old_directory+file+" not found')")
                print(old_directory+file+" not found")

            
            if bool(found) == True:
                driver.execute_script("csfunctions.moveFiles('Recycle Bin')")
                driver.implicitly_wait(3)
                driver.find_element(By.ID, "targetPath_CSFile").send_keys(new_directory)
                driver.execute_script("document.getElementById('file0').value='"+old_directory+file_name+"'")
                driver.find_element(By.ID, "bottom_Submit").click()
                driver.implicitly_wait(3)

                try:
                    driver.find_element(By.ID, "goodMsg1").text
                except:
                    print("Failed to move: "+old_directory+file_name)

def main():
    driver = login()
    copy_files(driver)
    logout(driver)

main()
