from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def rename_files(driver):
    with open("rename_files.txt", mode="r", encoding="utf-8") as rename_list:
        content_line = rename_list.read().splitlines()
        for content in content_line:
            content_array = content.split("\t")
            file_path = content_array[0]
            new_name = content_array[1]

            driver.get(my_domain+"/webapps/cmsmain/webui"+file_path+"?action=details&subaction=print&&uniq=tv2n43&gobackto=docView-")

            driver.implicitly_wait(3)

            try:
                driver.execute_script("document.getElementById('newname').value = '"+new_name+"';document.getElementById('bottom_Submit').click();")

                driver.implicitly_wait(3)
                time.sleep(1)
                    
            except:
                #driver.execute_script("alert('"+old_directory+file+" not found')")
                print(file_path+" not found")

                
            try:
                print(driver.execute_script("document.write(document.getElementById('goodMsg1').text);"))
                
            except :
                print("Failed to update: "+file_path)
                driver.implicitly_wait(3)

 

def main():
    driver = login()
    rename_files(driver)
    logout(driver)

main()
