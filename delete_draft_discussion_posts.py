from auth import *
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def delete_drafts(driver):
    with open("delete_draft_discussion_posts.txt", mode="r", encoding="utf-8") as thread_list:
        thread_line = thread_list.read().splitlines()
        for thread in thread_line:
            course_pk1, conf_pk1, forum_pk1, thread_pk1 = thread.split("\t")
            
            driver.get(my_domain+"/webapps/discussionboard/do/message?action=list_messages&course_id=_204057_1&nav=cp_discussion_board&conf_id=_44299_1&forum_id=_647839_1&message_id=_9766541_1")
            driver.implicitly_wait(3)

            try:
                messageForm = driver.find_element(By.NAME, "messageForm")
                driver.execute_script("document.messageForm.action = '/webapps/discussionboard/do/message?action=delete_post&do=remove&course_id=_"+course_pk1+"_1&nav=cp_discussion_board&conf_id="+conf_pk1+"&forum_id="+forum_pk1+"&thread_id=_"+thread_pk1+"_1db_thread_list_cp&nav=cp_discussion_board&message_id=_"+thread_pk1+"_1';document.messageForm.submit();")
                driver.implicitly_wait(3)
                
                try:
                    print(course_pk1+" "+conf_pk1+" "+driver.find_element(By.ID, "goodMsg1").text)
                except:
                    print(course_pk1+" "+conf_pk1+" failed")
                
            except:
                e = sys.exc_info()
                print(course_pk1+" "+conf_pk1+" no claim needed"+str(e))
           
            


def main():
    driver = login()
    delete_drafts(driver)
    logout(driver)

main()
