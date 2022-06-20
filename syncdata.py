import os
import pandas as pd
import sys
import s3fs
from io import StringIO
import streamlit as st

def calculate_returns(df):
    df['return'] = (df['stock_price_usd']-df['stock_price_usd'].shift(1))/df['stock_price_usd'].shift(1)
    rets = df[['date','return']].copy(deep = True)
    rets['dollar_return'] = 0

    if len(df)%2 == 0:
        l = len(df)
    else:
        l = len(df)-1
    for i in range(0,l,2):

        if df['total_shares_held'].iloc[i] < 0:
            profit = abs(df['total_usd'].iloc[i])-df['total_usd'].iloc[i+1]
        else:
            profit = abs(df['total_usd'].iloc[i+1])-df['total_usd'].iloc[i]

        rets['dollar_return'].iloc[i+1] = profit
    
    rets['value'] = rets['dollar_return'].cumsum()
    
    rets = rets[rets.index % 2 != 0]

    rets.loc[-1] = ['2022-06-03 07:41:00',0,0,0]
    rets.index = rets.index+1
    rets.sort_index(inplace=True)

    rets['date'] = pd.to_datetime(rets['date'])
    rets['daily_first'] = rets.groupby(rets['date'].dt.date)['value'].transform("first")
    rets['weekly_first'] = rets.groupby(rets['date'].dt.week)['value'].transform("first")
    rets['monthly_first'] = rets.groupby(rets['date'].dt.month)['value'].transform("first")

    rets['daily_return'] = ((10000+rets['value'])-(10000+rets['daily_first']))/(10000+rets['daily_first'])
    rets['weekly_return'] = ((10000+rets['value'])-(10000+rets['weekly_first']))/(10000+rets['weekly_first'])
    rets['monthly_return'] = ((10000+rets['value'])-(10000+rets['monthly_first']))/(10000+rets['monthly_first'])
    
    rets = rets[['date','value','return','daily_return','weekly_return','monthly_return']]
    rets.columns = ['dt','profit_sum','return','daily_return','weekly_return','monthly_return']

    return rets

def sync_data():
    df = pd.read_csv("purchase_info.csv")
    df.to_csv("s3://research-dashboard/trading-dashboard-data/purchase_info.csv",
          storage_options={'key': st.secret['access_key'],
                           'secret': st.secrets['access_secret']})
    rets = calculate_returns(df)
    rets.to_csv("s3://research-dashboard/trading-dashboard-data/portfolio_returns.csv",
           storage_options={'key': st.secret['access_key'],
                           'secret': st.secrets['access_secret']})