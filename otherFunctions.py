from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=os.getenv(NEWS_API_KEY))

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
    headlines = headliner.get_everything(q=word, sort_by='relevancy', language="en", page_size=10)
    
    articles = headlines.get('articles', [])  
    return articles 