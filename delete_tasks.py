from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def delete_tasks(driver):
    with open("delete_tasks.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_pk1, task_list = content.split("\t")
            list_of_tasks = task_list.split("|")

            driver.get(my_domain+"/webapps/blackboard/execute/taskEditList?course_id=_"+course_pk1+"_1&mode=edit&editPaging=true&numResults=1000")

            found = False

            for task in list_of_tasks:
                try:
                    driver.find_element(By.ID, "listContainer_task_id_"+task+"_1C_"+course_pk1+"_1").click()
                    if bool(found) == False:
                        found = True
                except:
                    #driver.execute_script("alert('"+old_directory+file+" not found')")
                    print(task+" not found")

            try:
                driver.execute_script("document.tasksForm.method.value='delete';document.tasksForm.submit();")

                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1)            
                
            except TimeoutException:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1)            
                          
            except:
                print("Failed to delete: "+course_pk1)

def main():
    driver = login()
    driver.set_page_load_timeout(3)
    delete_tasks(driver)
    logout(driver)

main()
