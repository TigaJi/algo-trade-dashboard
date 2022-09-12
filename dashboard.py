import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from streamlit_option_menu import option_menu
import pandas as pd 
import numpy as numpy
import time
import plotly.express as px
from backtest import backtest_dashboard
from realtime import realtime_dashboard
from portfoliobacktest import portfolio_backtest_dashboard
from oauth2client.service_account import ServiceAccountCredentials



gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata'
  ]

gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("algo-trade-dashboard-80cae071e907.json", scope)
drive = GoogleDrive(gauth)



f1 = drive.CreateFile({'id': "1CrpCQLa3iO_8TIMDzWu3Sa0JLX93KPCW"})
f1.GetContentFile('purchase_info.csv')

f2 = drive.CreateFile({'id':'1GeheRrBIXGOOK8Uqj5I6sAjNTC2BYlTf'})
f2.GetContentFile("portfolio_returns.csv")


f3 = drive.CreateFile({'id':'1V7RcSGANiAp31-B6yUU5VBtlKYprnW0I'})
f3.GetContentFile("portfolio_backtest_result.csv")



#page config
st.set_page_config(
    page_title='Trading Dashboard',
    layout = 'wide'
    )



#menu bar to switch between real-time results and back test results
with st.sidebar:
    selected = option_menu(
        menu_title = "Select a Dashboard",
        options = ['Real-Time',"Portfolio Backtest"]
    )



#real time dashboard
if selected == "Real-Time":

    transaction_data = pd.read_csv("purchase_info.csv")
    portfolio_return = pd.read_csv("portfolio_returns.csv")
    
    realtime_dashboard(portfolio_return,transaction_data)
    

#backtest dashboard
#if selected == "Portfolio Backtest":
#    st.write(backtest_data_path)
#    backtest_dashboard(backtest_data_path)

if selected == "Portfolio Backtest":
    #backtest_data = pd.read_csv("portfolio_backtest_result.csv")
    portfolio_backtest_dashboard(drive)

   
