#!/usr/bin/python3

# Example:
# python3 gen_info.py conference_websites/lobby_day2.html xxx@xxxxx.edu my_password > yt_links/day2_yt_links.txt

import Driver
import sys
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException


def login_conference_page(driver, email, password):
    con_url = "https://ispg.societyconference.com/v2/"

    try:
        driver.get(con_url)
        driver.find_element_by_xpath('//*[@id="link-login"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="txt-login-email"]').send_keys(email)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="txt-login-password"]').send_keys(password)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="btn-login"]').click()    
        time.sleep(2)
    except:
        print("Error. Unable to login the conference page")
        Driver.clean_exit()



def main():
    arg_num = len(sys.argv)
    if (arg_num != 4):
        err_str = "Wrong Input"
        sys.exit(err_str)

    local_html_file = str(sys.argv[1])
    email = str(sys.argv[2])
    password = str(sys.argv[3])

    driver = Driver.init()
    login_conference_page(driver, email, password)

    page = open(local_html_file)
    soup = BeautifulSoup(page, 'html.parser')

    for event in soup.find_all('div', {'class':'schedule-item'}):
        print("=" * 20)

        # Get time
        col1 = event.find('div', {'class':'schedule-item-col1'})
        col1_div = col1.find('div')
        time_text = col1_div.find_all('div')[1].text
        print(time_text)

        # Get title
        title = event.find('div', {'class':'schedule-item-title-inner'}).text.strip(' \t\n\r')
        print(title)

        # Get recording url
        data_id = event['data-id']
        recording_url = "https://ispg.societyconference.com/recording/?id=" + data_id

        try:
            driver.get(recording_url)
        except:
            print("Error. Unable to open the recording url" + recording_url)
            Driver.clean_exit()

        try:
            embeded_yt_url = driver.find_element_by_xpath("/html/body/iframe").get_attribute("src")
            driver.get(embeded_yt_url)
            driver.find_element_by_xpath('//*[@id="movie_player"]/div[3]/div[3]/button[2]').click()
            time.sleep(1)
            yt_url = driver.find_element_by_xpath('//*[@id="ytp-id-26"]/div/a').text
            print(yt_url)

        except NoSuchElementException:
            # Some of the events have no video links
            pass


    Driver.uninit()

if __name__ == "__main__":
    main()
