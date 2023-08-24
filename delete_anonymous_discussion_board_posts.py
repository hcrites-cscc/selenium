from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def delete_threads(driver):
    with open("delete_anonymous_discussion_board_posts.txt", mode="r", encoding="utf-8") as forum_list:
        forum_line = forum_list.read().splitlines()
        for forum in forum_line:
            course_pk1, conf_pk1, forum_pk1, thread_pk1_list = forum.split("\t")
            list_of_threads = thread_pk1_list.split("|")

            driver.get(my_domain+"/webapps/discussionboard/do/forum?action=list_threads&filterAction=ALL&showAll=true&course_id=_"+course_pk1+"_1&nav=cp_discussion_board&conf_id=_"+conf_pk1+"_1&forum_id=_"+forum_pk1+"_1&editPaging=true&numResults=1000")
            driver.implicitly_wait(3)

            document_body = driver.find_element(By.ID, "containerdiv").text

            if document_body.find("No items found.") >= 0:
                print(course_pk1+" "+conf_pk1+" "+forum_pk1+" empty")

            else:

                found = False         
            
                if list_of_threads[0] == "AllThreads":
                    try:
                        driver.find_element(By.ID, "listContainer_selectAll").click()
                        if bool(found) == False:
                            found = True
                        
                    except NoSuchElementException:
                        print("'Click All' not found")  
                        
                else:
                    for thread in list_of_threads:
                        try:
                            driver.find_element(By.XPATH, "//input[@value='"+thread+"']").click()
                            if bool(found) == False:
                                found = True
                                
                        except:
                            print(course_pk1+" "+conf_pk1+" "+forum_pk1+" "+thread+" not found")
                
                if bool(found) == True:
                    driver.execute_script("document.forumForm.action = 'forum?action=deleteThread&do=delete&requestType=thread&forum_title=&course_id=_"+course_pk1+"_1&nav=cp_discussion_board&conf_id=_"+conf_pk1+"_1&forum_id=_"+forum_pk1+"_1';document.forumForm.submit();")
                    driver.implicitly_wait(3)

                    try:
                        print(driver.find_element(By.ID, "goodMsg1").text)
                    except:
                        print("element not found")

def main():
    driver = login()
    delete_threads(driver)
    logout(driver)

main()
