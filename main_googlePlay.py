# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from attr import define
from bs4 import BeautifulSoup
from class_ConnectionManager import ConnectionManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
from itertools import count, islice
import getopt, sys, os, argparse, json

possibleVPN = ["US", "CA", "FR", "DE", "NL", "NO", "RO", "CH", "GB", "TR", "HK"]
reviewsList=[]

def vpnConnection(country):
    location = country
    if (location in possibleVPN):
        startVPNCommand = "windscribe connect"
        startVPNCommandComplete = startVPNCommand + " " + location
        os.system(startVPNCommandComplete)
        print("Connectiong to a VPN from " + country)

    elif location=="ES":
        print("Connectiong to a VPN from ES")
    
    else:
        print("Not a valid VPN")
        exit()



def defineURL(appStoreType, country):
    if (appStoreType=="Google"):
        URL_BASE = "https://play.google.com/store/apps/details?id="
        URL_PACKAGE = "com.gf.flyingmotorbike.policebike.robotshooting&hl=%s&gl=US&showAllReviews=true" %(country)
        print("Selecting Play Sotre as App Store")
        return URL_PACKAGE
    elif(appStoreType=="Huawei"):
        URL_BASE = "https://appgallery.huawei.com/app/"
        URL_PACKAGE = "C100315379"
        print("Selecting Huawei App Gallery as App Store")
        return URL_PACKAGE
    else:
        print("not a valid website")
        exit()

    
    URL_TOTAL = URL_BASE + URL_PACKAGE

def processComments(link, url):
    DRIVER_PATH = '/home/alberto/Descargas/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(link)

    if (url=="Google"):
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

            #Write info in json format
            reviewsList.append({'author':name_user,'timestamp':date,'numStars':contador,'review':description})

            #Write info in json file
        with open("reviewsGooglePlay.json", "w", encoding="utf8") as json_file:
            for rev in reviewsList:
                json.dump(rev, json_file, ensure_ascii=False)
    
    else:
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
                
            #Write info in json format
            reviewsList.append({'author':name_user,'timestamp':date,'numStars':contador,'review':description})

        #Write info in json file
        with open("reviewsHuaweiAppGallery.json", "w", encoding="utf8") as json_file:
            for rev in reviewsList:
                json.dump(rev, json_file, ensure_ascii=False)

def stopVPN():
    os.system("windscribe disconnect")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', type=str, required=True, help="The letter of the country where the VPN will be connected (US, CA, FR, DE, NL, NO, RO, CH, GB, TR, HK, ES)")
    parser.add_argument('-s', type=str, required=True, help="The App Store which will be processed (Google, Huawei)")
    args = parser.parse_args()
    location = args.v
    website = args.s                

    #Connection to the VPN
    vpnConnection(location)

    #Access to the website and process comments
    url = defineURL(website, location)

    #stopVPN
    stopVPN


if __name__ == "__main__":
    main()
