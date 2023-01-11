
Chosen API:https://gnews.io/
 
import requests

API_KEY = "?token=4a21868530d02f7387c0a672e3053af8"
BASE_URL = "https://gnews.io/api/v4/"

def get_news(endpoint, topic):
    
    url = BASE_URL+endpoint+API_KEY+"&topic="+topic
    
    print(f"url = {url}")
    resp = requests.get(
        url,
        params={"term": "Nicolas Jaar", "limit": 100}
    )

    return resp.json()


