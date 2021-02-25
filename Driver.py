#!/usr/bin/python3

from selenium import webdriver
import time, os, sys

Instance = None
Headless = None


def init(headless=True, chrome_path="/usr/bin/chromedriver"):
    global Instance, Headless
    Headless = headless
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('headless')
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('window-size=1200,1100')
    chrome_options.add_argument('no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.

    Instance = webdriver.Chrome(executable_path=chrome_path,
            chrome_options=chrome_options,
            service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])

    return Instance


def uninit():
    global Instance
    time.sleep(1)
    Instance.stop_client()
    Instance.close()
    Instance.quit()
    time.sleep(1)


def clean_exit():
    try:
        uninit()
    finally:
        sys.exit(0)


def get_headless():
    global Headless
    return Headless


def get_instance():
    global Instance
    return Instance