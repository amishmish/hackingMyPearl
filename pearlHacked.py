import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from analysisFunctions import candleplot

st.title('Stock Analyzer')

st.text_input("Please enter a stock ticker from the Yahoo Finance library", key="ticker")

stock = yf.Ticker(st.session_state.ticker)
hist = stock.history(period='6mo')
plot1 = candleplot(hist, 'green', 'red')

if not hist.empty:
    st.write(hist)
    st.pyplot(plot1)
else:
    st.write(st.session_state.ticker + " is not in the Yahoo Finance Library")
