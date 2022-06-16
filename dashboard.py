import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd 
import numpy as numpy
import time
import plotly.express as px
from backtest import backtest_dashboard
from realtime import realtime_dashboard
from datapath import *

#page config
st.set_page_config(
    layout = 'wide'
    )



#menu bar to switch between real-time results and back test results
with st.sidebar:
    selected = option_menu(
        menu_title = "Select a Dashboard",
        options = ['Real-Time','Backtesting']
    )



#real time dashboard
if selected == "Real-Time":
    st.write(transaction_data_path,portfolio_value_path)
    #realtime_dashboard(transaction_data_path,portfolio_value_path)

#backtest dashboard
if selected == "Backtesting":
    st.write(backtest_data_path)
    #backtest_dashboard(backtest_data_path)

   