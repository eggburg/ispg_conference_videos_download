#!/usr/bin/python3

# Example:
# python3 x2convert.py yt_links/test_yt_links.txt

import Driver
import sys, time
import os, os.path
import glob, shutil, traceback
from gi.repository import GLib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

CONCURENT_DOWNLOAD_LIMIT = 5

def xpath_exists(obj, xpath):
    try:
        item = obj.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def download(yt_url):
    driver = Driver.get_instance()
    driver.get("https://x2convert.com/en6")

    yt_url_box = driver.find_element_by_id('txtLink')
    yt_url_box.send_keys(yt_url)
    start_button = driver.find_element_by_id('btnGet')
    start_button.click()

    # Wait until the download button is ready
    WebDriverWait(driver, 30).until(\
            EC.presence_of_element_located((By.XPATH, '//*[@id="mp4"]/table')))

    tbody = driver.find_element_by_xpath('//*[@id="mp4"]/table/tbody')

    max_rs = -1
    max_tr = None
    for tr in tbody.find_elements_by_xpath('.//tr[position()>1]'):
        no_audio = xpath_exists(tr, './/img[@src="/Images/no_audio_red.png"]')
        if no_audio:
            continue
        td = tr.find_element_by_xpath('.//td[1]')
        if td.text is None:
            continue
        cur_rs = int(td.text.split('p')[0])
        if cur_rs > max_rs:
            max_rs = cur_rs
            max_tr = tr

    print('max resolution = ' + str(max_rs))
    button = max_tr.find_element_by_tag_name('a')
    button.click()

    dl_button_xpath = '//a[@target="_blank" and contains(\
            @class, "btn btn-success btn-lg") and contains(@href, "https://")]'
    # Wait until the download button ready
    WebDriverWait(driver, 30).until(\
            EC.presence_of_element_located((By.XPATH, dl_button_xpath)))

    dl_button = driver.find_element_by_xpath(dl_button_xpath)
    filename = dl_button.get_attribute('download')
    filename = filename.replace(' ', '+').replace('?', '_')
    print(filename)

    global FILE_COUNT
    FILE_COUNT += 1
    dl_button.click()


# Return a list of distinct youtube links
def get_yt_urls(yt_links_file):
    yt_urls = []
    with open(yt_links_file) as f:
        for line in f:
            if 'https://youtu.be' in line:
                yt_urls.append(line[:-1])   # get rid of '\n'

    # Remove duplicate links
    return set(yt_urls)


def download_yt_links_on_file(yt_links_file):

    cur_folder = os.getcwd()
    dest_folder = cur_folder + '/my_mp4'
    print('dest_folder = ' + dest_folder)
    if os.path.exists(dest_folder):
        print('Clean up destination folder ' + dest_folder)
        shutil.rmtree(dest_folder)
    os.makedirs(dest_folder)

    if Driver.get_headless():
        dl_folder = './'
    else:
        dl_folder = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)

    concurrent_dl_count = lambda: len(glob.glob(dl_folder + '/*.mp4.crdownload*'))
    downloaded_count = lambda: len(glob.glob(dl_folder + '/*.mp4'))

    global FILE_COUNT, CONCURENT_DOWNLOAD_LIMIT
    FILE_COUNT = 0

    for yt_url in get_yt_urls(yt_links_file):
        while concurrent_dl_count() >= CONCURENT_DOWNLOAD_LIMIT :
            print("Reaching concurent downloading limit " +
                    CONCURENT_DOWNLOAD_LIMIT + ". Waiting for 10 seconds ...")
            time.sleep(10)
        print("\nDownloading " + yt_url)
        download(yt_url)

    while downloaded_count() < FILE_COUNT :
        time.sleep(5)
        print("Waiting for download to complete. Downloaded count = " +
                str(downloaded_count()) + ". Total file count = " + str(FILE_COUNT))

    print('Download finished. \nMoving mp4 files to ' + dest_folder)

    for file in glob.glob(dl_folder + '/*.mp4*'):
        shutil.move(file, dest_folder)


if __name__ ==  '__main__':

    arg_num = len(sys.argv)
    if (arg_num != 2):
        err_str = "Wrong Input"
        sys.exit(err_str)

    yt_links_file = str(sys.argv[1])

    try:
        driver = Driver.init(headless=True)
        download_yt_links_on_file(yt_links_file)

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stdout)
        Driver.clean_exit()

    Driver.uninit()
