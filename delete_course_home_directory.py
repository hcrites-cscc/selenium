from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def delete_files(driver):
    with open("delete_course_home_directory.txt", mode="r", encoding="utf-8") as copy_list:
        content_line = copy_list.read().splitlines()
        
        for content in content_line:
            course_id = content

            driver.get(my_domain+"/webapps/cmsmain/webui"+course_id+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=1000&startIndex=0")
            time.sleep(0.5)

            document_body = driver.execute_script("return document.getElementById('containerdiv').innerText;")

            if document_body.find("Cannot display that location.") >= 0 or document_body.find("specified resource was not found") >= 0:
                print(course_id+" not found")

            else:
                files_count = driver.execute_script("return document.getElementById('numFiles').value;")
                files_form = driver.execute_script("return document.getElementsByName('filesForm')[0].innerText;")
                
                if files_form.find("Folder Empty") >= 0:
                    print(course_id+" empty")

                else:
                    subaction = driver.execute_script("return document.getElementById('subaction').value;")

                    if subaction=="deleteforce":
                        time.sleep(0.1)
                        print(course_id+" done")
                        
                    else:
                        driver.execute_script("return document.getElementById('listContainer_selectAll').click();")
                        #driver.find_element(By.ID, "listContainer_selectAll").click()
                        driver.execute_script("var selectedFiles = csfunctions.getSelectedFiles();FileFolderRemoval.getNumberOfFilesWithLinks( selectedFiles, function(numFiles) {if (numFiles > 0 && selectedFiles.length >= 1){document.filesForm.a1.value = 'multiple';document.filesForm.subaction.value = 'listfileswithlinks';document.filesForm.action = csfunctions.origAction;document.filesForm.submit();return;}document.filesForm.a1.value = 'multiple';document.filesForm.subaction.value = 'deleteforce';document.filesForm.action = csfunctions.origAction;document.filesForm.submit();});")
                        time.sleep(1.5)
                        print(course_id+" done")

                        #xid_count = 0

                        #if files_form.find("xid-") >= 0:
                        #    file_inputs = driver.find_elements_by_tag_name("input")
                        #    for field in file_inputs:
                        #        if field.get_attribute("type") == "checkbox":
                        #            if field.text.find("xid-") >= 0:
                        #                ++xid_count
                        #                field.click()
                        #                
                        #if xid_count == files_count:
                        #    print(course_id+" only xid files")
                        #else:
                        #    driver.execute_script("var selectedFiles = csfunctions.getSelectedFiles();FileFolderRemoval.getNumberOfFilesWithLinks( selectedFiles, function(numFiles) {if (numFiles > 0 && selectedFiles.length >= 1){document.filesForm.a1.value = 'multiple';document.filesForm.subaction.value = 'listfileswithlinks';document.filesForm.action = csfunctions.origAction;document.filesForm.submit();return;}document.filesForm.a1.value = 'multiple';document.filesForm.subaction.value = 'deleteforce';document.filesForm.action = csfunctions.origAction;document.filesForm.submit();});")
                        #    driver.implicitly_wait(5)
                            


def main():
    driver = login()
    delete_files(driver)
    logout(driver)

main()
