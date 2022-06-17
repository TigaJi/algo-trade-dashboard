import os
import pandas as pd
import sys
import s3fs
from io import StringIO

def calculate_returns(df):
    df['cash'] = 0
    df['cash'].loc[0] = 10000-df['total_usd'].loc[0]
    i = 1
    for i in range(1,len(df)):
        df['cash'].loc[i] = df['cash'].loc[i-1] - df['total_usd'].loc[i]
    rets = df.loc[df['total_shares_held'] == 0]
    rets = rets[['date','cash']]
    rets.reset_index(inplace = True,drop=True)
    rets.columns = ['dt','value']
    rets.loc[-1] = ['2022-06-03 07:41:00', 10000]
    rets.index = rets.index+1
    rets.sort_index(inplace=True) 
    rets['dt'] = pd.to_datetime(rets['dt'])
    
    rets['dt'] = pd.to_datetime(rets['dt'])

    rets['return'] = (rets['value']-rets['value'].shift(1))/rets['value'].shift(1)
    rets['daily_first'] = rets.groupby(rets['dt'].dt.date)['value'].transform("first")
    rets['weekly_first'] = rets.groupby(rets['dt'].dt.week)['value'].transform("first")
    rets['monthly_first'] = rets.groupby(rets['dt'].dt.month)['value'].transform("first")

    rets['daily_return'] = (rets['value']-rets['daily_first'])/rets['daily_first']
    rets['weekly_return'] = (rets['value']-rets['weekly_first'])/rets['weekly_first']
    rets['monthly_return'] = (rets['value']-rets['monthly_first'])/rets['monthly_first']
    
    rets = rets[['dt','value','return','daily_return','weekly_return','monthly_return']]
    rets = rets.round(decimals = 4)


    return rets


def sync_data():
    df = pd.read_csv("purchase_info.csv")
    try:
        df.to_csv("s3://research-dashboard/trading-dashboard-data/purchase_info.csv",
            storage_options={'key': 'AKIATHGO3RS3C7EMIAU4',
                           'secret': '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'})
    except Exception as e:
        print (e)
        print ("data uploaed failed.")
    
    try:
        rets = calculate_returns(df)
    except Exception as e:
        print(e)
        print("Couldn't calculate returns.")

    try:
        rets.to_csv("s3://research-dashboard/trading-dashboard-data/portfolio_returns.csv",
            storage_options={'key': 'AKIATHGO3RS3C7EMIAU4',
                           'secret': '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'})
    except Exception as e:
        print(e)
        print("data uploaed failed.")
    