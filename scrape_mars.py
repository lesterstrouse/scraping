
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import numpy as np
import pymongo
from splinter import Browser
import pandas as pd





# In[2]:
def scrape():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')


    # In[3]:


    # Print formatted version of the soup
    news_title = soup.title.text


    # In[4]:


    news_p = soup.p.text


    # In[5]:


    #print(news_title)
    #print(news_p)


    # In[6]:


    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome',  **executable_path, headless=False)


    # In[7]:


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)


    # In[8]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    anchors = soup.find_all('a',class_='button fancybox')
    anchors_href = anchors[0]['data-fancybox-href']
    featured_image_url = "https://www.jpl.nasa.gov" + anchors_href


    # In[9]:


    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)


    # In[10]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    weaths = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weath = weaths.text


    # In[11]:


    url="https://space-facts.com/mars/"


    # In[12]:
    tables = pd.read_html(url)
    df=tables[0]
    #print(df)
    table_html = df.to_html()
    

    # In[14]:


    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)


    # In[15]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    phlinks = soup.find_all('div',class_='item')
    hem_img_urls = []
    for phlink in phlinks:
        lnk = "https://astrogeology.usgs.gov"+phlink.a["href"]
        browser.visit(lnk)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        i = soup.find('img',class_='wide-image')
        img_url = 'http://astrogeology.usgs.gov' + i['src']
        title = soup.title.text
        hem_dict = { 'title' : title, 'img_url': img_url }
        hem_img_urls.append(hem_dict)
    
    listscrape = {'news_title':news_title,\
    'featured_image_url':featured_image_url,\
    'mars_weath':mars_weath,\
    'table_html':table_html,\
    'hem_img_urls':hem_img_urls}
    return listscrape

