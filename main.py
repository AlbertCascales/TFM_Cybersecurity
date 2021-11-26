# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from bs4 import BeautifulSoup
from class_ConnectionManager import ConnectionManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

URL_BASE = "https://play.google.com/store/apps/details?id="
URL_PACKAGE = "com.aquiris.horizonchase&showAllReviews=true"
URL_TOTAL = URL_BASE + URL_PACKAGE
MAX_PAGES = 30
counter_post = 0

cm = ConnectionManager()

# Do the request
cm.new_identity
req = cm.request(URL_TOTAL)

status_code = req.code if req != '' else -1
if status_code == 200:

    DRIVER_PATH = '/home/linux/Descargas/chromedriver_linux64/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(req.url)
    while (True):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            driver.find_element_by_css_selector('.RveJvd.snByac').click()
        except NoSuchElementException:
            print("No existe")

print("Finished")

"""


    html = BeautifulSoup(req.read(), "html.parser")
    posts = html.find_all('div', {'jscontroller':'H6eOGe'})
    file_text = open("output.txt", "a")
    file_text.write("Accessing:" + URL_TOTAL + "\n")
    for post in posts:
        file_text.write(str(post.get_text()) + "\n")
    
"""
