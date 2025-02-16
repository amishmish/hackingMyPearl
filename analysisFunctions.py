#imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key =  os.environ.get('GEMINI_API_KEY'))

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

def lineplot(inData):
    inData.index = pd.to_datetime(inData.index)

    plt.figure(facecolor='#f2e8cf')

    fig,ax = plt.subplots()

    yvals = (inData.Close + inData.Open)/2

    sorted_data = yvals.sort_index(axis=0, ascending=True)
    diff = sorted_data.iloc[-1] - sorted_data.iloc[0]

    if diff < 0:
        ax.plot(inData.index, yvals, color = '#bc4749')
    else:
        ax.plot(inData.index, yvals, color = '#386641')


    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    return fig

def compare_stocks(tick1, tick2):
    paragraph = ''
    score1 = 0
    score2 = 0 

    inform1 = tick1.info
    inform2 = tick2.info

    name1 = inform1.get('shortName')
    name2 = inform2.get('shortName')

    if inform1.get('trailingPE') > inform2.get*('trailingPE'):
        paragraph += f'{name2} seems to have a lower PE ratio.'
        score2 += 1
    else:
        paragraph += f'{name1} seems to have a lower PE ratio.'
        score1 += 1

    if inform1.get('epsCurrentYear') > inform2.get*('epsCurrentYear'):
        paragraph += f'{name1} seems to have a greater earnings per ratio.'
        score1 += 1 
    else:
        paragraph += f'{name2} seems to have a greater earnings per ratio.'
        score2 += 1

    if inform1.get('trailingPegRatio') > 1:
        f'{name1} exhibits some atypical behavior with a high PEG ratio which is worth investigating'
        score1 -= 1
    if inform2.get('trailingPegRatio') > 1:
        f'{name2} exhibits some atypical behavior with a high PEG ratio which is worth investigating'
        score2 -= 1

    if inform1.get('priceToSalesTrailing12Months') < inform2.get('priceToSalesTrailing12Months'):
        score1 += 1
        paragraph += f'{name1} has a lower price to sales ratio.'
    else: 
        score2 += 1
        paragraph += f'{name2} has a lower price to sales ratio.'
    
    if inform1.get('priceToBook') < inform2.get('priceToBook'):
        score1 += 1
        paragraph += f'{name1} has a lower price to book ratio, which is prefered. '
    else: 
        score2 += 1
        paragraph += f'{name2} has a lower price to book ratio, which is prefered.' 
    
    if inform1.get('dividendYield') > inform2.get('dividendYield'):
        score1 += 1
        paragraph += f'{name1} has a greater dividend yield, which is better.'
    else:
        score2 += 1
        paragraph += f'{name2} has a greater dividend yield, which is better.'

    if inform1.get('returnOnAssets') > inform2.get('returnOnAssets'):
        score1 += 1
        paragraph += f'{name1} has a greater return on assets in comparison to {name2}.'
    else:
        score2 += 1
        paragraph += f'{name2} has a greater return on assets in comparison to {name1}.'

    if inform1.get('returnOnEquity') > inform2.get('returnOnEquity'):
        score1 += 1
        paragraph += f'{name1} has a greater return on equity.'
    else:
        score2 += 1
        paragraph += f'{name2} has a greater return on equity.'
    
    if inform1.get('profitMargins') > inform2.get('profitMargins'):
        score1 += 1
        paragraph += f'{name1} has a greater profit margin.'
    else:
        score2 += 1
        paragraph += f'{name2} has a greater profit margin'

    if inform1.get('currentRatio') < 1:
        score1 -= 1
        paragraph += f'{name1} has a current ratio worth investigating.'
    
    if inform2.get('currentRatio') < 1:
        score2 -= 1
        paragraph += f'{name2} has a current ratio worth investigating.'

    if inform1.get("debtToEquity") < inform2.get('debtToEquity'):
        score1+= 1 
        paragraph += f'{name1} has a lower debt to equity ratio in comparison to {name2}. '
    else:
        score2+= 1 
        paragraph += f'{name2} has a lower debt to equity ratio in comparison to {name1}. '

    if inform1.get("beta") < inform2.get('beta'):
        score1+= 1 
        paragraph += f'{name1} is less volatiles than {name2}. '
    else:
        score2+= 1 
        paragraph += f'{name2} is less volatile than {name1}. '
    
    if score2 > score1:
        return [score2, paragraph]
    else:
        return [score1, paragraph]
    

def refine_paragraph(inList):
    result = client.models.generate_content(
        mdoel = 'gemini-2.0-flash', 
        contents = f'Rewrite the following paragraph to contain the same information but be better written: {inList[1]}'
    )

    output = result + f"\n It seems that {inList[0]} is the better stock based on a preliminary analysis of the stock."

    return output