from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

content_handlers = {
    "resource/x-bb-asmt-test-link": {
        "edit_url": my_domain+"/webapps/assessment/do/content/assessment?action=MODIFY&course_id=_[course_id]_1&content_id=_[content_id]_1&assessmentType=Test&method=modifyOptions",
        "text_name": "descriptiontext"
    },
    "resource/x-bb-asmt-survey-link": {
        "edit_url": my_domain+"/webapps/assessment/do/content/assessment?action=MODIFY&course_id=_[course_id]_1&content_id=_[content_id]_1&assessmentType=Survey&method=modifyOptions",
        "text_name": "descriptiontext"
    },
    "resource/x-bb-assignment": {
        "edit_url": my_domain+"/webapps/assignment/execute/manageAssignment?method=showmodify&content_id=_[content_id]_1&course_id=_[course_id]_1",
        "text_name": "content_desc_text"
    },
    "resource/x-bb-blankpage": {
        "edit_url": my_domain+"/webapps/blackboard/execute/content/blankPage?cmd=view&content_id=_[content_id]_1&course_id=_[course_id]_1",
        "text_name": "bodytext"
    },
    "resource/x-bb-blti-link": {
        "edit_url": my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_[content_id]_1&course_id=_[course_id]_1&dispatch=edit&type=externallink",
        "text_name": "htmlData_text"
    },
    "resource/x-bb-courselink": {
        "edit_url": my_domain+"/webapps/blackboard/content/manageCourseLink.jsp?content_id=_[content_id]_1&course_id=_[course_id]_1",
        "text_name": "htmlData_text"
    },
    "resource/x-bb-document": {
        "edit_url": my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_[content_id]_1&course_id=_[course_id]_1&dispatch=edit",
        "text_name": "htmlData_text"
    },
    "resource/x-bb-externallink": {
        "edit_url": my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_[content_id]_1&course_id=_[course_id]_1&dispatch=edit&type=externallink",
        "text_name": "htmlData_text"
    },
    "resource/x-bb-folder": {
        "edit_url": my_domain+"/webapps/blackboard/content/manageFolder.jsp?content_id=_[content_id]_1&course_id=_[course_id]_1",
        "text_name": "htmlData_text"
    },
    "resource/x-bb-forumlink": {
        "edit_url": my_domain+"/webapps/blackboard/execute/toolLinkProperties?itemAction=edit&content_id=_[content_id]_1&course_id=_[course_id]_1&type=forum",
        "text_name": "link_desc_text"
    },
    "resource/x-bb-lesson": {
        "edit_url": my_domain+"/webapps/blackboard/execute/manageLearningUnit?content_id=_[content_id]_1&course_id=_[course_id]_1",
        "text_name": "htmlData_text"
    },
    "resource/x-bb-module-page": {
        "edit_url": my_domain+"/webapps/blackboard/execute/modulepage/manageCourseModulePage?cmd=modify&content_id=_[content_id]_1&course_id=_[course_id]_1",
        "text_name": "descriptiontext"
    },
    "resource/x-osv-kaltura/mashup": {
        "edit_url": my_domain+"/webapps/osv-kaltura-bb_bb60/jsp/saMashupSettings.jsp?edit=true&course_id=_[course_id]_1&content_id=_[content_id]_1",
        "text_name": "descriptiontext"
        },
    "resource/x-bb-toollink": {
        "edit_url": my_domain+"/webapps/blackboard/execute/toolLinkProperties?itemAction=edit&content_id=_[content_id]_1&course_id=_[course_id]_1&type=tools",
        "text_name": "htmlData_text"
        },
    "resource/x-bb-image": {
        "edit_url": my_domain+"/webapps/blackboard/execute/content/media?cmd=edit&type=Image&content_id=_[content_id]_1&course_id=_[course_id]_1",
        "text_name": "htmlData_text"
    }
}

def replace_content(driver):
    global content_handlers
    with open("set_date_availability_content.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_id, content_id, content_handler, start_date, start_time = content.split("\t")    

            if content_handler in content_handlers.keys():
                edit_url = content_handlers[content_handler]["edit_url"].replace("[course_id]", course_id).replace("[content_id]", content_id)
                driver.get(edit_url)

                driver.execute_script("checkbox = document.getElementById('start_bbDateTimePicker'); if(!checkbox.checked) {checkbox.click();}")
                driver.find_element(By.ID, "dp_bbDateTimePicker_start_date").clear()
                driver.find_element(By.ID, "tp_bbDateTimePicker_start_time").clear()
                driver.execute_script("document.getElementById('dp_bbDateTimePicker_start_date').value = '"+start_date+"';")
                driver.execute_script("document.getElementById('tp_bbDateTimePicker_start_time').value = '"+start_time+"';")


                driver.find_element(By.NAME, "bottom_Submit").click()
                driver.implicitly_wait(3)

                try:
                    driver.find_element(By.ID, "goodMsg1").text
                except :
                    print("Failed to update: "+course_id+" "+content_id)
                    driver.implicitly_wait(3)
            else:
                print("Failed (no handler): "+content)
                driver.implicitly_wait(3)

def main():
    driver = login()
    replace_content(driver)
    logout(driver)

main()
