import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time
import re

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(10)
    news_html = browser.html
    soup = BeautifulSoup(news_html, "html.parser")

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_ = 'article_teaser_body').text 

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(10)
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, "html.parser")

    base_url = 'https://www.jpl.nasa.gov'
    time.sleep(10)
    featured_image_url = image_soup.find('img', class_ = 'thumb')["src"]
    featured_image = base_url + featured_image_url

    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    time.sleep(10)
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, "html.parser") 

    tweets = weather_soup.find_all("span",text=re.compile('InSight sol'))
    latest_tweets=tweets[0].get_text()

    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(10)

    facts_tables = pd.read_html(facts_url)
    facts_df = facts_tables[0]
    facts_df.columns = ["Description", "Value"]
    facts_df = facts_df.set_index("Description")
    html_table = facts_df.to_html()

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(10)
    hem_html = browser.html
    hemispheres_soup = BeautifulSoup(hem_html, "html.parser")

    hemispheres = hemispheres_soup.find_all('div', class_= 'item')

    links = []

    for hemisphere in hemispheres:
        
            # scrape the article title 
            title = hemisphere.find('h3').text

            # scrape the article image url
            img_url = hemisphere.find('a', class_= 'itemLink product-item')['href']
            browser.visit('https://astrogeology.usgs.gov' + img_url)
            time.sleep(10)
            img_url = browser.html
            imgs_url = hemisphere.find('img', class_='thumb')['src']

            # Print results only if title, price, and link are available
            if (title and imgs_url):
                hem_urls  = 'https://astrogeology.usgs.gov' + imgs_url
                links.append({'title': title, 'img_urls': hem_urls})

    # Store all in dictionary
    mars_info = {
        "news_title": news_title,
        "news_summary": news_p, 
        "featured_image": featured_image,
        "latest_tweets": latest_tweets,
        "facts_table": html_table,
        "hemispheres_links": links
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info


