#imports
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# candleplot returns those basic stock plots with the red and green thingies 
def candleplot(data, upCol, downCol):
    up = data[data.Close >= data.Open]
    down = data[data.Open < data.Close]

    fig, ax = plt.subplots(figsize=(10, 5))  # Create a figure and axis
    
    ax.bar(up.index, up.Close-up.Open, width=0.3, bottom=up.Open, color=upCol) 
    ax.bar(up.index, up.High-up.Close, width=0.03, bottom=up.Close, color=upCol) 
    ax.bar(up.index, up.Low-up.Open, width=0.03, bottom=up.Open, color=upCol) 
    
    # Plotting down prices of the stock 
    ax.bar(down.index, down.Close-down.Open, width=0.3, bottom=down.Open, color=downCol) 
    ax.bar(down.index, down.High-down.Open, width=0.03, bottom=down.Open, color=downCol) 
    ax.bar(down.index, down.Low-down.Close, width=0.03, bottom=down.Close, color=downCol)
    return fig