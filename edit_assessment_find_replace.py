from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def edit_assessment_find_replace(driver):
    with open("edit_assessment_find_replace.txt", mode="r", encoding="utf-8") as edit_list:
        question_line = edit_list.read().splitlines()
        for question in question_line:
            course_pk1, test_pk1, fix_type, find, replace = question.split("\t")

            driver.get(my_domain+"/webapps/assessment/do/authoring/modifyAssessment?method=modifyAssessment&copyAlignments=false&course_id=_"+course_pk1+"_1&assessmentId=_"+test_pk1+"_1&saveAsNew=false&createAnother=false&assessmentType=Test")

            driver.execute_script("assessment.modifyAssessmentInfo();")
            driver.implicitly_wait(3)

            # instructionstext = instructions (first in xml)
            # descriptiontext = description (second in xml)

            driver.execute_script("var text = document.getElementById('"+fix_type+"text').value;text = text.replace(/"+find+"/g,`"+replace+"`);document.getElementById('"+fix_type+"text').value = text;")

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
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+course_pk1+" "+test_pk1+" "+assessment_type)
                
            except:
                print("Failed to edit: "+course_pk1+" "+test_pk1+" "+assessment_type)


def main():
    driver = login()
    edit_assessment_find_replace(driver)
    logout(driver)

main()
