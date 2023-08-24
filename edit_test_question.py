from auth import *
import time, html, codecs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def edit_test_question(driver):
    with open("edit_test_question.txt", mode="r", encoding="utf-8") as edit_list:
        question_line = edit_list.read().splitlines()
        for question in question_line:
            course_pk1, question_pk1, test_pk1, question_body = question.split("\t")
            question_body = codecs.escape_decode(bytes(html.unescape(question_body), "utf-8"))[0].decode("utf-8")

            driver.get(my_domain+"/webapps/assessment/do/authoring/modifyAssessment?method=modifyAssessment&copyAlignments=false&course_id=_"+course_pk1+"_1&assessmentId=_"+test_pk1+"_1&saveAsNew=false&createAnother=false&assessmentType=Test")

            driver.execute_script("assessment.modifyQuestion('"+question_pk1+"');")
            driver.implicitly_wait(3)

            #WebDriverWait(driver, 300).until(EC.url_contains("course_id"))

            assessment_type = ""
            # question text
            driver.execute_script("""document.getElementsByName('questionText.text')[0].value=`"""+question_body+"""`;""")
            # correct response feedback
            #driver.execute_script("""document.getElementsByName('correctFeedbackForm.textForm.text')[0].value=`"""+question_body+"""`;""")
           
           
            try:
                driver.find_element(By.NAME, "bottom_Submit").click()
                assessment_type = ""
                
            except NoSuchElementException:
                try:
                    driver.find_element(By.NAME, "bottom_Submit and Update Attempts").click()
                    assessment_type = "attempts"

                    try:
                        WebDriverWait(driver, 8).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')
                        alert = driver.switch_to.alert
                        alert.accept()
        
                    except TimeoutException:
                        pass
                    
                except NoSuchElementException:
                    print("Failed to submit: "+course_pk1+" "+question_pk1)
                    continue         

            try:
                WebDriverWait(driver, 3600).until(EC.url_contains("assessmentId"))

                if "assessmentId" in driver.current_url:
                    print("Success: "+course_pk1+" "+question_pk1+" "+assessment_type)
                
            except:
                print("Failed to edit: "+course_pk1+" "+question_pk1+" "+assessment_type)


def main():
    driver = login()
    edit_test_question(driver)
    logout(driver)

main()
