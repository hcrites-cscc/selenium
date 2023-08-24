from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def rename_files(driver):
    with open("edit_file_permissions.txt", mode="r", encoding="utf-8") as rename_list:
        content_line = rename_list.read().splitlines()
        for content in content_line:
            file_path, user_id = content.split("\t")

            driver.get(my_domain+"/webapps/cmsmain/webui"+file_path+"?action=permissions&subaction=printmodifypermissions&uniq=vebruz&gobackto=dirList-&principal_id="+user_id)

            driver.implicitly_wait(3)

            driver.execute_script("document.getElementById('bAllowRead').checked = true;document.getElementById('bAllowWrite').checked = true;document.getElementById('bAllowDelete').checked = true;document.getElementById('bAllowManage').checked = true;")
            driver.find_element(By.NAME, "bottom_Submit").click()

            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
            except :
                print("Failed to update: "+file_path)
                driver.implicitly_wait(3)

 

def main():
    driver = login()
    rename_files(driver)
    logout(driver)

main()
