#imports
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from newsapi import NewsApiClient

headliner = NewsApiClient(api_key='9b0a343d2ac04b83b150a36d651ffe2c')

# candleplot returns those basic stock plots with the red and green thingies 
def candleplot(data, upcol, downcol):
    up = data[data.Close >= data.Open] 
    down = data[data.Close < data.Open]
    plt.figure(facecolor='#f2e8cf')

    fig,ax = plt.subplots()

    ax.bar(up.index, up.Close-up.Open, 1, bottom=up.Open, color=upcol) 
    ax.bar(up.index, up.High-up.Close, 0.1, bottom=up.Close, color=upcol) 
    ax.bar(up.index, up.Low-up.Open, 0.1, bottom=up.Open, color=upcol) 
    
    # Plotting down prices of the stock 
    ax.bar(down.index, down.Close-down.Open, 1, bottom=down.Open, color=downcol) 
    ax.bar(down.index, down.High-down.Open, 0.1, bottom=down.Open, color=downcol) 
    ax.bar(down.index, down.Low-down.Close, 0.1, bottom=down.Close, color=downcol) 

    return fig
