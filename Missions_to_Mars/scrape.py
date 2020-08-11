
# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import requests
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

def scrape_planet():

    browser = init_browser()

    # list of urls to visit
    url_mars_news = 'https://mars.nasa.gov/news/'
    url_jpl_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_mars_weather = 'https://twitter.com/marswxreport?lang=en'
    url_mars_facts = 'https://space-facts.com/mars/'
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # define result dictionary to RETURN
    planet_data = {}

    # Setup connection to mongodb
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

    # Select database and collection to use
    db = client.planet_db
    planet_coll = db.planet_data

    # Empty the collection



    # ---------------------------------------
    # SCRAPE PLANET NEWS FOR MARS
    # ---------------------------------------
    browser.visit(url_mars_news)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_="list_text").find('div', class_="content_title").get_text(strip=True)
    news_teaser = soup.find('div', class_="article_teaser_body").get_text(strip=True)

    planet_data['news_title'] = news_title
    planet_data['news_teaser'] = news_teaser


    # ---------------------------------------
    # SCRAPE JPL FOR FEATURED IMAGE
    # ---------------------------------------
    image_root = 'https://www.jpl.nasa.gov'

    browser.visit(url_jpl_image)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    jpg_path = soup.find('article', class_="carousel_item")["style"]

    featured_image_url = image_root + jpg_path[jpg_path.find('url')+5:jpg_path.find('jpg')+3]

    planet_data['featured_image_url'] = featured_image_url


    # ---------------------------------------
    # SCRAPE TWITTER FEED FOR WEATHER
    # ---------------------------------------
    browser.visit(url_mars_weather)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    weather_tweet = soup.find('div', attrs = {'class': 'css-901oao', 'lang': 'en', 'dir':'auto'}).get_text(strip=True)

    planet_data['weather_tweet'] = weather_tweet


    # ---------------------------------------
    # SCRAPE SPACE-FACTS FOR TABLE OF INFO
    # USING PANDAS
    # ---------------------------------------
    tables = pd.read_html(url_mars_facts)

    # get first table for DataFrame and set columns & index
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['attribute', 'value']
    mars_facts_df.set_index('attribute', inplace=True)
    
    # convert to html to save to result dictionary
    facts_html = mars_facts_df.to_html()
    planet_data['planet_facts_html'] = facts_html



    # ---------------------------------------
    # SCRAPE FOR IMAGES OF EACH HEMISPHERE
    # ---------------------------------------
    browser.visit(url_hemispheres)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    images_html = soup.find_all('a', class_='itemLink product-item')

    # get url list for all hemispheres
    image_base_url = 'https://astrogeology.usgs.gov'
    hemisphere_urls = []
    for element in images_html:
        if element.find('h3'):
            hemisphere_urls.append(image_base_url + element['href'])

    # go to hemisphere url and get full image path and description
    hemisphere_image_urls = []
    for h_url in hemisphere_urls:
        # print(h_url)
        browser.visit(h_url)
        time.sleep(0.5)
        
        h_html = browser.html
        soup = BeautifulSoup(h_html, 'html.parser')

        full_res_title = soup.find('h2', class_="title").get_text(strip=True)
        # print(full_res_title)

        full_res_url = soup.find('a', text='Sample')['href']
        # print(full_res_url)

        hemisphere_image_urls.append({
            'title': full_res_title,
            'img_url': full_res_url
        })

    # hemisphere_urls
    planet_data['hemisphere_image_urls'] = hemisphere_image_urls


    # ---------------------------------------
    # INSERT RESULT INTO MONGO COLLECTION
    # ---------------------------------------   
    
    # Empty collection first
    planet_coll.remove({})

    # Insert new data
    planet_coll.insert_one(planet_data)

    return planet_data