# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from bs4 import BeautifulSoup
from class_ConnectionManager import ConnectionManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
from itertools import islice

URL_BASE = "https://appgallery.huawei.com/app/"
URL_PACKAGE = "C100315379"
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

    #Wait to load page
    time.sleep(1)

    #Press "View All" button
    #Press "Show more reviews" button
    try:
        driver.find_element_by_css_selector('.more').click()
    except NoSuchElementException:
        print("No existe el boton: View all")

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

        
        

    #Get reviews of users
    reviews = driver.find_elements_by_xpath('//div[@class="listContainer"]/div')
    #print(reviews)



    for review in reviews[:-1]:
        #print(review.text)
        #Get name of user
        name_user=review.find_element_by_xpath('.//div[@class="userName"]').text
        #Get date of review
        date=review.find_element_by_xpath('.//div[@class="deviceName"]').text
        #Get description
        description=review.find_element_by_xpath('.//div[@class="part_middle"]').text
        #Get number of stars of review
        starts_element=review.find_elements_by_xpath('.//img[@src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iNjRweCIgaGVpZ2h0PSI2NHB4IiB2aWV3Qm94PSIwIDAgNjQgNjQiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8dGl0bGU+aWNfc2NvcmU8L3RpdGxlPgogICAgPGRlZnM+CiAgICAgICAgPHBhdGggZD0iTTMwLjgxMDU2NjUsMS40MTc0MTc5MyBMMzcuMzQ2Nzc5NCwxOS4xNjE5NzQyIEwzNy4zNDY3Nzk0LDE5LjE2MTk3NDIgTDU1LjI1MzM3NDUsMTkuMTYxOTc0MiBDNTYuNTE1NzM5NiwxOS4xNjE5NzQyIDU3LjUzOTA4ODgsMjAuMTg1MzIzMyA1Ny41MzkwODg4LDIxLjQ0NzY4ODUgQzU3LjUzOTA4ODgsMjIuMTY1MjExNyA1Ny4yMDIxNTcyLDIyLjg0MTA5MjYgNTYuNjI5MTY5MiwyMy4yNzI5NzcxIEw0Mi4wNzUwNjY2LDM0LjI0Mjk5OTIgTDQyLjA3NTA2NjYsMzQuMjQyOTk5MiBMNDcuNTQ4MzEwMSw1MS41NzkzNTg3IEM0Ny45MjgzNTk3LDUyLjc4MzE1NjEgNDcuMjYwNTgwMSw1NC4wNjcxMTc3IDQ2LjA1Njc4MjgsNTQuNDQ3MTY3MyBDNDUuMzgwMjQ2LDU0LjY2MDc1NiA0NC42NDI4ODI3LDU0LjU0ODA4ODEgNDQuMDYwOTk4Nyw1NC4xNDIyMTQ5IEwyOC43MjA4NDczLDQzLjQ0MjIxOSBMMjguNzIwODQ3Myw0My40NDIyMTkgTDE0LjAyMzE4ODUsNTQuMzg2NzQ4MSBDMTMuMDEwNjk5NSw1NS4xNDA2OTIzIDExLjU3ODcyMjUsNTQuOTMxMTAwNCAxMC44MjQ3NzgzLDUzLjkxODYxMTUgQzEwLjM5NjAwMTQsNTMuMzQyNzk3MSAxMC4yNjI2NzQ5LDUyLjU5ODk4NTQgMTAuNDY0NzU1Nyw1MS45MTAwOTEzIEwxNS42MzQwNDIzLDM0LjI4Nzk3NjUgTDE1LjYzNDA0MjMsMzQuMjg3OTc2NSBMMC43MDM4MjEwMDQsMjMuMjg3ODgyMSBDLTAuMzEyNDg5ODczLDIyLjUzOTA5NzggLTAuNTI5MzYzMDAxLDIxLjEwODIwNTQgMC4yMTk0MjEzMTcsMjAuMDkxODk0NSBDMC42NTAyMzU5MDMsMTkuNTA3MTU4IDEuMzMzMzEwNTgsMTkuMTYxOTc0MiAyLjA1OTYxNDk0LDE5LjE2MTk3NDIgTDE5Ljk5MzI5NzksMTkuMTYxOTc0MiBMMTkuOTkzMjk3OSwxOS4xNjE5NzQyIEwyNi41MjA1NjIsMS40MTgzMzQ3IEMyNi45NTYzODgzLDAuMjMzNTg5NDk4IDI4LjI3MDEyMTEsLTAuMzczNTI5MjIzIDI5LjQ1NDg2NjMsMC4wNjIyOTcwODA4IEMzMC4wODM0OTE1LDAuMjkzNTQ2Mjg0IDMwLjU3OTA0ODYsMC43ODg4OTE2NTQgMzAuODEwNTY2NSwxLjQxNzQxNzkzIFoiIGlkPSJwYXRoLTEiPjwvcGF0aD4KICAgIDwvZGVmcz4KICAgIDxnIGlkPSJpY19zY29yZSIgc3Ryb2tlPSJub25lIiBzdHJva2Utd2lkdGg9IjEiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgb3BhY2l0eT0iMSI+CiAgICAgICAgPGcgaWQ9ImljL2Zhdm91cml0ZXMvaWNfZmF2b3VyaXRlcyI+CiAgICAgICAgICAgIDxnIGlkPSJzeW1ib2wvZnJhbWUvc3ltYm9sX2dyaWQyNCI+PC9nPgogICAgICAgICAgICA8ZyBpZD0ic3RhciIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMy4zMzMzMzMsIDMuMzMzMzMzKSI+CiAgICAgICAgICAgICAgICA8bWFzayBpZD0ibWFzay0yIiBmaWxsPSJ3aGl0ZSI+CiAgICAgICAgICAgICAgICAgICAgPHVzZSB4bGluazpocmVmPSIjcGF0aC0xIj48L3VzZT4KICAgICAgICAgICAgICAgIDwvbWFzaz4KICAgICAgICAgICAgICAgIDxnIGlkPSJTdHJva2UtMTYxLUNvcHktMiIgZmlsbC1ydWxlPSJub256ZXJvIj48L2c+CiAgICAgICAgICAgICAgICA8ZyBpZD0iY29sb3IvbGlnaHQvIzAwMDAwMCIgbWFzaz0idXJsKCNtYXNrLTIpIiBmaWxsPSIjRkRDNTFFIj4KICAgICAgICAgICAgICAgICAgICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMy4zMzMzMzMsIC0zLjMzMzMzMykiIGlkPSJjb2xvci8jMDAwMDAwIj4KICAgICAgICAgICAgICAgICAgICAgICAgPHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0Ij48L3JlY3Q+CiAgICAgICAgICAgICAgICAgICAgPC9nPgogICAgICAgICAgICAgICAgPC9nPgogICAgICAgICAgICA8L2c+CiAgICAgICAgPC9nPgogICAgPC9nPgo8L3N2Zz4="]')
        contador=0
        for star in starts_element:
            contador+=1
            
        #Write info in file
        f = open("reviews.txt", "a")
        f.write("Name:"+name_user + "\n")
        f.write("Date:"+date+ "\n")
        f.write("Stars:"+str(contador)+ "\n")
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
