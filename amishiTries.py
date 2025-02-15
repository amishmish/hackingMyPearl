import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from analysisFunctions import candleplot

aapl = yf.Ticker('AAPL')

st.write('I made something cool :p')
st.write(aapl.history(period = 'max'))

st.pyplot(candleplot(aapl.history(period='max'), 'green', 'red'))

import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option