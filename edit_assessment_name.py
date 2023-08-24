from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def edit_assessment_name(driver):
    with open("edit_assessment_name.txt", mode="r", encoding="utf-8") as edit_list:
        question_line = edit_list.read().splitlines()
        for question in question_line:
            course_pk1, test_pk1, new_name = question.split("\t")

            driver.get(my_domain+"/webapps/assessment/do/authoring/modifyAssessment?method=modifyAssessment&copyAlignments=false&course_id=_"+course_pk1+"_1&assessmentId=_"+test_pk1+"_1&saveAsNew=false&createAnother=false&assessmentType=Test")

            driver.execute_script("assessment.modifyAssessmentInfo();")
            driver.implicitly_wait(3)

            driver.execute_script("document.getElementById('assessment_name_input').value=`"+new_name+"`;")
            assessment_type = ""

            try:
                driver.find_element(By.NAME, "bottom_Submit").click()
                assessment_type = ""
                
            except NoSuchElementException:
                try:
                    driver.find_element(By.NAME, "bottom_Submit and Update Attempts").click()
                    assessment_type = "attempts"
                   
                except NoSuchElementException:
                    print("Failed to submit: "+course_pk1+" "+question_pk1)
                    continue         

            try:
                driver.execute_script("document.getElementById('goodMsg1').text;")
                print("Success: "+course_pk1+" "+test_pk1+" "+assessment_type)
                
            except:
                print("Failed to edit: "+course_pk1+" "+test_pk1+" "+assessment_type)


def main():
    driver = login()
    edit_assessment_name(driver)
    logout(driver)

main()
