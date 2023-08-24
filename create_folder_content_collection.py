from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def create_folders(driver):
    with open("create_folder_content_collection.txt", mode="r", encoding="utf-8") as folder_list:
        folder_line = folder_list.read().splitlines()
        for folder in folder_line:
            folder_array = folder.split("\t")
            parent_directory = folder_array[0]
            new_directory = folder_array[1]

            driver.get(my_domain+"/webapps/cmsmain/webui"+parent_directory+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=10&startIndex=0")

            driver.implicitly_wait(3)

            driver.execute_script("document.getElementById('newAddFolderButton').click();")
            driver.execute_script("document.getElementById('newFolderName').value='"+new_directory+"'")
            driver.execute_script("document.getElementById('addFolderFormSubmit').disabled = false;document.getElementById('addFolderFormSubmit').click();")
                     
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
            except:
                print("Failed to create: "+parent_directory+"/"+new_directory)

def main():
    driver = login()
    create_folders(driver)
    logout(driver)

main()
