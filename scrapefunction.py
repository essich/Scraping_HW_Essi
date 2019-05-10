#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 17:49:42 2019

@author: charlesessi
"""

# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd



# Initialize browser
def use_browser(): 
    #Replace the path with your actual path to the chromedriver

    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)



# Create Sailing dictionary that can be imported into Mongo
scuttlebutt = {}

# NASA MARS NEWS
def scrape_sail_news(): 

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    #Return Recent Paragraph and title
    scutt_news_url = "https://www.sailingscuttlebutt.com/"
    browser.visit(scutt_news_url)
    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    recent_title = soup.find('h2', class_="omc-blog-one-heading").text[1:-1]
    recent_title

    recent_title_par = soup.find('p', class_="omc-blog-one-exceprt").text
    recent_title_par

    #Return Featured Sailing Image
    scutt_img_url = "https://www.sailingscuttlebutt.com/category/photo/"
    browser.visit(scutt_img_url)
    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    featured_image_url = soup.find_all('img', class_="omc-image-resize wp-post-image")[0]["src"]
    featured_image_url

    #Return Cleveland Weather 
        # Cle weather (via twitter)
    cle_weather_twitter_url = 'https://twitter.com/NWSCLE?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor'
    page = requests.get(cle_weather_twitter_url)
    soup = BeautifulSoup(page.text,'html.parser')

    cle_tweet = soup.find('p', class_="TweetTextSize").get_text()

    cle_weather = cle_tweet.replace('\n', ' ')
    cle_weather

    #Return Sailing Table 
    sailing_def_url = "https://en.wikipedia.org/wiki/List_of_large_sailing_yachts"
    browser.visit(sailing_def_url)
    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    tables = pd.read_html(sailing_def_url)
    sail_facts = tables[1]
    sail_facts=sail_facts.to_html()

    scuttlebutt = {"title": recent_title,
                   "paragraph": recent_title_par,
                   "image": featured_image_url,
                   "weather": cle_weather,
                   "facts": sail_facts}
    
    
    return scuttlebutt