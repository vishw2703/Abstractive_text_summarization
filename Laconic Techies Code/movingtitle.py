from urllib import response
from bs4 import BeautifulSoup
import requests
import json

def scroll_news():
    url= "https://newsapi.org/v2/top-headlines?country=in&apiKey=e3374b995f2f4ea497e7b618587ca690"
    
    response_url= requests.get(url)
    
    json_response= response_url.json()
        
    article=json_response["articles"]
    title_no=[]
    for i in range(10):
        title_=article[i].get('title')
        title_no.append(title_)
        
    
    return title_no