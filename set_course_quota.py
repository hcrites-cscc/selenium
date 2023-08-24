from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def set_course_quota(driver):
    with open("set_course_quota.txt", mode="r", encoding="utf-8") as quota_list:
        course_lines = quota_list.read().splitlines()
        for course_pk1 in course_lines:
            
            driver.get(my_domain+"/webapps/blackboard/execute/course/diskQuota/manage?course_id=_"+course_pk1+"_1&dispatch=viewDiskQuotaSettings")

            driver.implicitly_wait(3)

            try:
                driver.execute_script('''
                    document.getElementById('limited_disk_size').click();
                    document.getElementById('maxDiskSize').value = 1000;
                    document.getElementById('soft_limit_on').click();
                    document.getElementById('softLimitSize').value = 800;
                    document.getElementById('limited_legacy_size').click();
                    document.getElementById('maxLegacySize').value = 1000;
                    ''')

                driver.implicitly_wait(3)
                
                driver.find_element(By.ID, "bottom_Submit").click()

                try:
                    driver.find_element(By.ID, "goodMsg1").text
                    print("Success: "+course_pk1)
                    
                except :
                    print("Failed to update: "+course_pk1)
                    driver.implicitly_wait(3)
                    
            except Exception as e:
                print(str(e))
                print(course_pk1+" not found")



 

def main():
    driver = login()
    set_course_quota(driver)
    logout(driver)

main()
