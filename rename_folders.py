from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def rename_folders(driver):
    with open("rename_folders.txt", mode="r", encoding="utf-8") as rename_list:
        content_line = rename_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            folder_path = content_array[0]
            new_name = content_array[1]

            driver.get(my_domain+"/webapps/cmsmain/webui"+folder_path+"?action=details&subaction=bb_directorydetails&uniq=tv2n43&gobackto=dirList-")

            driver.implicitly_wait(3)

            found = False

            try:
                driver.find_element(By.ID, "newname").clear()
                
                if bool(found) == False:
                    found = True
                    
            except:
                #driver.execute_script("alert('"+old_directory+file+" not found')")
                print(folder_path+" not found")

            if bool(found) == True:

                driver.find_element(By.ID, "newname").clear()
                driver.find_element(By.ID, "newname").send_keys(new_name)

                driver.find_element(By.NAME, "bottom_Submit").click()

                driver.implicitly_wait(3)

                try:
                    driver.find_element(By.ID, "goodMsg1").text
                except :
                    print("Failed to update: "+folder_path)
                    driver.implicitly_wait(3)

 

def main():
    driver = login()
    rename_folders(driver)
    logout(driver)

main()
