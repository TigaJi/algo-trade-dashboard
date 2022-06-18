import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd 
import numpy as numpy
import time
import plotly.express as px
from backtest import backtest_dashboard
from realtime import realtime_dashboard
from datapath import *
import boto3
from io import StringIO


client = boto3.client('s3', aws_access_key_id='AKIATHGO3RS3C7EMIAU4',
        aws_secret_access_key='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')
bucket_name = 'research-dashboard'


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
    transaction_obj = client.get_object(Bucket=bucket_name, Key='trading-dashboard-data/purchase_info.csv')
    transaction_body = transaction_obj['Body']
    transaction_csv_string = transaction_body.read().decode('utf-8')

    portfolio_obj = client.get_object(Bucket=bucket_name, Key='trading-dashboard-data/portfolio_returns.csv')
    portfolio_body = portfolio_obj['Body']
    portfolio_csv_string = portfolio_body.read().decode('utf-8')

    transaction_data = pd.read_csv(StringIO(transaction_csv_string))
    portfolio_return = pd.read_csv(StringIO(portfolio_csv_string))
    
    realtime_dashboard(portfolio_return,transaction_data)
    

#backtest dashboard
if selected == "Backtesting":
    st.write(backtest_data_path)
    backtest_dashboard(backtest_data_path)

   