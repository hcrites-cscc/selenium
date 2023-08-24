from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import NoSuchElementException

def overwrite_files(driver):
    with open("overwrite_files.txt", mode="r", encoding="utf8") as file_list:
        file_line = file_list.read().splitlines()
        for file in file_line:
            parent_directory, file_name, file_path = file.split("\t")

            driver.get(my_domain+"/webapps/cmsmain/webui"+parent_directory+file_name+"?action=upload&subaction=print&uniq=oa9mk3&gobackto=dirList-")
            time.sleep(2)
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "newFile_chooseLocalFile").send_keys(file_path)
                driver.implicitly_wait(5)
                driver.find_element(By.ID, "bottom_Submit").click()
                
                wait = WebDriverWait(driver, 1000)
                wait.until(EC.title_contains("Content")) #/courses/
                #wait.until(EC.title_contains("Files")) #/internal/

                try:
                    success = driver.find_element(By.ID, "goodMsg1").text
                    print(success+" - "+parent_directory+" "+file_name)
                except:
                    print("Fail: element not found - "+parent_directory+" "+file_name)
                
            except InvalidArgumentException:
                print("Fail: new file path not found - "+parent_directory+" "+file_name)

            except NoSuchElementException:
                print("Fail: page didn't load - "+parent_directory+" "+file_name)
          



def main():
    driver = login()
    overwrite_files(driver)
    logout(driver)

main()
