import streamlit as st
import os
from dotenv import load_dotenv, dotenv_values
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from otherFunctions import get_the_news, convertTime
from analysisFunctions import candleplot, lineplot

