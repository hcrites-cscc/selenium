from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException        

def edit_pool_question(driver):
    with open("edit_pool_question.txt", mode="r", encoding="utf-8") as edit_list:
        question_line = edit_list.read().splitlines()
        for question in question_line:
            course_pk1, pool_pk1, question_pk1, question_body = question.split("\t")

            driver.get(my_domain+"/webapps/assessment/do/authoring/modifyAssessment?method=modifyAssessment&copyAlignments=false&course_id=_"+course_pk1+"_1&assessmentId=_"+pool_pk1+"_1&saveAsNew=false&createAnother=false&assessmentType=Pool")

            driver.execute_script("assessment.modifyQuestion('"+question_pk1+"');")
            driver.implicitly_wait(3)

            driver.execute_script("document.getElementsByName('questionText.text')[0].value=`"+question_body+"`")


            try:
                driver.find_element(By.NAME, "bottom_Submit").click()
            except NoSuchElementException:
                try:
                    driver.find_element(By.NAME, "bottom_Submit and Update Attempts").click()
                except NoSuchElementException:
                    print("Failed to submit: "+course_pk1+" "+question_pk1)
                    continue         

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+question_pk1)
                
            except:
                print("Failed to edit: "+course_pk1+" "+question_pk1)


def main():
    driver = login()
    edit_pool_question(driver)
    logout(driver)

main()
