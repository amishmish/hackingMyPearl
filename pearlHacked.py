import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from otherFunctions import get_the_news, convertTime
from analysisFunctions import candleplot
from newsapi import NewsApiClient


newsapi = NewsApiClient(api_key='9b0a343d2ac04b83b150a36d651ffe2c')

st.title('Stock Analyzer')

st.text_input("Please enter a stock ticker from the Yahoo Finance library", key="ticker")
timePeriod = convertTime(st.selectbox(
    'What time period would you like to look at?',
     ['5 days', '1 month', '6 months', '1 year', '5 years', 'YTD', 'max']))

tick = st.session_state.ticker
stock = yf.Ticker(tick)
hist = stock.history(period=timePeriod)

if not hist.empty:
    st.header(stock.info.get('shortName'))

    st.divider()
    if timePeriod in ['5d', '1mo', 'YTD']:
        plot1 = candleplot(hist,'d', '#386641', '#bc4749')
    elif timePeriod in ['6mo', '1y']:
        plot1 = candleplot(hist,'w', '#386641', '#bc4749')
    else: 
        plot1 = candleplot(hist, 'm', '#386641', '#bc4749')
    st.pyplot(plot1)

    st.divider()
    st.header('News')
    news = get_the_news(stock)
    i = 0
    index = 0
    while i < 3:
        valid = True
        for value in news[index]:
            if news[index][value] == None:
                valid = False
        
        if valid:
            url = news[index]['url']
            st.image(news[index]['urlToImage'])
            st.subheader(news[index]['title'])
            st.write(news[index]['description'])
            st.markdown(f'[Read More About This]({url})\n\n')
            i += 1

        index += 1
        if index == 9:
            break
else:
    st.write(st.session_state.ticker + " is not in the Yahoo Finance Library")
