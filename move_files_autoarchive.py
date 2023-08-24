from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def move_files_autoarchive(driver):
    with open("move_files_autoarchive.txt", mode="r", encoding="utf-8") as archive_file:
        archive_list = archive_file.read().splitlines()
        new_directory = "/internal/autoArchive/0000_temp/"

        for archive_set in archive_list:
            archives = archive_set.split("|")

            driver.get(my_domain+"/webapps/cmsmain/webui/internal/autoArchive?sortDir=ASCENDING&subaction=view&action=frameset&uniq=-quealr&editPaging=true&numResults=1")

            driver.implicitly_wait(3)

            #driver.find_element(By.NAME, "file0").click()
            driver.execute_script("document.getElementsByName('file0')[0].click();")
            driver.execute_script("csfunctions.moveFiles('Recycle Bin')")

            driver.implicitly_wait(3)

            #driver.find_element(By.ID, "targetPath_CSFile").send_keys(new_directory)
            driver.execute_script("document.getElementById('targetPath_CSFile').value = '"+new_directory+"'")
            driver.execute_script("var my_form = document.getElementsByName('destination')[0];document.getElementById('file0').remove();")

            file_count = 0

            for archive in archives:
                driver.execute_script("var my_form = document.getElementsByName('destination')[0];var input = document.createElement('input');input.setAttribute('type', 'hidden');input.setAttribute('id', 'file"+str(file_count)+"');input.setAttribute('name', 'file"+str(file_count)+"');input.setAttribute('value', `"+archive+"`);my_form.appendChild(input);")
                file_count+=1

            driver.execute_script("document.getElementById('numFiles').value = '"+str(file_count)+"';")
            driver.execute_script("document.getElementById('bottom_Submit').click();")
            #driver.find_element(By.ID, "bottom_Submit").click()
            driver.implicitly_wait(3)

            try:
                driver.find_element(By.ID, "goodMsg1").text
                print("Success: "+str(file_count)+" folders moved")
            except:
                print("Failed to move: "+str(file_count)+" folders")


def main():
    driver = login()
    move_files_autoarchive(driver)
    logout(driver)

main()
