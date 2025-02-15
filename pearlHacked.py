import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from analysisFunctions import candleplot, get_the_news
from newsapi import NewsApiClient


newsapi = NewsApiClient(api_key='9b0a343d2ac04b83b150a36d651ffe2c')

st.title('Stock Analyzer')

st.text_input("Please enter a stock ticker from the Yahoo Finance library", key="ticker")

tick = st.session_state.ticker
stock = yf.Ticker(tick)
hist = stock.history(period='6mo')

st.header(stock.info.get('shortName'))
st.write(stock.info)

if not hist.empty:
    plot1 = candleplot(hist, '#bc4749', '#386641')
    st.pyplot(plot1)
    st.write(get_the_news(stock))
else:
    st.write(st.session_state.ticker + " is not in the Yahoo Finance Library")
