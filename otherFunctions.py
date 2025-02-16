from newsapi import NewsApiClient

headliner = NewsApiClient(api_key='9b0a343d2ac04b83b150a36d651ffe2c')

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