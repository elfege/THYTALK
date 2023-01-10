import requests
from flask import jsonify
import os

try:
    from keys import API_KEY_keys, API_KEY_2_keys 
except:
    API_KEY_keys="nokey"
    API_KEY_2_keys="nokey"
    


API_KEY = os.environ.get("API_KEY", API_KEY_keys)
BASE_URL = "https://gnews.io/api/v4/"

# EXAMPLE: get_news("top-headlines","breaking-news")

def get_news(endpoint, topic):
    
    url = BASE_URL+endpoint+"?token="+API_KEY+"&topic="+topic
    
    print(f"url = {url}")
    
    
    resp = requests.get(
        url,
        # params={"term": "Nicolas Jaar", "limit": 100}
        params={"lang": "en"}
    )
    
    return resp.json()
    

API_KEY_2 = os.environ.get("API_KEY_2", API_KEY_2_keys)
BASE_URL_2 = "https://newsapi.org/v2/everything/"

def get_news_2(): 
        
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey="+API_KEY_2

    print(f"url = {url}")
    
    resp = requests.get(url)
    
    return resp.json()


# I use 2 different API's because their daily number of requests is limited in their respective
# free editions.
def news_api_req():
    articles = {}
    news = get_news("top-headlines", "breaking-news")
    if list(news.keys())[0] == "errors":
        """BOTH API'S HAVE A DIFFERENT DICT KEY FOR THE IMAGE URL
        THIS FUNCTION MAKES SURE THEY BOTH HAVE THE SAME DICT KEY
        """
        news = get_news_2()
        articles = news['articles']

        for dic in articles:
            v = dic['urlToImage']
            del dic['urlToImage']
            dic['image'] = v

        return articles

    else:
        articles = news['articles']
        return articles


print("NEWS.PY LOADED")