import streamlit as st
import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 
from otherFunctions import convertTime

st.text_input("Please enter a stock ticker from the Yahoo Finance library", key="ticker")

timePeriod = convertTime(st.selectbox(
    'What time period would you like to look at?',
     ['5 days', '1 month', '6 months', '1 year', '5 years', 'YTD', 'max']))

stock = yf.Ticker(st.session_state.ticker)
hist = stock.history(period=timePeriod)
st.write(stock.info)
if not hist.empty:
    st.write(hist)
else:
    st.write(st.session_state.ticker + " is not in the Yahoo Finance Library")

st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbNcbwE9P_iSw9jzMfRAk_-Bz1dQjW9vfeWQ&s')
st.markdown("[Click me](https://www.linkedin.com/in/mishmishra/)")