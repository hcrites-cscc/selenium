from auth import *
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def claim_posts(driver):
    with open("claim_anonymous_posts.txt", mode="r", encoding="utf-8") as conf_list:
        conf_line = conf_list.read().splitlines()
        for conf in conf_line:
            course_pk1, conf_pk1, enrollment_pk1 = conf.split("\t")

            driver.get(my_domain+"/webapps/discussionboard/do/conference?action=list_forums&course_id=_"+course_pk1+"_1&nav=cp_discussion_board&conf_id="+conf_pk1)           
            driver.implicitly_wait(3)

            try:
                #conf_pk1 = conf_pk1
                #conf_pk1 = conf_pk1
                select = Select(driver.find_element(By.ID, "deAnonymizeAuthorSelectId"))
                select.select_by_value("_"+enrollment_pk1+"_1")
                driver.find_element(By.NAME, "bottom_Submit").click()
                
                try:
                    print(course_pk1+" "+conf_pk1+" "+driver.find_element(By.ID, "goodMsg1").text)
                except:
                    print(course_pk1+" "+conf_pk1+" failed")
                
            except:
                e = sys.exc_info()
                print(course_pk1+" "+conf_pk1+" no claim needed"+str(e))
           
            


def main():
    driver = login()
    claim_posts(driver)
    logout(driver)

main()
