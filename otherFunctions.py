from newsapi import NewsApiClient
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
newsapi = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))

def convertTime(period):
    if 'day' in period:
        return period[0] + "d"
    elif 'month' in period:
        return period[0] + 'mo'
    elif 'year' in period:
        return period[0] + 'y'
    else:
        return period 

def get_the_news(stock):
    word = stock.info.get('shortName')
    headlines = newsapi.get_everything(q=word, sort_by='relevancy', language="en", page_size=10)
    
    articles = headlines.get('articles', [])  
    return articles 