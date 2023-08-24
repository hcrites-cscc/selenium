from auth import *
import time, html, codecs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException        

def edit_pool_matching_question(driver):
    with open("edit_pool_matching_question.txt", mode="r", encoding="utf-8") as edit_list:
        question_line = edit_list.read().splitlines()
        for question in question_line:
            course_pk1, question_pk1, pool_pk1, question_body_0, question_body_1, question_body_2, question_body_3, question_body_4 = question.split("\t")
            question_body_0 = codecs.escape_decode(bytes(html.unescape(question_body_0), "utf-8"))[0].decode("utf-8")
            question_body_1 = codecs.escape_decode(bytes(html.unescape(question_body_1), "utf-8"))[0].decode("utf-8")
            question_body_2 = codecs.escape_decode(bytes(html.unescape(question_body_2), "utf-8"))[0].decode("utf-8")
            question_body_3 = codecs.escape_decode(bytes(html.unescape(question_body_3), "utf-8"))[0].decode("utf-8")
            question_body_4 = codecs.escape_decode(bytes(html.unescape(question_body_4), "utf-8"))[0].decode("utf-8")

            driver.get(my_domain+"/webapps/assessment/do/authoring/modifyAssessment?method=modifyAssessment&copyAlignments=false&course_id=_"+course_pk1+"_1&assessmentId=_"+pool_pk1+"_1&saveAsNew=false&createAnother=false&assessmentType=Pool")
            #driver.get(my_domain+"/webapps/assessment/do/authoring/modifyAssessment?method=modifyAssessment&copyAlignments=false&course_id=_"+course_pk1+"_1&assessmentId=_"+test_pk1+"_1&saveAsNew=false&createAnother=false&assessmentType=Test")
            #driver.get(my_domain+"/webapps/assessment/do/authoring/modifyAssessment?course_id=_"+course_pk1+"_1&assessmentId=_"+test_pk1+"_1&isLinkedQuestion=false&method=cancel&questionId=_"+question_pk1+"_1&sectionId=&assessmentType=Pool&position=-1&course_id=_"+course_pk1+"_1&questionType=Matching")                      

            driver.execute_script("assessment.modifyQuestion('"+question_pk1+"');")
            driver.implicitly_wait(3)

            #driver.execute_script("document.getElementsByName('questionText.text')[0].value=`"+question_body+"`") #question

            #driver.execute_script("document.getElementById('leftMatchList.answer[0].textForm.text').value=`"+question_body+"`") #left matching option 1
            driver.execute_script("document.getElementById('rightMatchList.answer[0].textForm.text').value=`"+question_body_0+"`") #right matching option 1
            driver.execute_script("document.getElementById('rightMatchList.answer[1].textForm.text').value=`"+question_body_1+"`") #right matching option 2
            driver.execute_script("document.getElementById('rightMatchList.answer[2].textForm.text').value=`"+question_body_2+"`") #right matching option 3
            driver.execute_script("document.getElementById('rightMatchList.answer[3].textForm.text').value=`"+question_body_3+"`") #right matching option 4
            driver.execute_script("document.getElementById('rightMatchList.answer[4].textForm.text').value=`"+question_body_4+"`") #right matching option 5
            


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
    edit_pool_matching_question(driver)
    logout(driver)

main()
