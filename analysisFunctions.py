#imports
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# candleplot returns those basic stock plots with the red and green thingies 
def candleplot(inData, group, upcol, downcol):

    if group == 'd':
        data = inData
        width = 0.5
    if group == 'w':
        data = inData.resample('W').agg({'Open': 'first', 'Close': 'last', 'High': 'max', 'Low': 'min'})
        width= 5
    if group == 'm':
        data = inData.resample('ME').agg({'Open': 'first', 'Close': 'last', 'High': 'max', 'Low': 'min'})
        width = 10

    data.index = pd.to_datetime(data.index)

    up = data[data.Close >= data.Open] 
    down = data[data.Close < data.Open]
    plt.figure(facecolor='#f2e8cf')

    fig,ax = plt.subplots()

    ax.bar(up.index, up.Close-up.Open, width, bottom=up.Open, color=upcol) 
    ax.bar(up.index, up.High-up.Close, width * 0.1, bottom=up.Close, color=upcol) 
    ax.bar(up.index, up.Low-up.Open, width * 0.1, bottom=up.Open, color=upcol) 
    
    # Plotting down prices of the stock 
    ax.bar(down.index, down.Close-down.Open, width, bottom=down.Open, color=downcol) 
    ax.bar(down.index, down.High-down.Open, width*0.1, bottom=down.Open, color=downcol) 
    ax.bar(down.index, down.Low-down.Close, width*0.1, bottom=down.Close, color=downcol) 

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    return fig

def compare_stocks(tick1, tick2):
    score1 = 0
    score2 = 0 

    