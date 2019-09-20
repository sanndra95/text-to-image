from selenium import webdriver
import json
import os
import platform
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import ActionChains

# set the desired hashtag
the_item = "running"
# set the number of photos you want to collect, instagram eill not allow you to collect all the posts at
# once, so you will have to go several timer to collect the desired amount
max_scrape = 150
insta_path = "explore/tags/"
prefix = "photos"
# Create folders as necessary
data_path = "data/data" + "_" + prefix + "_" + the_item
media_path = "data/media"


def create_folders():
    try:
        os.mkdir("data")
        print("made new data folder")
    except:
        pass

    try:
        os.mkdir("data/media")
        print("made new media folder")
    except:
        pass

    try:
        os.mkdir(data_path)
        print("made new project folder")
    except:
        pass


def previous_posts():
    try:
        f = open(data_path + "/temp_links.json", "r")
        the_posts = json.load(f)
        f.close()
        if len(the_posts) == 0:
            the_posts = {}
            print("This is a new scrape. No saved posts found.")
        else:
            print("Found", len(the_posts), "saved posts.")
    except:
        the_posts = {}
        try:
            os.mkdir(data_path + "/temp_links.json")
        except:
            print("File exists.")
        print("This is a new scrape. No saved posts found.")

    return the_posts


def read_default_config():
    try:
        f = open("config.json","r")
    except:
        f = open("default-config.json","r")

    conf = json.load(f)
    f.close()
    if not the_item in conf:
        conf[the_item] = conf["default"]
        f = open("config.json","w")
        json.dump(conf,f)
        f.close()
        print("Updated the config file.")
    return conf[the_item]


def set_up_driver():
    if not os.getcwd() in os.get_exec_path():
        print('adding path')
        if platform.system() == "Windows":
            os.environ["PATH"] = os.environ["PATH"] + ";" + os.getcwd()
        else:
            os.environ["PATH"] = os.environ["PATH"] + ":" + os.getcwd()

    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'D:\projekti\scrapinInsta\geckodriver.exe')
    actionChains = ActionChains(driver)
    driver.get("https://www.instagram.com/" + insta_path + the_item + "/")

    return driver, actionChains


def load_more(driver):
    # Send key strokes to scroll down the page
    # first of all click on the "Load more" button
    # Instagram uses different class names for the "Load more" button, so it's necessary to check for more than one.
    load_more_codes = ["_8imhp", "_oidfu"]

    found_it = False

    for load_more_code in load_more_codes:
        if not found_it:
            try:
                print(driver.title)
                some_element = driver.find_element_by_class_name(load_more_code)
                some_element.click()
                found_it = True
            except:
                pass

    if not found_it:
        print("there is only one page")
        some_element = None

    return some_element


