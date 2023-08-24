from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#all permissions: bAllowRead|bAllowWrite|bAllowDelete|bAllowManage
#roles: P, PE,DS, R, S, SI, U,

role_type = "course"
#role_type = "institution"


def edit_permissions(driver):
    with open("edit_permissions.txt", mode="r", encoding="utf-8") as permission_list:
        permission_line = permission_list.read().splitlines()
        for permission_entry in permission_line:
            directory, roles, permissions, course_id = permission_entry.split("\t")
            permission_array = permissions.split("|")
            role_array = roles.split("|")

            if role_type=="course":
                driver.get(my_domain+"/webapps/cmsmain/webui"+directory+"?action=permissions&uniq=-qfeycf&gobackto=dirListHere-&subaction=printfindcourseuserlist")

                driver.implicitly_wait(3)

                driver.execute_script("document.getElementById('course_ids').value = '"+course_id+"';")
                
                for role in role_array:
                    driver.execute_script("document.getElementById('"+role+"').checked = true;")
                
            elif role_type=="institution":
                driver.get(my_domain+"/webapps/cmsmain/webui"+directory+"?action=permissions&uniq=-qfeycf&gobackto=dirListHere-&subaction=printmodifypermissions&principal_id="+role_array[0].strip())

                driver.implicitly_wait(3)

            

            for permission in permission_array:
                driver.execute_script("document.getElementById('"+permission.strip()+"').checked = true;")
            
            driver.execute_script("document.getElementById('cascadeOverwrite').checked = true;")
            driver.find_element(By.ID, "bottom_Submit").click()                

            try:
                print(directory+driver.find_element(By.ID, "goodMsg1").text)
            except:
                print("element not found")
                

def main():
    driver = login()
    edit_permissions(driver)
    logout(driver)

main()
