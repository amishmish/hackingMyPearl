import streamlit as st
import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 

st.text_input("Please enter a stock ticker from the Yahoo Finance library", key="ticker")

if not yf.Ticker(st.session_state.ticker).history(period='6mo').empty:
    stock = yf.Ticker(st.session_state.ticker)
    hist = stock.history(period='6mo')
    st.write(hist)
else:
    st.write(st.session_state.ticker + " is not in the Yahoo Finance Library")
