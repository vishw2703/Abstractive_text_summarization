from time import time
from urllib import request
import urllib.parse as urlparse
import requests
from bs4 import BeautifulSoup
import time
from newspaper import Article
import urllib.parse as urlparse


def title_for_second(input_by_user):
    
    topic = input_by_user
    
    params = {
    "key": "AIzaSyCsFpUNDvwllXgylQRimZa6f53rHPQ0r8o",
    "cx": "b5cb6aab31f41482f",
    "q": topic,
     "start": 0 }
    gcse_base_url = "https://www.googleapis.com/customsearch/v1"
    url_parts = list(urlparse.urlparse(gcse_base_url))
    url_parts[4] = urlparse.urlencode(params)
    gcse_url = urlparse.urlunparse(url_parts)
    data = requests.get(gcse_url).json()
    # print(data)
    items = data["items"]
    # no_website = (len(items))
    website_link=[]
    for i in range(10):
        web_link= str((items[i].get('link')))
        website_link.append(web_link)

    
    def title_of_website(website_link):
        
        def getdata(url):
            r = requests.get(url)
            return r.text
        
        htmldata = getdata(website_link)
        soup = BeautifulSoup(htmldata, 'html.parser')
        for title in soup.find_all('title'):
            title = (title.get_text())
            break
        
        return title

    def get_text_article(link_of_website):
        url = link_of_website
        article = Article(url)
        article.download()
        article.parse()
        text_article = (article.text)
        return text_article

    web_data=[]


    for i in range(10):
        web_data.append(title_of_website(website_link[i]))



    for i in range(10):
        web_data.append(get_text_article(website_link[i]))

    for i in range(10):
        web_link= str((items[i].get('link')))
        web_data.append(web_link)

    

    return web_data



