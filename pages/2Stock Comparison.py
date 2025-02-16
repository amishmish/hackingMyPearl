import streamlit as st
import os
from dotenv import load_dotenv, dotenv_values
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from otherFunctions import get_the_news, convertTime
from analysisFunctions import candleplot, lineplot, compare_stocks, refine_paragraph


col1, col2 = st.columns(2)

with col1:
    st.text_input("Please enter a valid stock ticker!", key="ticker1")
    tick1 = st.session_state.ticker1
    stock1 = yf.Ticker(tick1)
    if not stock1.actions.empty:
        st.subheader(stock1.info.get('shortName'))
        hist1 = stock1.history(period = '1y')
        plot1 = candleplot(hist1,'w', '#386641', '#bc4749')
        st.pyplot(plot1)
    else: 
        st.write(tick1 + " is not in the Yahoo Finance Library")

with col2:
    st.text_input("Please enter a valid stock ticker!", key="ticker2")
    tick2 = st.session_state.ticker2
    stock2 = yf.Ticker(tick2)
    if not stock2.actions.empty:
        st.subheader(stock2.info.get('shortName'))
        hist2 = stock2.history(period = '1y')
        plot2 = candleplot(hist2,'w', '#386641', '#bc4749')
        st.pyplot(plot2)
    else: 
        st.write(tick2 + " is not in the Yahoo Finance Library")

if not (stock2.actions.empty & stock1.actions.empty):
    out = compare_stocks(stock1, stock2)
    st.write(refine_paragraph(out))

