from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def add_permissions(driver):
    with open("add_permissions.txt", mode="r", encoding="utf-8") as permission_list:
        permission_line = permission_list.read().splitlines()
        for permission_entry in permission_line:
            directory, course_id, roles = permission_entry.split("\t")
            role_array = roles.split("|")

            driver.get(my_domain+"/webapps/cmsmain/webui"+directory+"?action=permissions&subaction=printfindcourseuserlist&uniq=-jfgos1&gobackto=dirListHere-")

            driver.implicitly_wait(3)

            driver.execute_script("document.getElementById('course_ids').value = '"+course_id.strip()+"';")

            for role in role_array:
                driver.execute_script("document.getElementById('"+role+"').checked = true;")
            
            driver.execute_script("document.getElementById('cascadeOverwrite').checked = true;")
            driver.find_element(By.ID, "bottom_Submit").click()

            try:
                print(directory+driver.find_element(By.ID, "goodMsg1").text)
            except:
                print("element not found")
                

def main():
    driver = login()
    add_permissions(driver)
    logout(driver)

main()
