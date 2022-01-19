# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from bs4 import BeautifulSoup
from class_ConnectionManager import ConnectionManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
from itertools import islice

URL_BASE = "https://play.google.com/store/apps/details?id="
URL_PACKAGE = "com.gf.flyingmotorbike.policebike.robotshooting&hl=en&gl=US&showAllReviews=true"
URL_TOTAL = URL_BASE + URL_PACKAGE
MAX_PAGES = 30
counter_post = 0

cm = ConnectionManager()

# Do the request
cm.new_identity
req = cm.request(URL_TOTAL)

status_code = req.code if req != '' else -1
if status_code == 200:

    DRIVER_PATH = '/home/alberto/Descargas/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(req.url)

    #Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while (True):
        #Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #Wait to load page
        time.sleep(1)
        #Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        #Compare with previous scroll height
        if (new_height == last_height):
            break
        #Update new scroll height
        last_height=new_height
        #Press "Show more reviews" button
        try:
            driver.find_element_by_css_selector('.RveJvd.snByac').click()
        except NoSuchElementException:
            print("No existe")

    #Get reviews of users
    reviews = driver.find_elements_by_xpath('//div[@jsname="fk8dgd"]/div')

    for review in reviews:
        #print(review.text)
        #Get name of user
        name_user=review.find_element_by_xpath('.//span[@class="X43Kjb"]').text
        #Get date of review
        date=review.find_element_by_xpath('.//span[@class="p2TkOb"]').text
        #Get description
        description=review.find_element_by_xpath('.//span[@jsname="bN97Pc"]').text
        #Get number of stars of review
        starts_element=review.find_element_by_xpath('.//div[contains(@aria-label,"Rated")]')
        numStars = int(starts_element.get_attribute('aria-label').split()[1])

        #Write info in file
        f = open("reviews.txt", "a")
        f.write("Name:"+name_user + "\n")
        f.write("Date:"+date+ "\n")
        f.write("Stars:"+str(numStars)+ "\n")
        f.write("Description:"+description+ "\n")
        f.close()
            


print("Finished")
    

"""


    html = BeautifulSoup(req.read(), "html.parser")
    posts = html.find_all('div', {'jscontroller':'H6eOGe'})
    file_text = open("output.txt", "a")
    file_text.write("Accessing:" + URL_TOTAL + "\n")
    for post in posts:
        file_text.write(str(post.get_text()) + "\n")
    
"""
