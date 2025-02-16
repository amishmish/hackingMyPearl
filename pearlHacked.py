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

st.header(stock.info.get('shortName'))

if not hist.empty:
    plot1 = candleplot(hist, '#bc4749', '#386641')
    st.pyplot(plot1)
    news = get_the_news(stock)
    for i in range(0,3):
        st.write(news[i]['title'])
else:
    st.write(st.session_state.ticker + " is not in the Yahoo Finance Library")
