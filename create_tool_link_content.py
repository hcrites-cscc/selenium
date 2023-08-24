from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def create_tool_link_content(driver):
    with open("create_tool_link_content.txt", mode="r", encoding="utf-8") as edit_list:
        edit_list = edit_list.read().splitlines()
        for content in edit_list:
            tool_handle, course_pk1, parent_pk1, content_title, content_body, content_available, content_tracking = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/toolLinkProperties?type=tools&subtype=toolLinks&itemAction=add&rTool=content&course_id=_"+course_pk1+"_1&content_id=_"+parent_pk1+"_1&itemId="+tool_handle)

            driver.execute_script("document.getElementById('specific_link_name').value=`"+content_title+"`;")
            driver.execute_script("document.getElementById('link_desc_text').value=`"+content_body+"`;")

            if content_available == 'No':
                driver.execute_script("document.getElementById('make_visible_false').click();")

            if content_tracking == 'Yes':
                driver.execute_script("document.getElementById('track_views_true').click();")

            driver.find_element(By.NAME, "bottom_Submit").click()

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+content_title)
                
            except:
                print("Failed to edit: "+course_pk1+" "+content_title)


def main():
    driver = login()
    create_tool_link_content(driver)
    logout(driver)

main()
